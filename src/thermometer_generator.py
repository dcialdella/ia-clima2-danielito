"""Generador de termómetro vintage SVG inline."""


class ThermometerGenerator:
    """Genera termómetro vintage SVG inline."""
    
    def generate_thermometer(self, temp: float, unit: str, min_temp: float = None, max_temp: float = None) -> str:
        """
        Genera un termómetro vintage SVG.
        
        Args:
            temp: Temperatura actual
            unit: Unidad de temperatura ("celsius" o "fahrenheit")
            min_temp: Temperatura mínima de la escala (opcional)
            max_temp: Temperatura máxima de la escala (opcional)
            
        Returns:
            String con el código SVG inline
        """
        # Establecer rangos por defecto según unidad
        if unit == "fahrenheit":
            if min_temp is None:
                min_temp = -22  # -30°C en Fahrenheit
            if max_temp is None:
                max_temp = 122  # 50°C en Fahrenheit
            unit_symbol = "°F"
        else:  # celsius
            if min_temp is None:
                min_temp = -30
            if max_temp is None:
                max_temp = 50
            unit_symbol = "°C"
        
        # Calcular altura del mercurio (proporción de 0 a 1)
        temp_range = max_temp - min_temp
        temp_normalized = max(0, min(1, (temp - min_temp) / temp_range))
        
        # Dimensiones del termómetro
        tube_height = 200
        tube_width = 30
        bulb_radius = 25
        mercury_height = temp_normalized * tube_height
        
        # Generar marcas de escala cada 10 grados
        scale_marks = []
        for t in range(int(min_temp), int(max_temp) + 1, 10):
            if t < min_temp or t > max_temp:
                continue
            y_pos = tube_height - ((t - min_temp) / temp_range * tube_height)
            scale_marks.append(f'<line x1="45" y1="{y_pos + 20}" x2="55" y2="{y_pos + 20}" stroke="#8B4513" stroke-width="2"/>')
            scale_marks.append(f'<text x="65" y="{y_pos + 25}" font-size="10" fill="#8B4513">{t}{unit_symbol}</text>')
        
        scale_marks_svg = '\n            '.join(scale_marks)
        
        svg = f'''<svg viewBox="0 0 150 280" xmlns="http://www.w3.org/2000/svg">
            <!-- Bulbo del termómetro -->
            <circle cx="50" cy="245" r="{bulb_radius}" fill="#DC143C" stroke="#8B0000" stroke-width="2"/>
            
            <!-- Tubo del termómetro -->
            <rect x="35" y="20" width="{tube_width}" height="{tube_height}" rx="15" fill="#FFFFFF" stroke="#8B4513" stroke-width="3"/>
            
            <!-- Mercurio en el tubo -->
            <rect x="40" y="{20 + tube_height - mercury_height}" width="20" height="{mercury_height}" fill="#DC143C"/>
            
            <!-- Conexión bulbo-tubo -->
            <rect x="40" y="220" width="20" height="25" fill="#DC143C"/>
            
            <!-- Marcas de escala -->
            {scale_marks_svg}
            
            <!-- Decoración vintage -->
            <circle cx="50" cy="245" r="{bulb_radius + 3}" fill="none" stroke="#8B4513" stroke-width="2"/>
            <path d="M 35 20 Q 30 15 35 10" stroke="#8B4513" stroke-width="2" fill="none"/>
            <path d="M 65 20 Q 70 15 65 10" stroke="#8B4513" stroke-width="2" fill="none"/>
            
            <!-- Temperatura actual -->
            <text x="50" y="270" font-size="14" font-weight="bold" fill="#8B4513" text-anchor="middle">{temp:.1f}{unit_symbol}</text>
        </svg>'''
        
        return svg
