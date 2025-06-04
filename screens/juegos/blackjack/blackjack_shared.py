"""
Módulo compartido para el estado del BlackJack
Evita importaciones circulares entre pantallas
"""

# Estado global compartido
_blackjack_instance = None
_jugador_actual = None

def set_game_state(blackjack_instance, jugador_actual):
    """Establecer el estado global del juego"""
    global _blackjack_instance, _jugador_actual
    _blackjack_instance = blackjack_instance
    _jugador_actual = jugador_actual
    print(f"✅ Estado guardado: BlackJack={blackjack_instance is not None}, Jugador={jugador_actual is not None}")

def get_game_state():
    """Obtener el estado global del juego"""
    global _blackjack_instance, _jugador_actual
    print(f"📋 Obteniendo estado: BlackJack={_blackjack_instance is not None}, Jugador={_jugador_actual is not None}")
    return _blackjack_instance, _jugador_actual

def clear_game_state():
    """Limpiar el estado global del juego"""
    global _blackjack_instance, _jugador_actual
    print("🧹 Limpiando estado del juego")
    _blackjack_instance = None
    _jugador_actual = None
