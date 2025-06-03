"""
Módulo principal del cliente para el Casino Virtual
"""

__version__ = "0.1.0"
__description__ = "Cliente del Casino Virtual 404 Luck Not Found"
__author__ = "sga-encoder"

# Importar módulos principales
from . import screens
from . import utils

# Exportar símbolos principales
__all__ = [
    'screens',
    'utils'
]