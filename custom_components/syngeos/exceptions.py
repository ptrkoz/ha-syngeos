"""Exceptions for the Syngeos integration."""

from homeassistant.exceptions import HomeAssistantError


class SyngeosException(HomeAssistantError):
    """Base exception for the Syngeos integration."""


class SyngeosClientError(SyngeosException):
    """Custom exception to indicate Syngeos API errors."""


class SyngeosClientCommunicationError(SyngeosClientError):
    """Exception to indicate a communication error."""


class SyngeosCannotConnect(SyngeosException):
    """Error to indicate we cannot connect."""


class SyngeosNoDataAvailable(SyngeosException):
    """Error to indicate there's no data available for that station."""


class SyngeosInvalidResponse(SyngeosException):
    """Error to indicate there is invalid response."""
