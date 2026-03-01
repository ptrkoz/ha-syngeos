"""Constants for the Syngeos integration."""

DOMAIN = "syngeos"
MANUFACTURER = "Syngeos"
LIST_OF_STATIONS_API_URL = "https://api.syngeos.pl/api/v2/public/data/{filter_type}"
STATION_DETAILS_API_URL = "https://api.syngeos.pl/api/public/data/device/{station_id}"
STATION_DETAILS_WEBSITE_URL = (
    "https://panel.syngeos.pl/sensor/{filter_type}?device={station_id}"
)
FILTER_TYPES = [
    "pm10",
    "pm2_5",
    "caqi",
    "co",
    "no2",
    "so2",
    "o3",
    "c6h6",
    "ch2o",
    "noise",
]
NEARBY_STATIONS_KM_RADIUS = 50
