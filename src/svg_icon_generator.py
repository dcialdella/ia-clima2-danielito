"""Generador de iconos SVG inline para condiciones climáticas."""

from src.models import WeatherConditionType


class SVGIconGenerator:
    """Genera iconos SVG inline para las 8 condiciones climáticas."""
    
    def generate_icon(self, condition: WeatherConditionType) -> str:
        """
        Genera un icono SVG para la condición climática especificada.
        
        Args:
            condition: Tipo de condición climática
            
        Returns:
            String con el código SVG inline
        """
        generators = {
            WeatherConditionType.SUNNY: self._generate_sunny,
            WeatherConditionType.PARTLY_CLOUDY: self._generate_partly_cloudy,
            WeatherConditionType.VERY_CLOUDY: self._generate_very_cloudy,
            WeatherConditionType.OVERCAST: self._generate_overcast,
            WeatherConditionType.LIGHT_RAIN: self._generate_light_rain,
            WeatherConditionType.HEAVY_RAIN: self._generate_heavy_rain,
            WeatherConditionType.SNOW: self._generate_snow,
            WeatherConditionType.MIST: self._generate_mist,
        }
        
        generator = generators.get(condition, self._generate_partly_cloudy)
        return generator()
    
    def _generate_sunny(self) -> str:
        """Genera icono de sol."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="20" fill="#FFD700"/>
            <line x1="50" y1="10" x2="50" y2="25" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="50" y1="75" x2="50" y2="90" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="10" y1="50" x2="25" y2="50" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="75" y1="50" x2="90" y2="50" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="21" y1="21" x2="32" y2="32" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="68" y1="68" x2="79" y2="79" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="79" y1="21" x2="68" y2="32" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
            <line x1="32" y1="68" x2="21" y2="79" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
        </svg>'''
    
    def _generate_partly_cloudy(self) -> str:
        """Genera icono de parcialmente nublado."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="35" cy="35" r="15" fill="#FFD700"/>
            <line x1="35" y1="10" x2="35" y2="20" stroke="#FFD700" stroke-width="2" stroke-linecap="round"/>
            <line x1="10" y1="35" x2="20" y2="35" stroke="#FFD700" stroke-width="2" stroke-linecap="round"/>
            <line x1="15" y1="15" x2="23" y2="23" stroke="#FFD700" stroke-width="2" stroke-linecap="round"/>
            <line x1="55" y1="15" x2="47" y2="23" stroke="#FFD700" stroke-width="2" stroke-linecap="round"/>
            <ellipse cx="60" cy="65" rx="25" ry="18" fill="#FFFFFF" stroke="#B0C4DE" stroke-width="2"/>
            <ellipse cx="45" cy="70" rx="20" ry="15" fill="#FFFFFF" stroke="#B0C4DE" stroke-width="2"/>
            <ellipse cx="75" cy="70" rx="20" ry="15" fill="#FFFFFF" stroke="#B0C4DE" stroke-width="2"/>
        </svg>'''
    
    def _generate_very_cloudy(self) -> str:
        """Genera icono de muy nublado."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="40" cy="45" rx="25" ry="18" fill="#D3D3D3" stroke="#A9A9A9" stroke-width="2"/>
            <ellipse cx="25" cy="50" rx="20" ry="15" fill="#D3D3D3" stroke="#A9A9A9" stroke-width="2"/>
            <ellipse cx="55" cy="50" rx="20" ry="15" fill="#D3D3D3" stroke="#A9A9A9" stroke-width="2"/>
            <ellipse cx="60" cy="65" rx="25" ry="18" fill="#E8E8E8" stroke="#B0C4DE" stroke-width="2"/>
            <ellipse cx="45" cy="70" rx="20" ry="15" fill="#E8E8E8" stroke="#B0C4DE" stroke-width="2"/>
            <ellipse cx="75" cy="70" rx="20" ry="15" fill="#E8E8E8" stroke="#B0C4DE" stroke-width="2"/>
        </svg>'''
    
    def _generate_overcast(self) -> str:
        """Genera icono de totalmente nublado."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="35" cy="35" rx="25" ry="18" fill="#A9A9A9" stroke="#808080" stroke-width="2"/>
            <ellipse cx="20" cy="40" rx="20" ry="15" fill="#A9A9A9" stroke="#808080" stroke-width="2"/>
            <ellipse cx="50" cy="40" rx="20" ry="15" fill="#A9A9A9" stroke="#808080" stroke-width="2"/>
            <ellipse cx="50" cy="55" rx="25" ry="18" fill="#B0B0B0" stroke="#909090" stroke-width="2"/>
            <ellipse cx="35" cy="60" rx="20" ry="15" fill="#B0B0B0" stroke="#909090" stroke-width="2"/>
            <ellipse cx="65" cy="60" rx="20" ry="15" fill="#B0B0B0" stroke="#909090" stroke-width="2"/>
            <ellipse cx="60" cy="70" rx="25" ry="18" fill="#C0C0C0" stroke="#A0A0A0" stroke-width="2"/>
            <ellipse cx="45" cy="75" rx="20" ry="15" fill="#C0C0C0" stroke="#A0A0A0" stroke-width="2"/>
            <ellipse cx="75" cy="75" rx="20" ry="15" fill="#C0C0C0" stroke="#A0A0A0" stroke-width="2"/>
        </svg>'''
    
    def _generate_light_rain(self) -> str:
        """Genera icono de lluvia leve."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="50" cy="35" rx="25" ry="18" fill="#B0C4DE" stroke="#4682B4" stroke-width="2"/>
            <ellipse cx="35" cy="40" rx="20" ry="15" fill="#B0C4DE" stroke="#4682B4" stroke-width="2"/>
            <ellipse cx="65" cy="40" rx="20" ry="15" fill="#B0C4DE" stroke="#4682B4" stroke-width="2"/>
            <line x1="35" y1="55" x2="32" y2="70" stroke="#4682B4" stroke-width="2" stroke-linecap="round"/>
            <line x1="50" y1="55" x2="47" y2="70" stroke="#4682B4" stroke-width="2" stroke-linecap="round"/>
            <line x1="65" y1="55" x2="62" y2="70" stroke="#4682B4" stroke-width="2" stroke-linecap="round"/>
            <line x1="42" y1="60" x2="39" y2="75" stroke="#4682B4" stroke-width="2" stroke-linecap="round"/>
            <line x1="57" y1="60" x2="54" y2="75" stroke="#4682B4" stroke-width="2" stroke-linecap="round"/>
        </svg>'''
    
    def _generate_heavy_rain(self) -> str:
        """Genera icono de lluvia fuerte."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="50" cy="30" rx="25" ry="18" fill="#4682B4" stroke="#191970" stroke-width="2"/>
            <ellipse cx="35" cy="35" rx="20" ry="15" fill="#4682B4" stroke="#191970" stroke-width="2"/>
            <ellipse cx="65" cy="35" rx="20" ry="15" fill="#4682B4" stroke="#191970" stroke-width="2"/>
            <line x1="30" y1="50" x2="27" y2="70" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="40" y1="50" x2="37" y2="70" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="50" y1="50" x2="47" y2="70" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="60" y1="50" x2="57" y2="70" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="70" y1="50" x2="67" y2="70" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="35" y1="55" x2="32" y2="75" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="45" y1="55" x2="42" y2="75" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="55" y1="55" x2="52" y2="75" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
            <line x1="65" y1="55" x2="62" y2="75" stroke="#1E90FF" stroke-width="3" stroke-linecap="round"/>
        </svg>'''
    
    def _generate_snow(self) -> str:
        """Genera icono de nieve."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="50" cy="35" rx="25" ry="18" fill="#E0E0E0" stroke="#B0C4DE" stroke-width="2"/>
            <ellipse cx="35" cy="40" rx="20" ry="15" fill="#E0E0E0" stroke="#B0C4DE" stroke-width="2"/>
            <ellipse cx="65" cy="40" rx="20" ry="15" fill="#E0E0E0" stroke="#B0C4DE" stroke-width="2"/>
            <g fill="#B0E0E6">
                <circle cx="35" cy="60" r="3"/>
                <circle cx="50" cy="65" r="3"/>
                <circle cx="65" cy="60" r="3"/>
                <circle cx="42" cy="70" r="3"/>
                <circle cx="58" cy="70" r="3"/>
                <circle cx="35" cy="80" r="3"/>
                <circle cx="50" cy="80" r="3"/>
                <circle cx="65" cy="80" r="3"/>
            </g>
        </svg>'''
    
    def _generate_mist(self) -> str:
        """Genera icono de bruma."""
        return '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <line x1="20" y1="30" x2="80" y2="30" stroke="#D3D3D3" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
            <line x1="15" y1="40" x2="85" y2="40" stroke="#D3D3D3" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
            <line x1="20" y1="50" x2="80" y2="50" stroke="#D3D3D3" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
            <line x1="15" y1="60" x2="85" y2="60" stroke="#D3D3D3" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
            <line x1="20" y1="70" x2="80" y2="70" stroke="#D3D3D3" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
        </svg>'''
