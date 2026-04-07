# Weather HTML Display

Sistema que obtiene datos meteorológicos de servicios externos y genera páginas HTML completamente autónomas con visualización atractiva del clima.

## Características

- 🌍 Soporte para 6 idiomas (inglés, francés, italiano, español, chino, alemán)
- 🌡️ Selección de unidades de temperatura (Celsius/Fahrenheit)
- 📏 5 tamaños de fuente ajustables para accesibilidad
- 🎨 Esquemas de color dinámicos según condiciones climáticas
- 🔄 Failover automático entre fuentes de datos (OpenWeatherMap + Open-Meteo)
- 📦 HTML completamente autónomo (sin dependencias externas)
- 🔁 Regeneración automática programable cada hora
- 🎨 Iconos SVG inline para 8 condiciones climáticas
- 🌡️ Termómetro vintage SVG

## Requisitos

- Python 3.8 o superior
- No requiere dependencias externas en runtime (solo biblioteca estándar)

## Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd weather-html-display

# Instalar el paquete
pip install -e .

# Para desarrollo (incluye herramientas de testing)
pip install -r requirements-dev.txt
```

## Configuración

### API Key de OpenWeatherMap

El sistema usa OpenWeatherMap como fuente primaria de datos. Necesitas una API key gratuita:

1. Regístrate en [OpenWeatherMap](https://openweathermap.org/api)
2. Obtén tu API key gratuita (1000 llamadas/día)
3. Configura la API key:

```bash
# Opción 1: Mediante argumento de línea de comandos
python -m src.cli --api-key YOUR_API_KEY --city London

# Opción 2: Editar archivo de configuración
# El archivo se crea automáticamente en ~/.weather-display-config.json
```

### Archivo de Configuración

El archivo de configuración se encuentra en `~/.weather-display-config.json`:

```json
{
  "language": "en",
  "temp_unit": "celsius",
  "font_size": "m",
  "last_city": "London",
  "api_keys": {
    "openweathermap": "YOUR_API_KEY_HERE"
  }
}
```

## Uso

### Uso Básico

```bash
# Generar HTML para una ciudad
python -m src.cli --city "London"

# Con opciones personalizadas
python -m src.cli --city "Paris" --language fr --temp-unit celsius --font-size l

# Especificar archivo de salida
python -m src.cli --city "Tokyo" --output ~/weather/tokyo.html
```

### Opciones de Línea de Comandos

- `--city`: Nombre de la ciudad (requerido en primera ejecución)
- `--language`: Idioma (en, fr, it, es, zh, de)
- `--temp-unit`: Unidad de temperatura (celsius, fahrenheit)
- `--font-size`: Tamaño de fuente (xs, s, m, l, xl)
- `--output`: Ruta del archivo HTML de salida
- `--api-key`: API key de OpenWeatherMap

### Regeneración Automática

#### Linux/macOS (cron)

Editar crontab:

```bash
crontab -e
```

Agregar línea para ejecutar cada hora:

```bash
# Regenerar cada hora
0 * * * * /usr/bin/python3 /path/to/weather-html-display/src/cli.py --city "London" --output /home/user/weather.html

# Regenerar cada 30 minutos
*/30 * * * * /usr/bin/python3 /path/to/weather-html-display/src/cli.py --city "London" --output /home/user/weather.html
```

#### Windows (Task Scheduler)

Crear tarea programada con PowerShell:

```powershell
# Crear acción
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\path\to\weather-html-display\src\cli.py --city London --output C:\Users\user\weather.html"

# Crear trigger (cada hora)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)

# Registrar tarea
Register-ScheduledTask -TaskName "WeatherHTMLDisplay" -Action $action -Trigger $trigger
```

O usar la interfaz gráfica:

1. Abrir Task Scheduler
2. Crear tarea básica
3. Trigger: Diariamente, repetir cada 1 hora
4. Acción: Iniciar programa
   - Programa: `python.exe`
   - Argumentos: `C:\path\to\src\cli.py --city London --output C:\Users\user\weather.html`

## Estructura del Proyecto

```
weather-html-display/
├── src/
│   ├── __init__.py
│   ├── cli.py                    # CLI interface
│   ├── config_manager.py         # Gestión de configuración
│   ├── weather_api_client.py     # Cliente API con failover
│   ├── html_generator.py         # Generador de HTML
│   ├── svg_icon_generator.py     # Generador de iconos SVG
│   ├── thermometer_generator.py  # Generador de termómetro
│   ├── translations.py           # Diccionarios de traducción
│   └── models.py                 # Dataclasses y enums
├── tests/
│   ├── unit/                     # Unit tests
│   └── property/                 # Property-based tests
├── requirements.txt              # Sin dependencias de runtime
├── requirements-dev.txt          # pytest, hypothesis, pytest-cov
├── setup.py
└── README.md
```

## Desarrollo

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Solo unit tests
pytest tests/unit/

# Solo property tests
pytest tests/property/

# Con cobertura
pytest --cov=src --cov-report=html
```

### Logging

Los logs se guardan en `~/.weather-display.log` con rotación automática (últimos 7 días).

Formato:
```
[2025-01-14 15:30:45] INFO [WeatherAPIClient] Fetching weather for London
[2025-01-14 15:30:46] INFO [WeatherAPIClient] Successfully retrieved data from openweathermap
[2025-01-14 15:30:47] INFO [cli] Generated HTML file: /home/user/weather_london_20250114_153047.html
```

## Condiciones Climáticas Soportadas

El sistema reconoce y visualiza 8 condiciones climáticas:

1. ☀️ Sol (Sunny)
2. ⛅ Parcialmente nublado (Partly Cloudy)
3. ☁️ Muy nublado (Very Cloudy)
4. ☁️ Totalmente nublado (Overcast)
5. 🌧️ Lluvia leve (Light Rain)
6. 🌧️ Lluvia fuerte (Heavy Rain)
7. ❄️ Nieve (Snow)
8. 🌫️ Bruma (Mist)

## Failover de Fuentes de Datos

El sistema implementa failover automático:

1. **Primaria**: OpenWeatherMap (requiere API key)
2. **Secundaria**: Open-Meteo (sin API key requerida)

Si la fuente primaria falla, el sistema automáticamente intenta la secundaria.

## Características del HTML Generado

- ✅ HTML5 válido
- ✅ Completamente autónomo (sin CDNs ni recursos externos)
- ✅ CSS inline con diseño responsivo
- ✅ JavaScript vanilla inline (si se necesita en futuras versiones)
- ✅ Meta refresh tag (recarga cada hora)
- ✅ Iconos SVG inline
- ✅ Termómetro vintage SVG
- ✅ Timestamp de actualización centrado en footer
- ✅ Esquemas de color según clima
- ✅ Contraste WCAG AA mínimo

## Solución de Problemas

### Error: "Invalid API key"

- Verifica que tu API key de OpenWeatherMap sea correcta
- Asegúrate de que la API key esté activada (puede tomar unos minutos después del registro)

### Error: "City not found"

- Verifica la ortografía del nombre de la ciudad
- Intenta con el nombre en inglés
- Algunos nombres de ciudades requieren el país: "London,UK"

### Error: "Weather services are currently unavailable"

- Verifica tu conexión a internet
- Los servicios pueden estar temporalmente caídos
- El sistema reintentará automáticamente en la próxima ejecución programada

### HTML no se actualiza

- Verifica que el cron job o tarea programada esté activa
- Revisa los logs en `~/.weather-display.log`
- Asegúrate de que el navegador no esté cacheando la página (Ctrl+F5 para forzar recarga)

## Issues Conocidos

⚠️ **Bug Crítico**: Falta importar `urllib.parse` en `src/weather_api_client.py`.

**Para corregir, agregar al inicio del archivo:**
```python
import urllib.parse
```

Ver `docs/ANALISIS_CODIGO.md` para análisis completo de bugs y mejoras.

## Licencia

[Especificar licencia]

## Contribuciones

[Especificar guías de contribución]
