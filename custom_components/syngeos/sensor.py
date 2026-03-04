"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfSoundPressure,
    UnitOfTemperature,
)

from .entity import SyngeosEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SyngeosDataUpdateCoordinator
    from .data import SyngeosConfigEntry


ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="temperature",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        translation_key="temperature",
    ),
    SensorEntityDescription(
        key="humidity",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        translation_key="humidity",
    ),
    SensorEntityDescription(
        key="pressure",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        translation_key="pressure",
    ),
    SensorEntityDescription(
        key="pm1",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM1,
        translation_key="pm1",
    ),
    SensorEntityDescription(
        key="pm25",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM25,
        translation_key="pm25",
    ),
    SensorEntityDescription(
        key="pm10",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM10,
        translation_key="pm10",
    ),
    SensorEntityDescription(
        key="caqi",
        state_class=SensorStateClass.MEASUREMENT,
        translation_key="caqi",
    ),
    SensorEntityDescription(
        key="co",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.CO,
        translation_key="co",
    ),
    SensorEntityDescription(
        key="no2",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.NITROGEN_DIOXIDE,
        translation_key="no2",
    ),
    SensorEntityDescription(
        key="so2",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.SULPHUR_DIOXIDE,
        translation_key="so2",
    ),
    SensorEntityDescription(
        key="o3",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.OZONE,
        translation_key="o3",
    ),
    SensorEntityDescription(
        key="c6h6",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        translation_key="c6h6",
    ),
    SensorEntityDescription(
        key="ch2o",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        translation_key="ch2o",
    ),
    SensorEntityDescription(
        key="noise",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfSoundPressure.DECIBEL,
        translation_key="noise",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SyngeosConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    api_data = entry.runtime_data.coordinator.data
    entities_to_add = []
    sensor_names = {sensor.get("name") for sensor in api_data.get("sensors", [])}
    sensor_name_mapping = {"pressure": "air_pressure", "pm25": "pm2_5"}
    for description in ENTITY_DESCRIPTIONS:
        key = description.key

        if (key in sensor_names) or (
            key in sensor_name_mapping and sensor_name_mapping.get(key) in sensor_names
        ):
            entities_to_add.append(description)

    async_add_entities(
        SyngeosSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in entities_to_add
    )


class SyngeosSensor(SyngeosEntity, SensorEntity):
    """Syngeos Sensor class."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SyngeosDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description.key)
        self.entity_description = entity_description

    def get_sensor_state(
        self, sensors: list[dict[str, Any]], sensor_name: str
    ) -> str | None:
        """Get sensor state from sensor array and updates it's attributes."""
        if sensors is None:
            return None
        result = None
        for sensor in sensors:
            if (
                sensor.get("name") == sensor_name
                and "data" in sensor
                and len(sensor["data"]) == 1
            ):
                sensor_data = sensor["data"][0]
                result = sensor_data.get("value")
                self._attr_extra_state_attributes = {
                    "last_updated": sensor_data.get("read_at")
                }
                if "current_norm" in sensor_data:
                    self._attr_extra_state_attributes.update(
                        {"current_norm": sensor_data.get("current_norm")}
                    )
                if "threshold_level" in sensor_data:
                    self._attr_extra_state_attributes.update(
                        {"threshold_level": sensor_data.get("threshold_level")}
                    )
                break
        return result

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        apiData = self.coordinator.data
        if apiData is None or not isinstance(apiData, dict):
            return None

        if self.entity_description.key == "pressure":
            return self.get_sensor_state(apiData.get("sensors"), "air_pressure")
        if self.entity_description.key == "pm25":
            return self.get_sensor_state(apiData.get("sensors"), "pm2_5")

        return self.get_sensor_state(
            apiData.get("sensors"), self.entity_description.key
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.native_value is not None
