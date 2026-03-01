"""DataUpdateCoordinator for Syngeos."""

from __future__ import annotations

from typing import Any

from homeassistant.const import CONF_ID
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SyngeosClientError


class SyngeosDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Syngeos data API."""

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data(
                self.config_entry.data[CONF_ID]
            )
        except SyngeosClientError as exception:
            raise UpdateFailed(exception) from exception
