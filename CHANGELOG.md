# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.1.0] - 2026-04-05

### Added
- Documentación de análisis de código (`docs/ANALISIS_CODIGO.md`)
- Sección de "Issues Conocidos" en README.md

### Fixed
- Bug crítico: falta import `urllib.parse` en `weather_api_client.py`

### Changed
- README.md actualizado con sección de bugs conocidos

---

## [1.0.0] - 2025-03-06

### Added
- Soporte para 6 idiomas (en, es, fr, it, de, zh)
- Selección de unidades de temperatura (Celsius/Fahrenheit)
- 5 tamaños de fuente ajustables
- Esquemas de color dinámicos según condiciones climáticas
- Failover automático (OpenWeatherMap → Open-Meteo)
- HTML completamente autónomo
- Regeneración automática programable
- 8 iconos SVG para condiciones climáticas
- Termómetro vintage SVG
- CLI interface completa
- Sistema de logging con rotación
- Tests con pytest y hypothesis
