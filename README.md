[![HACS Default][hacs_shield]][hacs]
[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub All Releases][downloads_total_shield]][releases]
[![Installations][installations_shield]][releases]

[hacs_shield]: https://img.shields.io/static/v1.svg?label=HACS&message=Custom&color=orange&labelColor=41bdf5&logo=HomeAssistantCommunityStore&logoColor=white&style=flat-square
[hacs]:https://hacs.xyz/docs/faq/custom_repositories/

[releases_shield]: https://img.shields.io/github/v/release/ptrkoz/ha-syngeos?style=flat-square
[latest_release]: https://github.com/ptrkoz/ha-syngeos/releases/latest

[downloads_total_shield]: https://img.shields.io/github/downloads/ptrkoz/ha-syngeos/total?style=flat-square
[releases]: https://github.com/ptrkoz/ha-syngeos/releases

[installations_shield]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.syngeos.total&color=41bdf5&label=analytics&style=flat-square

# Syngeos integration for Home Assistant

🇬🇧 English | [🇵🇱 Polski](README.pl.md)


Syngeos custom integration provides air quality data from [Syngeos](https://syngeos.pl/) stations to [Home Assistant](https://www.home-assistant.io/).

<img width="837" height="516" alt="Syngeos integration entities screenshot" src="https://github.com/user-attachments/assets/5bab8709-5cad-43a1-bcf5-e74f3ae0d06f" />


The integration provides following entities with data from configured Syngeos station:
- temperature (*°C*)
- humidity (*%*)
- air pressure (*hPa*)
- PM1 pollution (*μg/m³*)
- PM2.5 pollution (*μg/m³*)
- PM10 pollution (*μg/m³*)
- CAQI index (scale of *0* to *>100*)
- carbon monoxide pollution (*mg/m³*)
- nitrogen dioxide pollution (*μg/m³*)
- sulfur dioxide pollution (*μg/m³*)
- ozone pollution (*μg/m³*)
- benzene pollution (*μg/m³*)
- formaldehyde pollution (*μg/m³*)
- noise level (*dB*)

Each entity has a *last_updated* attribute with time of the recent measurement.

Some stations may not include all entities listed above.

**Disclaimer** This is not an official integration from or supported by the Syngeos

## Installation

This integration can be installed either via HACS or manually.

### Install integration via HACS (recommended)
1. Make sure you have [HACS](https://hacs.xyz) installed in your Home Assistant

2. Add custom repository to HACS by clicking the button below:

	[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ptrkoz&category=integration&repository=ha-syngeos)
	
	Or go to: **HACS** → **3 dots (⋮)** → **Custom repositories**

	- Repository: https://github.com/ptrkoz/ha-syngeos
	- Type: **Integration**
	
    And click **ADD**

4. Search "Syngeos" in HACS and click on the found integration, next click **DOWNLOAD** (blue button in the bottom right corner)

5. Restart Home Assistant

### Install integration manually

1. Download [syngeos.zip](https://github.com/ptrkoz/ha-syngeos/releases/latest/download/syngeos.zip) from the [latest release](https://github.com/ptrkoz/ha-syngeos/releases/latest), unzip it, and add/merge the `custom_components/` folder with its contents in your configuration directory

2. Restart Home Assistant

## Configuration

To configure this integration in Home Assistant click the button below:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=syngeos)

Or go to: **Settings** → **Devices & services** → **Add integration** → **Syngeos**


<img width="446" height="272" alt="Syngeos integration select configuration method screenshot" src="https://github.com/user-attachments/assets/7e1cd084-19b3-4ca8-abcb-f24387c18594" />

You can add your Syngeos station in 3 ways:
- by finding the nearest stations and picking one of them

  <img width="443" height="275" alt="Syngeos integration select station from the nearest ones screenshot" src="https://github.com/user-attachments/assets/e13e2f38-103f-4d8e-963b-25e770030690" />
- by picking it from alphabetical list of active stations

  <img width="444" height="246" alt="Syngeos integration select station from the alphabetical list screenshot" src="https://github.com/user-attachments/assets/032803d3-6460-4f5f-9e51-c432fcf21e7c" />
- by manually entering station ID

  <img width="444" height="300" alt="Syngeos integration select station by ID screenshot" src="https://github.com/user-attachments/assets/da6f2895-4c41-4988-a1bf-2993be60d66a" />



