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

# Integracja Syngeos dla Home Assistant

[🇬🇧 English](https://github.com/ptrkoz/ha-syngeos) | 🇵🇱 Polski


Niestandardowa integracja Syngeos dostarczająca dane o jakości powietrza z stacji [Syngeos](https://syngeos.pl/) do [Home Assistant](https://www.home-assistant.io/).

Integracja dostarcza następujące encje z skonfigurowanej stacji Syngeos:
- temperatura (*°C*)
- wilgotność (*%*)
- ciśnienie powietrza (*hPa*)
- poziom PM1 (*μg/m³*)
- poziom PM2,5 (*μg/m³*)
- poziom PM10 (*μg/m³*)
- indeks CAQI (skala od *0* do *>100*)
- poziom tlenku węgla (*mg/m³*)
- poziom dwutlenku azotu (*μg/m³*)
- poziom dwutlenku siarki (*μg/m³*)
- poziom ozonu (*μg/m³*)
- poziom benzenu (*μg/m³*)
- poziom formaldehydu (*μg/m³*)
- poziom hałasu (*dB*)

Każda encja ma atrybut *last_updated* z czasem ostatniego pomiaru. 

Niektóre stacje mogę nie posiadać wszystkich encji wymienionych powyżej.

**Zastrzeżenie** To nie jest oficjalna integracja stworzona lub wspierana przez Syngeos

## Instalacja

Tą integrację można zainstalować przez HACS lub manualnie.

### Instalacja integracji przez HACS (zalecane)
1. Upewnij się, że [HACS](https://hacs.xyz) jest zainstalowany w twoim Home Assistant

2. Dodaj niestandardowe repozytorium do HACS klikając przycisk poniżej:

	[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ptrkoz&category=integration&repository=ha-syngeos)
	
	Lub przejdź do: **HACS** → **3 kropki (⋮)** → **Niestandardowe repozytoria**

	- Repozytorium: https://github.com/ptrkoz/ha-syngeos
	- Typ: **Integracja**
	
    Następnie kliknij **DODAJ**

3. Wyszukaj "Syngeos" w HACS i kliknij na wyszukaną integrację, a następnie kliknij **POBIERZ** (niebieski przycisk w prawym dolnym rogu)

4. Zrestartuj Home Assistant

### Instalacja integracji manualnie

1. Pobierz [syngeos.zip](https://github.com/ptrkoz/ha-syngeos/releases/latest/download/syngeos.zip) z [ostatniego wydania](https://github.com/ptrkoz/ha-syngeos/releases/latest), rozpakuj go, a następnie dodaj/scal z zawartością folderu `custom_components/` w twoim katalogu konfiguracji

2. Zrestartuj Home Assistant

## Konfiguracja

Skonfiguruj tą integrację w Home Assistant używając przycisku poniżej:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=syngeos)

Lub przejdź do: **Ustawienia** → **Urządzenia oraz usługi** → **Dodaj integrację** → **Syngeos**
