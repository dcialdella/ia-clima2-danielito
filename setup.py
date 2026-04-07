"""Setup configuration for Weather HTML Display."""

from setuptools import setup, find_packages

setup(
    name="weather-html-display",
    version="1.0.0",
    description="Sistema que obtiene datos meteorológicos y genera páginas HTML autónomas",
    author="Weather Display Team",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "weather-display=src.cli:main",
        ],
    },
)
