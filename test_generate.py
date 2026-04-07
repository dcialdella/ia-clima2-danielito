"""Script de prueba para generar HTML sin necesidad de API key real."""

from datetime import datetime
from src.models import WeatherData, WeatherConditionType
from src.html_generator import HTMLGenerator

# Crear datos de prueba
weather_data = WeatherData(
    temperature=22.5,
    feels_like=24.0,
    condition=WeatherConditionType.PARTLY_CLOUDY,
    condition_description="Parcialmente nublado con sol",
    humidity=65,
    wind_speed=5.2,
    visibility=10000,
    uv_index=6.5,
    timestamp=datetime.now(),
    source="test"
)

# Generar HTML en español
print("Generando HTML en español...")
generator_es = HTMLGenerator(language="es", temp_unit="celsius", font_size="m")
html_es = generator_es.generate_html(weather_data, "Madrid")

with open("weather_madrid_es.html", "w", encoding="utf-8") as f:
    f.write(html_es)
print("✓ Generado: weather_madrid_es.html")

# Generar HTML en inglés con Fahrenheit
print("\nGenerando HTML en inglés con Fahrenheit...")
generator_en = HTMLGenerator(language="en", temp_unit="fahrenheit", font_size="l")
html_en = generator_en.generate_html(weather_data, "London")

with open("weather_london_en.html", "w", encoding="utf-8") as f:
    f.write(html_en)
print("✓ Generado: weather_london_en.html")

# Generar HTML con clima soleado
print("\nGenerando HTML con clima soleado...")
sunny_data = WeatherData(
    temperature=28.0,
    feels_like=30.0,
    condition=WeatherConditionType.SUNNY,
    condition_description="Cielo despejado",
    humidity=45,
    wind_speed=3.5,
    visibility=15000,
    uv_index=8.0,
    timestamp=datetime.now(),
    source="test"
)
generator_sunny = HTMLGenerator(language="es", temp_unit="celsius", font_size="m")
html_sunny = generator_sunny.generate_html(sunny_data, "Barcelona")

with open("weather_barcelona_sunny.html", "w", encoding="utf-8") as f:
    f.write(html_sunny)
print("✓ Generado: weather_barcelona_sunny.html")

# Generar HTML con lluvia fuerte
print("\nGenerando HTML con lluvia fuerte...")
rain_data = WeatherData(
    temperature=15.0,
    feels_like=13.0,
    condition=WeatherConditionType.HEAVY_RAIN,
    condition_description="Lluvia intensa",
    humidity=90,
    wind_speed=12.5,
    visibility=3000,
    uv_index=1.0,
    timestamp=datetime.now(),
    source="test"
)
generator_rain = HTMLGenerator(language="es", temp_unit="celsius", font_size="m")
html_rain = generator_rain.generate_html(rain_data, "Seattle")

with open("weather_seattle_rain.html", "w", encoding="utf-8") as f:
    f.write(html_rain)
print("✓ Generado: weather_seattle_rain.html")

# Generar HTML con nieve
print("\nGenerando HTML con nieve...")
snow_data = WeatherData(
    temperature=-5.0,
    feels_like=-8.0,
    condition=WeatherConditionType.SNOW,
    condition_description="Nevando",
    humidity=85,
    wind_speed=8.0,
    visibility=2000,
    uv_index=0.5,
    timestamp=datetime.now(),
    source="test"
)
generator_snow = HTMLGenerator(language="en", temp_unit="fahrenheit", font_size="xl")
html_snow = generator_snow.generate_html(snow_data, "Moscow")

with open("weather_moscow_snow.html", "w", encoding="utf-8") as f:
    f.write(html_snow)
print("✓ Generado: weather_moscow_snow.html")

print("\n" + "="*60)
print("✓ Todos los archivos HTML generados exitosamente!")
print("="*60)
print("\nArchivos generados:")
print("  - weather_madrid_es.html (Parcialmente nublado, español, Celsius)")
print("  - weather_london_en.html (Parcialmente nublado, inglés, Fahrenheit)")
print("  - weather_barcelona_sunny.html (Soleado, español, Celsius)")
print("  - weather_seattle_rain.html (Lluvia fuerte, español, Celsius)")
print("  - weather_moscow_snow.html (Nieve, inglés, Fahrenheit)")
print("\nAbre cualquiera de estos archivos en tu navegador para ver el resultado.")
