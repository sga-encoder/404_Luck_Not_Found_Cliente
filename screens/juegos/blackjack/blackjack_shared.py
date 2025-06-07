"""
Módulo compartido para el estado del BlackJack
Evita importaciones circulares entre pantallas
"""
import gc
import threading
import time

# Variable global para compartir estado entre módulos
_game_state = None

def set_game_state(blackjack_instance, jugador_usuario, sala_id=None):
    """Establece el estado del juego compartido"""
    global _game_state
    if sala_id is not None:
        _game_state = (blackjack_instance, jugador_usuario, sala_id)
    else:
        _game_state = (blackjack_instance, jugador_usuario)
    print(f"🔧 Estado guardado: {type(_game_state)} con {len(_game_state)} elementos")

def get_game_state():
    """Obtiene el estado del juego compartido"""
    global _game_state
    print(f"🔍 Obteniendo estado: {type(_game_state)}")
    return _game_state

def clear_game_state():
    """Limpia el estado del juego compartido"""
    global _game_state
    _game_state = None
    print("🧹 Estado limpiado")

def get_sala_id():
    """Obtiene solo el ID de la sala"""
    global _game_state
    if _game_state and isinstance(_game_state, (tuple, list)) and len(_game_state) >= 3:
        return _game_state[2]
    return None
