"""Syngeos API Client."""

from __future__ import annotations

import asyncio
import socket
from typing import Any

import aiohttp

from .const import STATION_DETAILS_API_URL
from .exceptions import (
    SyngeosClientCommunicationError,
    SyngeosClientError,
    SyngeosInvalidResponse,
)


class SyngeosClient:
    """Syngeos API client."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Syngeos API client."""
        self._session = session

    async def async_get_list_of_stations(self, api_url: str) -> list[dict[str, Any]]:
        """Get list of stations from Syngeos API."""
        stations = await self._api_wrapper(method="get", url=api_url)
        if not isinstance(stations, list):
            raise SyngeosInvalidResponse("Response object is not a list")
        return stations

    async def async_get_data(self, stationId: str) -> dict[str, Any]:
        """Get data from Syngeos API."""
        return await self._api_wrapper(
            method="get", url=STATION_DETAILS_API_URL.format(station_id=stationId)
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method=method, url=url, headers=headers, json=data
                )
                response.raise_for_status()
                return await response.json()
        except TimeoutError as exception:
            msg = f"Timeout errror fetching information - {exception}"
            raise SyngeosClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise SyngeosClientCommunicationError(msg) from exception
        except Exception as exception:
            msg = f"Unexpected error fetching information - {exception}"
            raise SyngeosClientError(msg) from exception
