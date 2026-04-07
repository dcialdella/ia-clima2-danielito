"""Modelos de datos para el sistema Weather HTML Display."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class WeatherConditionType(Enum):
    """Tipos de condiciones climáticas soportadas."""
    SUNNY = "sol"
    PARTLY_CLOUDY = "parcialmente_nublado"
    VERY_CLOUDY = "muy_nublado"
    OVERCAST = "totalmente_nublado"
    LIGHT_RAIN = "lluvia_leve"
    HEAVY_RAIN = "lluvia_fuerte"
    SNOW = "nieve"
    MIST = "bruma"


@dataclass
class WeatherData:
    """Datos meteorológicos obtenidos de servicios externos."""
    temperature: float
    feels_like: float
    condition: WeatherConditionType
    condition_description: str
    humidity: int  # percentage
    wind_speed: float  # m/s or mph
    visibility: Optional[int]  # meters
    uv_index: Optional[float]
    timestamp: datetime
    source: str  # "openweathermap" or "open-meteo"


@dataclass
class ColorScheme:
    """Esquema de colores para la página HTML."""
    background: str  # hex color
    text: str  # hex color
    accent: str  # hex color


@dataclass
class UserPreferences:
    """Preferencias del usuario."""
    language: str  # "en", "fr", "it", "es", "zh", "de"
    temp_unit: str  # "celsius", "fahrenheit"
    font_size: str  # "xs", "s", "m", "l", "xl"
    last_city: Optional[str]
