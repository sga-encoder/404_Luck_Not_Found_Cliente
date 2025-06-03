# Módulo de formularios del Casino Virtual

from .login import *
from .login_firestore_form import *
from .login_with_print_form import *
from .register_form import *

__all__ = [
    'login',
    'login_firestore_form',
    'login_with_print_form', 
    'register_form'
]