"""Cliente API para obtener datos meteorológicos con failover."""

import urllib.request
import urllib.error
import urllib.parse
import json
from datetime import datetime
from typing import Optional
from src.models import WeatherData, WeatherConditionType


class WeatherDisplayError(Exception):
    """Excepción base para el sistema."""

    pass


class CityNotFoundError(WeatherDisplayError):
    """Ciudad no encontrada en servicios meteorológicos."""

    pass


class WeatherServiceUnavailableError(WeatherDisplayError):
    """Todos los servicios meteorológicos no disponibles."""

    pass


class InvalidAPIKeyError(WeatherDisplayError):
    """API key inválida o faltante."""

    pass


class WeatherAPIClient:
    """Cliente para obtener datos meteorológicos con failover automático."""

    def __init__(self, api_key: str = ""):
        """
        Inicializa el cliente API.

        Args:
            api_key: API key para OpenWeatherMap (opcional para Open-Meteo)
        """
        self.api_key = api_key
        self.timeout = 5  # segundos

    def get_weather_data(self, city: str, language: str = "en") -> WeatherData:
        """
        Obtiene datos meteorológicos con failover automático.

        Args:
            city: Nombre de la ciudad
            language: Código de idioma para descripciones

        Returns:
            WeatherData con la información meteorológica

        Raises:
            CityNotFoundError: Si la ciudad no se encuentra
            WeatherServiceUnavailableError: Si todos los servicios fallan
            InvalidAPIKeyError: Si la API key es inválida
        """
        # Intentar fuente primaria (OpenWeatherMap)
        try:
            return self._fetch_from_primary(city, language)
        except (CityNotFoundError, InvalidAPIKeyError):
            # Estos errores no se recuperan con failover
            raise
        except Exception:
            # Cualquier otro error, intentar fuente secundaria
            pass

        # Intentar fuente secundaria (Open-Meteo)
        try:
            return self._fetch_from_secondary(city, language)
        except CityNotFoundError:
            raise
        except Exception:
            pass

        # Ambas fuentes fallaron
        raise WeatherServiceUnavailableError("All weather services are unavailable")

    def _fetch_from_primary(self, city: str, language: str) -> WeatherData:
        """
        Obtiene datos de OpenWeatherMap (fuente primaria).

        Args:
            city: Nombre de la ciudad
            language: Código de idioma

        Returns:
            WeatherData

        Raises:
            CityNotFoundError: Ciudad no encontrada
            InvalidAPIKeyError: API key inválida
            Exception: Otros errores de red o parsing
        """
        if not self.api_key:
            raise InvalidAPIKeyError("OpenWeatherMap API key is required")

        # Mapeo de códigos de idioma a códigos de OpenWeatherMap
        lang_map = {
            "en": "en",
            "es": "es",
            "fr": "fr",
            "it": "it",
            "de": "de",
            "zh": "zh_cn",
        }
        owm_lang = lang_map.get(language, "en")

        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"q={urllib.parse.quote(city)}&"
            f"appid={self.api_key}&"
            f"units=metric&"
            f"lang={owm_lang}"
        )

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))

            # Parsear respuesta
            condition = self._map_owm_code_to_condition(data["weather"][0]["id"])

            return WeatherData(
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                condition=condition,
                condition_description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                visibility=data.get("visibility"),
                uv_index=None,  # OWM no incluye UV en endpoint básico
                timestamp=datetime.now(),
                source="openweathermap",
            )

        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise CityNotFoundError(f"City '{city}' not found")
            elif e.code == 401:
                raise InvalidAPIKeyError("Invalid OpenWeatherMap API key")
            else:
                raise Exception(f"HTTP error {e.code}")
        except urllib.error.URLError:
            raise Exception("Network error or timeout")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Error parsing API response: {e}")

    def _fetch_from_secondary(self, city: str, language: str) -> WeatherData:
        """
        Obtiene datos de Open-Meteo (fuente secundaria).

        Args:
            city: Nombre de la ciudad
            language: Código de idioma (no usado por Open-Meteo)

        Returns:
            WeatherData

        Raises:
            CityNotFoundError: Ciudad no encontrada
            Exception: Otros errores
        """
        # Primero necesitamos geocodificar la ciudad
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=en&format=json"

        try:
            req = urllib.request.Request(geocode_url)
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                geo_data = json.loads(response.read().decode("utf-8"))

            if not geo_data.get("results"):
                raise CityNotFoundError(f"City '{city}' not found")

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            # Obtener datos meteorológicos
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&"
                f"current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&"
                f"timezone=auto"
            )

            req = urllib.request.Request(weather_url)
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                weather_data = json.loads(response.read().decode("utf-8"))

            current = weather_data["current"]
            condition = self._map_wmo_code_to_condition(current["weather_code"])

            return WeatherData(
                temperature=current["temperature_2m"],
                feels_like=current[
                    "temperature_2m"
                ],  # Open-Meteo no proporciona feels_like
                condition=condition,
                condition_description=condition.value,
                humidity=current["relative_humidity_2m"],
                wind_speed=current["wind_speed_10m"] / 3.6,  # Convertir km/h a m/s
                visibility=None,
                uv_index=None,
                timestamp=datetime.now(),
                source="open-meteo",
            )

        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP error {e.code}")
        except urllib.error.URLError:
            raise Exception("Network error or timeout")
        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Error parsing API response: {e}")

    def _map_owm_code_to_condition(self, code: int) -> WeatherConditionType:
        """
        Mapea código de OpenWeatherMap a WeatherConditionType.

        Args:
            code: Código de condición de OpenWeatherMap

        Returns:
            WeatherConditionType correspondiente
        """
        if code == 800:
            return WeatherConditionType.SUNNY
        elif code == 801:
            return WeatherConditionType.PARTLY_CLOUDY
        elif code == 802:
            return WeatherConditionType.VERY_CLOUDY
        elif code in (803, 804):
            return WeatherConditionType.OVERCAST
        elif code in range(300, 322) or code in (500, 501):
            return WeatherConditionType.LIGHT_RAIN
        elif code in range(502, 532):
            return WeatherConditionType.HEAVY_RAIN
        elif code in range(600, 623):
            return WeatherConditionType.SNOW
        elif code in (701, 741):
            return WeatherConditionType.MIST
        else:
            # Default para códigos no mapeados
            return WeatherConditionType.PARTLY_CLOUDY

    def _map_wmo_code_to_condition(self, code: int) -> WeatherConditionType:
        """
        Mapea código WMO de Open-Meteo a WeatherConditionType.

        Args:
            code: Código WMO

        Returns:
            WeatherConditionType correspondiente
        """
        if code == 0:
            return WeatherConditionType.SUNNY
        elif code in (1, 2):
            return WeatherConditionType.PARTLY_CLOUDY
        elif code == 3:
            return WeatherConditionType.OVERCAST
        elif code in (45, 48):
            return WeatherConditionType.MIST
        elif code in range(51, 56):
            return WeatherConditionType.LIGHT_RAIN
        elif code in range(61, 66) or code in range(80, 83):
            return WeatherConditionType.HEAVY_RAIN
        elif code in range(71, 78) or code in range(85, 87):
            return WeatherConditionType.SNOW
        else:
            return WeatherConditionType.PARTLY_CLOUDY
