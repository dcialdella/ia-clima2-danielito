"""Gestión de configuración del usuario."""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigurationError(Exception):
    """Error en archivo de configuración."""
    pass


class ConfigManager:
    """Gestiona la persistencia de preferencias del usuario."""
    
    def __init__(self, config_path: str = None):
        """
        Inicializa el ConfigManager.
        
        Args:
            config_path: Ruta al archivo de configuración. Si es None, usa ~/.weather-display-config.json
        """
        if config_path is None:
            self.config_path = Path.home() / ".weather-display-config.json"
        else:
            self.config_path = Path(config_path)
    
    def get_default_config(self) -> Dict[str, Any]:
        """
        Retorna la configuración por defecto.
        
        Returns:
            Diccionario con valores por defecto
        """
        return {
            "language": "en",
            "temp_unit": "celsius",
            "font_size": "m",
            "last_city": None,
            "api_keys": {
                "openweathermap": ""
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """
        Carga la configuración desde el archivo.
        
        Returns:
            Diccionario con la configuración
            
        Raises:
            ConfigurationError: Si el archivo está corrupto
        """
        # Si el archivo no existe, retornar configuración por defecto
        if not self.config_path.exists():
            return self.get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validar que sea un diccionario
            if not isinstance(config, dict):
                raise ConfigurationError("Configuration file is not a valid JSON object")
            
            # Merge con valores por defecto para asegurar que existan todas las claves
            default_config = self.get_default_config()
            default_config.update(config)
            
            return default_config
            
        except json.JSONDecodeError as e:
            # Archivo corrupto - hacer backup y retornar configuración por defecto
            backup_path = self.config_path.with_suffix('.json.backup')
            if self.config_path.exists():
                self.config_path.rename(backup_path)
            raise ConfigurationError(f"Configuration file is corrupted: {e}")
        except PermissionError:
            raise ConfigurationError(f"Permission denied reading configuration file: {self.config_path}")
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Guarda la configuración en el archivo.
        
        Args:
            config: Diccionario con la configuración a guardar
            
        Raises:
            ConfigurationError: Si no se puede escribir el archivo
        """
        try:
            # Crear directorio si no existe
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo con formato legible
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Establecer permisos restrictivos (solo lectura/escritura para el usuario)
            if os.name != 'nt':  # Unix-like systems
                os.chmod(self.config_path, 0o600)
                
        except PermissionError:
            raise ConfigurationError(f"Permission denied writing configuration file: {self.config_path}")
        except Exception as e:
            raise ConfigurationError(f"Error saving configuration: {e}")
