"""
Pantallas del cliente para el Casino Virtual
"""

# Importar pantallas principales
from .inicio import inicio, main as inicio_main
from .home import home

# Importar submódulos
from . import forms
from . import juegos

# Exportar todo
__all__ = [
    "inicio",
    "inicio_main",
    "home",
    "forms",
    "juegos"
]