#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Weather HTML Display - Test Generator"
echo "======================================"
echo ""

command -v python3 >/dev/null 2>&1 || { echo "Error: python3 no está instalado"; exit 1; }

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
    echo ""
fi

echo "Activando entorno virtual..."
source venv/bin/activate

if [ ! -f "venv/.deps_installed" ] || [ "requirements-dev.txt" -nt "venv/.deps_installed" ]; then
    echo "Instalando dependencias de desarrollo..."
    pip install -q -r requirements-dev.txt
    touch venv/.deps_installed
    echo "✓ Dependencias instaladas"
    echo ""
fi

echo "Ejecutando generador de prueba..."
echo ""
python test_generate.py

echo ""
if [ -f "weather_madrid_es.html" ]; then
    echo "✓ Archivos HTML generados exitosamente"
    echo ""
    echo "Para ver los archivos, abre cualquiera de estos en tu navegador:"
    for file in weather_*.html; do
        echo "  - $file"
    done
else
    echo "✗ Error: No se generaron los archivos HTML"
    exit 1
fi

deactivate

echo ""
echo "¡Listo! Abre los archivos HTML en tu navegador."
