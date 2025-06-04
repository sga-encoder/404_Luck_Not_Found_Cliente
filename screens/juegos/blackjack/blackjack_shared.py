"""
Módulo compartido para el estado del BlackJack
Evita importaciones circulares entre pantallas
"""
import gc
import threading
import time

# Estado global compartido
_blackjack_instance = None
_jugador_actual = None

def set_game_state(blackjack_instance, jugador_actual):
    """Establecer el estado global del juego"""
    global _blackjack_instance, _jugador_actual
    _blackjack_instance = blackjack_instance
    _jugador_actual = jugador_actual

def get_game_state():
    """Obtener el estado global del juego"""
    return _blackjack_instance, _jugador_actual

def clear_game_state():
    """Limpiar el estado global del juego - VERSIÓN MEJORADA para gRPC"""
    global _blackjack_instance, _jugador_actual
    
    print("🧹 Limpiando estado del juego (gRPC-safe)")
    
    # Finalizar el juego si existe
    if _blackjack_instance:
        try:
            print("🏁 Finalizando instancia de BlackJack...")
            _blackjack_instance.finalizar_juego()
            
            # Esperar un momento para que se complete la limpieza
            time.sleep(0.5)
            
        except Exception as e:
            print(f"⚠️ Error finalizando juego: {e}")
    
    # Limpiar referencias
    _blackjack_instance = None
    _jugador_actual = None
    
    # Forzar garbage collection para limpiar conexiones gRPC
    print("🗑️ Ejecutando garbage collection...")
    gc.collect()
    
    print("✅ Estado limpiado (gRPC-safe)")
