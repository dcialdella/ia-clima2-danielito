"""Generador de páginas HTML completamente autónomas."""

from datetime import datetime
from src.models import WeatherData, ColorScheme, WeatherConditionType
from src.svg_icon_generator import SVGIconGenerator
from src.thermometer_generator import ThermometerGenerator
from src.translations import get_translation
import html


class HTMLGenerationError(Exception):
    """Error al generar HTML."""

    pass


class HTMLGenerator:
    """Genera páginas HTML completamente autónomas con CSS y JavaScript inline."""

    def __init__(self, language: str, temp_unit: str, font_size: str):
        """
        Inicializa el generador HTML.

        Args:
            language: Código de idioma (en, fr, it, es, zh, de)
            temp_unit: Unidad de temperatura (celsius, fahrenheit)
            font_size: Tamaño de fuente (xs, s, m, l, xl)
        """
        self.language = language
        self.temp_unit = temp_unit
        self.font_size = font_size
        self.icon_generator = SVGIconGenerator()
        self.thermometer_generator = ThermometerGenerator()

    def generate_html(self, weather_data: WeatherData, city: str) -> str:
        """
        Genera una página HTML completamente autónoma.

        Args:
            weather_data: Datos meteorológicos
            city: Nombre de la ciudad

        Returns:
            String con el HTML completo

        Raises:
            HTMLGenerationError: Si hay un error generando el HTML
        """
        try:
            # Escapar caracteres especiales en el nombre de la ciudad
            city_escaped = html.escape(city)

            # Obtener esquema de color según condición
            color_scheme = self._get_color_scheme(weather_data.condition)

            # Generar icono SVG
            weather_icon = self.icon_generator.generate_icon(weather_data.condition)

            # Convertir temperatura si es necesario
            temp_display = self._convert_temperature(weather_data.temperature)
            feels_like_display = self._convert_temperature(weather_data.feels_like)

            # Generar termómetro
            thermometer = self.thermometer_generator.generate_thermometer(
                temp_display, self.temp_unit
            )

            # Generar CSS
            css = self._generate_css(color_scheme)

            # Formatear timestamp
            timestamp_str = self._format_timestamp(weather_data.timestamp)

            translations = {
                "t_temp": get_translation(self.language, "temperature"),
                "t_feels": get_translation(self.language, "feels_like"),
                "t_humidity": get_translation(self.language, "humidity"),
                "t_wind": get_translation(self.language, "wind_speed"),
                "t_visibility": get_translation(self.language, "visibility"),
                "t_uv": get_translation(self.language, "uv_index"),
                "t_updated": get_translation(self.language, "updated"),
                "t_condition": get_translation(
                    self.language, weather_data.condition.value
                ),
            }

            # Símbolo de unidad
            unit_symbol = "°F" if self.temp_unit == "fahrenheit" else "°C"

            # Build HTML con lista para mejor performance
            html_parts = [
                f'''<!DOCTYPE html>
<html lang="{self.language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3600">
    <title>{city_escaped} - {translations["t_condition"]}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{city_escaped}</h1>
        </header>
        <main>
            <div class="weather-display">
                <div class="weather-icon">
                    {weather_icon}
                </div>
                <div class="thermometer">
                    {thermometer}
                </div>
            </div>
            <div class="temperature-main">
                <span class="temp-value">{temp_display:.1f}{unit_symbol}</span>
                <span class="condition">{translations["t_condition"]}</span>
            </div>
            <div class="details">
                <div class="detail-item">
                    <span class="detail-label">{translations["t_feels"]}:</span>
                    <span class="detail-value">{feels_like_display:.1f}{unit_symbol}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">{translations["t_humidity"]}:</span>
                    <span class="detail-value">{weather_data.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">{translations["t_wind"]}:</span>
                    <span class="detail-value">{weather_data.wind_speed:.1f} m/s</span>
                </div>''',
            ]

            if weather_data.visibility is not None:
                visibility_km = weather_data.visibility / 1000
                html_parts.append(
                    f'<div class="detail-item">'
                    f'<span class="detail-label">{translations["t_visibility"]}:</span>'
                    f'<span class="detail-value">{visibility_km:.1f} km</span>'
                    f"</div>"
                )

            if weather_data.uv_index is not None:
                html_parts.append(
                    f'<div class="detail-item">'
                    f'<span class="detail-label">{translations["t_uv"]}:</span>'
                    f'<span class="detail-value">{weather_data.uv_index:.1f}</span>'
                    f"</div>"
                )

            html_parts.extend(
                [
                    f'''
            </div>
        </main>
        <footer>
            <p class="timestamp">{translations["t_updated"]}: {timestamp_str}</p>
        </footer>
    </div>
    
    <div class="controls-panel">
        <button class="controls-toggle" onclick="toggleControls()">⚙️</button>
        <div class="controls-content" id="controlsContent">
            <h3>Settings / Configuración</h3>
            
            <div class="control-group">
                <label>Language / Idioma:</label>
                <select id="languageSelect" onchange="changeLanguage()">
                    <option value="en" {"selected" if self.language == "en" else ""}>English</option>
                    <option value="es" {"selected" if self.language == "es" else ""}>Español</option>
                    <option value="fr" {"selected" if self.language == "fr" else ""}>Français</option>
                    <option value="it" {"selected" if self.language == "it" else ""}>Italiano</option>
                    <option value="de" {"selected" if self.language == "de" else ""}>Deutsch</option>
                    <option value="zh" {"selected" if self.language == "zh" else ""}>中文</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>Temperature / Temperatura:</label>
                <select id="tempUnitSelect" onchange="changeTempUnit()">
                    <option value="celsius" {"selected" if self.temp_unit == "celsius" else ""}>Celsius (°C)</option>
                    <option value="fahrenheit" {"selected" if self.temp_unit == "fahrenheit" else ""}>Fahrenheit (°F)</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>Font Size / Tamaño:</label>
                <select id="fontSizeSelect" onchange="changeFontSize()">
                    <option value="xs" {"selected" if self.font_size == "xs" else ""}>Extra Small / Muy pequeño</option>
                    <option value="s" {"selected" if self.font_size == "s" else ""}>Small / Pequeño</option>
                    <option value="m" {"selected" if self.font_size == "m" else ""}>Medium / Mediano</option>
                    <option value="l" {"selected" if self.font_size == "l" else ""}>Large / Grande</option>
                    <option value="xl" {"selected" if self.font_size == "xl" else ""}>Extra Large / Muy grande</option>
                </select>
            </div>
        </div>
    </div>
    
    <script>
        const weatherData = {{
            temperature: {weather_data.temperature},
            feels_like: {weather_data.feels_like},
            condition: "{weather_data.condition.value}",
            condition_description: "{weather_data.condition_description}",
            humidity: {weather_data.humidity},
            wind_speed: {weather_data.wind_speed},
            visibility: {weather_data.visibility if weather_data.visibility is not None else "null"},
            uv_index: {weather_data.uv_index if weather_data.uv_index is not None else "null"}
        }};
        
        const city = "{city_escaped}";
        
        function toggleControls() {{
            const content = document.getElementById('controlsContent');
            content.style.display = content.style.display === 'block' ? 'none' : 'block';
        }}
        
        function changeLanguage() {{
            const lang = document.getElementById('languageSelect').value;
            localStorage.setItem('language', lang);
            alert('Language change requires page regeneration. Please run the program again with --language ' + lang);
        }}
        
        function changeTempUnit() {{
            const unit = document.getElementById('tempUnitSelect').value;
            localStorage.setItem('tempUnit', unit);
            const tempCelsius = weatherData.temperature;
            const feelsLikeCelsius = weatherData.feels_like;
            let tempDisplay, feelsLikeDisplay, symbol;
            if (unit === 'fahrenheit') {{
                tempDisplay = (tempCelsius * 9/5) + 32;
                feelsLikeDisplay = (feelsLikeCelsius * 9/5) + 32;
                symbol = '°F';
            }} else {{
                tempDisplay = tempCelsius;
                feelsLikeDisplay = feelsLikeCelsius;
                symbol = '°C';
            }}
            document.querySelector('.temp-value').textContent = tempDisplay.toFixed(1) + symbol;
            const detailValues = document.querySelectorAll('.detail-value');
            if (detailValues[0]) {{
                detailValues[0].textContent = feelsLikeDisplay.toFixed(1) + symbol;
            }}
        }}
        
        function changeFontSize() {{
            const size = document.getElementById('fontSizeSelect').value;
            const sizes = {{
                'xs': '12px',
                's': '14px',
                'm': '16px',
                'l': '18px',
                'xl': '22px'
            }};
            localStorage.setItem('fontSize', size);
            document.body.style.fontSize = sizes[size];
        }}
        
        window.onload = function() {{
            const savedLang = localStorage.getItem('language');
            const savedUnit = localStorage.getItem('tempUnit');
            const savedSize = localStorage.getItem('fontSize');
            if (savedLang) {{
                document.getElementById('languageSelect').value = savedLang;
            }}
            if (savedUnit) {{
                document.getElementById('tempUnitSelect').value = savedUnit;
                changeTempUnit();
            }}
            if (savedSize) {{
                document.getElementById('fontSizeSelect').value = savedSize;
                changeFontSize();
            }}
        }};
    </script>
</body>
</html>''',
                ]
            )

            return "".join(html_parts)

        except Exception as e:
            raise HTMLGenerationError(f"Error generating HTML: {e}")

    def _get_color_scheme(self, condition: WeatherConditionType) -> ColorScheme:
        """
        Obtiene el esquema de color según la condición climática.

        Args:
            condition: Condición climática

        Returns:
            ColorScheme con los colores apropiados
        """
        schemes = {
            WeatherConditionType.SUNNY: ColorScheme(
                background="#FFD700", text="#333333", accent="#FF8C00"
            ),
            WeatherConditionType.PARTLY_CLOUDY: ColorScheme(
                background="#87CEEB", text="#333333", accent="#4682B4"
            ),
            WeatherConditionType.VERY_CLOUDY: ColorScheme(
                background="#B0C4DE", text="#333333", accent="#708090"
            ),
            WeatherConditionType.OVERCAST: ColorScheme(
                background="#A9A9A9", text="#FFFFFF", accent="#696969"
            ),
            WeatherConditionType.LIGHT_RAIN: ColorScheme(
                background="#4682B4", text="#FFFFFF", accent="#1E90FF"
            ),
            WeatherConditionType.HEAVY_RAIN: ColorScheme(
                background="#191970", text="#FFFFFF", accent="#4169E1"
            ),
            WeatherConditionType.SNOW: ColorScheme(
                background="#F0F8FF", text="#333333", accent="#B0E0E6"
            ),
            WeatherConditionType.MIST: ColorScheme(
                background="#D3D3D3", text="#333333", accent="#A9A9A9"
            ),
        }

        return schemes.get(condition, schemes[WeatherConditionType.PARTLY_CLOUDY])

    def _generate_css(self, color_scheme: ColorScheme) -> str:
        """
        Genera el CSS inline para la página.

        Args:
            color_scheme: Esquema de colores a aplicar

        Returns:
            String con el CSS
        """
        # Tamaños de fuente base
        font_sizes = {"xs": "12px", "s": "14px", "m": "16px", "l": "18px", "xl": "22px"}
        base_size = font_sizes.get(self.font_size, "16px")

        css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: {base_size};
            background: linear-gradient(135deg, {color_scheme.background} 0%, {color_scheme.accent} 100%);
            color: {color_scheme.text};
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }}
        
        .container {{
            max-width: 800px;
            width: 100%;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        header h1 {{
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .weather-display {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 2rem;
        }}
        
        .weather-icon {{
            width: 150px;
            height: 150px;
        }}
        
        .weather-icon svg {{
            width: 100%;
            height: 100%;
        }}
        
        .thermometer {{
            width: 150px;
            height: 280px;
        }}
        
        .thermometer svg {{
            width: 100%;
            height: 100%;
        }}
        
        .temperature-main {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .temp-value {{
            font-size: 4em;
            font-weight: bold;
            display: block;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .condition {{
            font-size: 1.5em;
            display: block;
            margin-top: 0.5rem;
        }}
        
        .details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .detail-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 1rem;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .detail-label {{
            font-weight: bold;
            margin-right: 0.5rem;
        }}
        
        .detail-value {{
            font-size: 1.2em;
        }}
        
        footer {{
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 2px solid rgba(255, 255, 255, 0.3);
        }}
        
        .timestamp {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        /* Panel de controles */
        .controls-panel {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }}
        
        .controls-toggle {{
            background: rgba(255, 255, 255, 0.9);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
        }}
        
        .controls-toggle:hover {{
            transform: scale(1.1);
        }}
        
        .controls-content {{
            display: none;
            position: absolute;
            top: 60px;
            right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            min-width: 280px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            color: #333;
        }}
        
        .controls-content h3 {{
            margin: 0 0 1rem 0;
            font-size: 1.2em;
            color: #333;
            border-bottom: 2px solid #ddd;
            padding-bottom: 0.5rem;
        }}
        
        .control-group {{
            margin-bottom: 1rem;
        }}
        
        .control-group label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
            color: #555;
            font-size: 0.9em;
        }}
        
        .control-group select {{
            width: 100%;
            padding: 0.5rem;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            background: white;
            cursor: pointer;
            transition: border-color 0.2s;
        }}
        
        .control-group select:hover {{
            border-color: {color_scheme.accent};
        }}
        
        .control-group select:focus {{
            outline: none;
            border-color: {color_scheme.accent};
            box-shadow: 0 0 0 3px rgba(70, 130, 180, 0.1);
        }}
        
        @media (max-width: 600px) {{
            header h1 {{
                font-size: 2em;
            }}
            
            .temp-value {{
                font-size: 3em;
            }}
            
            .weather-icon,
            .thermometer {{
                width: 120px;
                height: auto;
            }}
            
            .details {{
                grid-template-columns: 1fr;
            }}
            
            .controls-panel {{
                top: 10px;
                right: 10px;
            }}
            
            .controls-content {{
                right: -10px;
                min-width: 250px;
            }}
        }}
        """

        return css

    def _convert_temperature(self, temp_celsius: float) -> float:
        """
        Convierte temperatura a la unidad seleccionada.

        Args:
            temp_celsius: Temperatura en Celsius

        Returns:
            Temperatura en la unidad seleccionada
        """
        if self.temp_unit == "fahrenheit":
            return (temp_celsius * 9 / 5) + 32
        return temp_celsius

    def _format_timestamp(self, dt: datetime) -> str:
        """
        Formatea el timestamp según el idioma.

        Args:
            dt: Datetime a formatear

        Returns:
            String formateado
        """
        # Formato básico que funciona en todos los idiomas
        # En una implementación completa, se usaría locale para formatear según idioma
        formats = {
            "en": "%B %d, %Y at %I:%M %p",
            "es": "%d de %B de %Y a las %H:%M",
            "fr": "%d %B %Y à %H:%M",
            "it": "%d %B %Y alle %H:%M",
            "de": "%d. %B %Y um %H:%M",
            "zh": "%Y年%m月%d日 %H:%M",
        }

        format_str = formats.get(self.language, "%Y-%m-%d %H:%M")

        try:
            return dt.strftime(format_str)
        except:
            # Fallback a formato ISO si hay problemas
            return dt.strftime("%Y-%m-%d %H:%M")
