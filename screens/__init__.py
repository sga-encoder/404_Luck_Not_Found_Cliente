"""
Pantallas del cliente para el Casino Virtual
"""

# Importar pantallas principales
from .home import home

# Importar submódulos
from . import forms
from . import juegos

# Exportar todo
__all__ = [
    "inicio",
    "home",
    "forms",
    "juegos"
]