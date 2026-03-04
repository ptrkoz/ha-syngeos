"""Config flow for the Syngeos integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from geopy.distance import geodesic
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_ID
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .api import SyngeosClient
from .const import (
    DOMAIN,
    FILTER_TYPES,
    LIST_OF_STATIONS_API_URL,
    NEARBY_STATIONS_KM_RADIUS,
)
from .exceptions import (
    SyngeosCannotConnect,
    SyngeosClientCommunicationError,
    SyngeosInvalidResponse,
    SyngeosNoDataAvailable,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): cv.positive_int,
    }
)


class SyngeosFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Syngeos."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        available_options = ["station_list_filter", "station_id"]
        if self.hass.config.latitude and self.hass.config.longitude:
            available_options.insert(0, "station_geolocation_filter")

        return self.async_show_menu(
            step_id="user",
            menu_options=available_options,
            description_placeholders={"nearby_radius": str(NEARBY_STATIONS_KM_RADIUS)},
        )

    async def get_list_of_stations(self, search_filter) -> list[dict[str, Any]]:
        """Gets the list of Syngeos stations."""
        client = SyngeosClient(session=async_get_clientsession(self.hass))
        stations = []
        if search_filter == "all":
            tasks = [
                client.async_get_list_of_stations(
                    LIST_OF_STATIONS_API_URL.format(filter_type=filter_type)
                )
                for filter_type in FILTER_TYPES
            ]
            results = await asyncio.gather(*tasks)
            ids = []
            for result in results:
                for station in result:
                    if (
                        "device" in station
                        and "id" in station["device"]
                        and station["device"]["id"] not in ids
                    ):
                        stations.append(station["device"])
                        ids.append(station["device"]["id"])
        else:
            result = await client.async_get_list_of_stations(
                LIST_OF_STATIONS_API_URL.format(filter_type=search_filter)
            )
            stations = [station["device"] for station in result if "device" in station]
        return stations

    @staticmethod
    def get_distance_to_station(e: SelectOptionDict) -> float:
        """Returns station distance from SelectOptionDict object."""
        return float(e.get("label").split(" - ")[-1].split(" ")[0])

    def get_available_options(
        self, stations: list[dict[str, Any]], with_geolocation: bool = False
    ) -> list[SelectOptionDict]:
        """Returns stations that can be selected."""
        options: list[SelectOptionDict] = []
        for station in stations:
            if (
                "id" in station
                and station["id"] > 0
                and "city" in station
                and station["city"] != ""
            ):
                value = str(station["id"])
                label = f"{station['city']}"
                if (
                    "address" in station
                    and station["address"] is not None
                    and station["address"] != ""
                ):
                    label += f" - {station['address']}"
                label += f" (ID: {station['id']})"
                if with_geolocation:
                    if "coordinates" in station and len(station["coordinates"]) == 2:
                        distance_to_station = round(
                            geodesic(
                                f"{station['coordinates'][0]},{station['coordinates'][1]}",
                                f"{self.hass.config.latitude},{self.hass.config.longitude}",
                            ).kilometers,
                            2,
                        )
                        if distance_to_station <= NEARBY_STATIONS_KM_RADIUS:
                            label += f" - {distance_to_station} km"
                        else:
                            continue
                    else:
                        continue
                options.append(SelectOptionDict(value=value, label=label))
        return options

    async def async_step_station_geolocation_filter(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle choosing the search filter for station geolocation step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            selected = user_input.get("search_filter")
            return await self.async_step_station_geolocation(
                user_input={"search_filter": selected}
            )

        options: list[SelectOptionDict] = [
            SelectOptionDict(value=filter_type, label=filter_type)
            for filter_type in FILTER_TYPES
        ]
        options.insert(0, SelectOptionDict(value="all", label="all"))

        schema: vol.Schema = vol.Schema(
            {
                vol.Required("search_filter"): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        translation_key="search_filter",
                        mode=SelectSelectorMode.LIST,
                    ),
                )
            }
        )

        return self.async_show_form(
            step_id="station_geolocation_filter",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_station_geolocation(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the station geolocation step."""
        errors: dict[str, str] = {}
        options: list[SelectOptionDict] = []
        if "syngeos_station" in user_input:
            selected = user_input.get("syngeos_station")
            return await self.async_step_station_id(user_input={CONF_ID: int(selected)})

        try:
            stations = await self.get_list_of_stations(user_input.get("search_filter"))
        except SyngeosClientCommunicationError:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            options: list[SelectOptionDict] = self.get_available_options(stations, True)

            options.sort(key=SyngeosFlowHandler.get_distance_to_station)

            if options is None or len(options) == 0:
                errors["base"] = "no_nearby_stations"

        schema: vol.Schema = vol.Schema(
            {
                vol.Required("syngeos_station"): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        mode=SelectSelectorMode.DROPDOWN,
                    ),
                )
            }
        )

        placeholders = {
            "station_number": str(len(options)),
            "nearby_radius": str(NEARBY_STATIONS_KM_RADIUS),
        }

        return self.async_show_form(
            step_id="station_geolocation",
            data_schema=schema,
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_station_list_filter(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle choosing the search filter for station geolocation step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            selected = user_input.get("search_filter")
            return await self.async_step_station_list(
                user_input={"search_filter": selected}
            )

        options: list[SelectOptionDict] = [
            SelectOptionDict(value=filter_type, label=filter_type)
            for filter_type in FILTER_TYPES
        ]
        options.insert(0, SelectOptionDict(value="all", label="all"))

        schema: vol.Schema = vol.Schema(
            {
                vol.Required("search_filter"): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        translation_key="search_filter",
                        mode=SelectSelectorMode.LIST,
                    ),
                )
            }
        )

        return self.async_show_form(
            step_id="station_list_filter",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_station_list(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the station list step."""
        errors: dict[str, str] = {}
        options: list[SelectOptionDict] = []
        if "syngeos_station" in user_input:
            selected = user_input.get("syngeos_station")
            return await self.async_step_station_id(user_input={CONF_ID: int(selected)})

        try:
            stations = await self.get_list_of_stations(user_input.get("search_filter"))
        except SyngeosClientCommunicationError:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            options: list[SelectOptionDict] = self.get_available_options(
                stations, False
            )

            if options is None or len(options) == 0:
                errors["base"] = "no_stations"

        schema: vol.Schema = vol.Schema(
            {
                vol.Required("syngeos_station"): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        sort=True,
                        mode=SelectSelectorMode.DROPDOWN,
                    ),
                )
            }
        )

        return self.async_show_form(
            step_id="station_list",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_station_id(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the station ID step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                response = await self.validate_input(user_input)
                filter_type = await self.get_filter_type(response)
                user_input["filter-type"] = filter_type
            except SyngeosCannotConnect:
                errors["base"] = "cannot_connect"
            except SyngeosInvalidResponse:
                errors["base"] = "invalid_response"
            except SyngeosNoDataAvailable:
                errors["base"] = "no_data_available"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(
                    str(user_input[CONF_ID]), raise_on_progress=False
                )
                self._abort_if_unique_id_configured()

                station_title = f"{response['city']}"
                if (
                    "address" in response
                    and response["address"] is not None
                    and response["address"] != ""
                ):
                    station_title += f" - {response['address']}"
                return self.async_create_entry(title=station_title, data=user_input)

        placeholders = {
            "deviceslist_url": "https://panel.syngeos.pl/",
            "example_deviceslist_url": "https://panel.syngeos.pl/sensor/pm10?device=671",
            "example_device_id": "671",
        }
        return self.async_show_form(
            step_id="station_id",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders=placeholders,
        )

    async def validate_input(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate connection."""
        client = SyngeosClient(session=async_get_clientsession(self.hass))
        response = await client.async_get_data(data[CONF_ID])
        if isinstance(response, dict) and response == {}:
            raise SyngeosNoDataAvailable
        if not response:
            raise SyngeosCannotConnect
        if (
            "id" not in response
            or response["id"] is None
            or "city" not in response
            or response["city"] is None
            or "sensors" not in response
        ):
            raise SyngeosInvalidResponse
        return response

    async def get_filter_type(self, api_response: dict[str, Any]) -> str:
        """Get filter type to create station website URL."""
        api_sensors = [sensor.get("name") for sensor in api_response["sensors"]]
        if "pm10" in api_sensors:
            return "pm10"
        if "pm2_5" in api_sensors:
            return "pm2_5"
        if "caqi" in api_sensors:
            return "caqi"
        if "co" in api_sensors:
            return "co"
        if "no2" in api_sensors:
            return "no2"
        if "so2" in api_sensors:
            return "so2"
        if "o3" in api_sensors:
            return "o3"
        if "c6h6" in api_sensors:
            return "c6h6"
        if "ch2o" in api_sensors:
            return "ch2o"
        if "noise" in api_sensors:
            return "noise"
        return "pm10"
