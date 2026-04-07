"""Interfaz de línea de comandos para Weather HTML Display."""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

from src.config_manager import ConfigManager, ConfigurationError
from src.weather_api_client import (
    WeatherAPIClient,
    CityNotFoundError,
    WeatherServiceUnavailableError,
    InvalidAPIKeyError
)
from src.html_generator import HTMLGenerator, HTMLGenerationError
from src.translations import get_translation


def setup_logging():
    """Configura el sistema de logging."""
    log_file = Path.home() / ".weather-display.log"
    
    # Crear logger
    logger = logging.getLogger("weather_display")
    logger.setLevel(logging.INFO)
    
    # Handler con rotación (mantener últimos 7 días, ~1MB por archivo)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=1024*1024,  # 1MB
        backupCount=7
    )
    
    # Formato
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.
    
    Returns:
        Namespace con los argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description="Genera páginas HTML con información meteorológica"
    )
    
    parser.add_argument(
        "--city",
        type=str,
        help="Nombre de la ciudad"
    )
    
    parser.add_argument(
        "--language",
        type=str,
        choices=["en", "fr", "it", "es", "zh", "de"],
        help="Idioma de la interfaz"
    )
    
    parser.add_argument(
        "--temp-unit",
        type=str,
        choices=["celsius", "fahrenheit"],
        help="Unidad de temperatura"
    )
    
    parser.add_argument(
        "--font-size",
        type=str,
        choices=["xs", "s", "m", "l", "xl"],
        help="Tamaño de fuente"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Ruta del archivo HTML de salida"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key de OpenWeatherMap"
    )
    
    return parser.parse_args()


def main():
    """
    Función principal del CLI.
    
    Returns:
        Código de salida (0 = éxito, 1 = error)
    """
    # Configurar logging
    logger = setup_logging()
    
    try:
        # Parsear argumentos
        args = parse_arguments()
        
        # Cargar configuración
        config_manager = ConfigManager()
        try:
            config = config_manager.load_config()
        except ConfigurationError as e:
            logger.error(f"Configuration error: {e}")
            config = config_manager.get_default_config()
        
        # Actualizar configuración con argumentos de línea de comandos
        if args.language:
            config["language"] = args.language
        if args.temp_unit:
            config["temp_unit"] = args.temp_unit
        if args.font_size:
            config["font_size"] = args.font_size
        if args.api_key:
            config["api_keys"]["openweathermap"] = args.api_key
        
        # Determinar ciudad
        city = args.city
        if not city:
            city = config.get("last_city")
        
        if not city:
            # Solicitar ciudad interactivamente
            city = input("Enter city name: ").strip()
            if not city:
                print("Error: City name is required")
                logger.error("No city name provided")
                return 1
        
        # Actualizar última ciudad en configuración
        config["last_city"] = city
        
        # Guardar configuración actualizada
        try:
            config_manager.save_config(config)
        except ConfigurationError as e:
            logger.warning(f"Could not save configuration: {e}")
        
        # Obtener datos meteorológicos
        logger.info(f"Fetching weather data for {city}")
        api_key = config["api_keys"].get("openweathermap", "")
        client = WeatherAPIClient(api_key)
        
        try:
            weather_data = client.get_weather_data(city, config["language"])
            logger.info(f"Successfully retrieved data from {weather_data.source}")
        except CityNotFoundError:
            error_msg = get_translation(config["language"], "city_not_found", city=city)
            print(f"Error: {error_msg}")
            logger.error(f"City not found: {city}")
            return 1
        except InvalidAPIKeyError:
            error_msg = get_translation(config["language"], "invalid_api_key")
            print(f"Error: {error_msg}")
            logger.error("Invalid API key")
            return 1
        except WeatherServiceUnavailableError:
            error_msg = get_translation(config["language"], "service_unavailable")
            print(f"Error: {error_msg}")
            logger.error("All weather services unavailable")
            return 1
        
        # Generar HTML
        logger.info("Generating HTML")
        generator = HTMLGenerator(
            config["language"],
            config["temp_unit"],
            config["font_size"]
        )
        
        try:
            html_content = generator.generate_html(weather_data, city)
        except HTMLGenerationError as e:
            error_msg = get_translation(config["language"], "html_generation_error", error=str(e))
            print(f"Error: {error_msg}")
            logger.error(f"HTML generation error: {e}")
            return 1
        
        # Determinar ruta de salida
        if args.output:
            output_path = Path(args.output)
        else:
            # Generar nombre de archivo con ciudad y timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            city_safe = "".join(c if c.isalnum() else "_" for c in city.lower())
            filename = f"weather_{city_safe}_{timestamp}.html"
            output_path = Path.cwd() / filename
        
        # Guardar archivo HTML
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML file generated: {output_path.absolute()}")
            logger.info(f"Generated HTML file: {output_path.absolute()}")
            
        except Exception as e:
            print(f"Error saving HTML file: {e}")
            logger.error(f"Error saving HTML file: {e}")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
