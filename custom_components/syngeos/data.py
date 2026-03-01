"""Custom types for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import SyngeosClient
    from .coordinator import SyngeosDataUpdateCoordinator

type SyngeosConfigEntry = ConfigEntry[SyngeosData]


@dataclass
class SyngeosData:
    """Data for Syngeos integration."""

    client: SyngeosClient
    coordinator: SyngeosDataUpdateCoordinator
    integration: Integration
    station_id: str
