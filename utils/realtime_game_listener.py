# -*- coding: utf-8 -*-
"""
Utilidad para manejar listeners de juego en tiempo real desde el cliente.
Este módulo actúa como intermediario entre el cliente y los listeners del servidor.
"""

import sys
import os

# Agregar la ruta del servidor
sys.path.append(os.path.join(os.path.dirname(__file__), '../../servidor/src'))

from model.salaDeJuego.SalaDeJuegoServicio import SalaDeJuegoServicio
from model.salaDeJuego.SalaDeJuego import SalaDeJuego

class RealtimeGameListener:
    """
    Clase para manejar listeners de juego en tiempo real desde el cliente.
    """
    
    def __init__(self):
        self.servicio_sala = SalaDeJuegoServicio()
        self.listeners_activos = {}  # Para llevar registro de listeners activos
    
    def escuchar_sala_especifica(self, sala_id: str, callback_personalizado=None):
        """
        Inicia un listener para una sala específica.
        
        Args:
            sala_id (str): ID de la sala a escuchar
            callback_personalizado (Callable, optional): Función personalizada para manejar cambios
        
        Returns:
            str: ID del listener para poder detenerlo después
        """
        
        def callback_por_defecto(datos_sala, changes, read_time):
            """Callback por defecto optimizado para el cliente"""
            if datos_sala:
                print(f"🎮 [CLIENTE] Cambio en sala {sala_id}:")
                print(f"   - Jugadores activos: {len(datos_sala.get('jugadores', []))}")
                print(f"   - Estado del juego: {datos_sala.get('estado', 'desconocido')}")
                
                # Datos específicos según el tipo de juego
                tipo_juego = datos_sala.get('tipo_juego', '')
                
                if tipo_juego == 'BlackJack':
                    manos = datos_sala.get('manos_jugadores', {})
                    mano_crupier = datos_sala.get('mano_crupier', [])
                    print(f"   - Manos de jugadores: {len(manos)} jugadores")
                    print(f"   - Cartas del crupier: {len(mano_crupier)} cartas")
                
                elif tipo_juego == 'KnuckleBones':
                    mesa = datos_sala.get('mesa', {})
                    turno = datos_sala.get('turno_actual', 0)
                    print(f"   - Estado de la mesa: {bool(mesa)}")
                    print(f"   - Turno actual: Jugador {turno}")
                
                # Datos generales
                apuestas = datos_sala.get('apuestas', {})
                historial = datos_sala.get('historial', [])
                print(f"   - Apuestas activas: {len(apuestas)}")
                print(f"   - Eventos en historial: {len(historial)}")
                
            else:
                print(f"❌ [CLIENTE] Sala {sala_id} no disponible")
        
        # Usar callback personalizado o el por defecto
        callback_final = callback_personalizado if callback_personalizado else callback_por_defecto
        
        print(f"🎧 [CLIENTE] Iniciando escucha de sala {sala_id}...")
        
        # Iniciar listener a través del servicio
        unsubscribe_func = self.servicio_sala.iniciar_listener_sala_especifica(
            sala_id=sala_id,
            callback=callback_final
        )
        
        # Guardar referencia para poder detenerlo
        listener_id = f"sala_{sala_id}"
        self.listeners_activos[listener_id] = unsubscribe_func
        
        return listener_id
    
    def escuchar_todas_las_salas(self, tipo_juego=None, callback_personalizado=None):
        """
        Inicia un listener para todas las salas activas.
        
        Args:
            tipo_juego (str, optional): Filtrar por tipo de juego específico
            callback_personalizado (Callable, optional): Función personalizada para manejar cambios
        
        Returns:
            str: ID del listener para poder detenerlo después
        """
        
        def callback_por_defecto(salas_activas, changes, read_time):
            """Callback por defecto para todas las salas"""
            print(f"🏠 [CLIENTE] Cambios en salas activas:")
            print(f"   - Total salas activas: {len(salas_activas)}")
            
            for sala in salas_activas:
                if sala:
                    sala_id = sala.get('id', 'desconocido')
                    tipo = sala.get('tipo_juego', 'desconocido')
                    jugadores = len(sala.get('jugadores', []))
                    estado = sala.get('estado', 'desconocido')
                    
                    print(f"   📋 Sala {sala_id} ({tipo}): {jugadores} jugadores, estado: {estado}")
        
        # Usar callback personalizado o el por defecto
        callback_final = callback_personalizado if callback_personalizado else callback_por_defecto
        
        # Aplicar filtros si se especifica tipo de juego
        filtros = {'tipo_juego': tipo_juego} if tipo_juego else None
        
        print(f"🎧 [CLIENTE] Iniciando escucha de todas las salas...")
        if tipo_juego:
            print(f"   🔍 Filtrado por tipo: {tipo_juego}")
        
        # Iniciar listener a través del servicio
        unsubscribe_func = self.servicio_sala.iniciar_listener_salas_activas(
            callback=callback_final,
            filtros=filtros
        )
        
        # Guardar referencia para poder detenerlo
        listener_id = f"todas_salas_{tipo_juego if tipo_juego else 'todas'}"
        self.listeners_activos[listener_id] = unsubscribe_func
        
        return listener_id
    
    def detener_listener(self, listener_id: str):
        """
        Detiene un listener específico.
        
        Args:
            listener_id (str): ID del listener a detener
        
        Returns:
            bool: True si se detuvo correctamente, False si no se encontró
        """
        if listener_id in self.listeners_activos:
            unsubscribe_func = self.listeners_activos[listener_id]
            try:
                unsubscribe_func()  # Llamar función de unsubscribe
                del self.listeners_activos[listener_id]
                print(f"🔇 [CLIENTE] Listener {listener_id} detenido correctamente")
                return True
            except Exception as e:
                print(f"❌ [CLIENTE] Error al detener listener {listener_id}: {e}")
                return False
        else:
            print(f"⚠️ [CLIENTE] Listener {listener_id} no encontrado")
            return False
    
    def detener_todos_los_listeners(self):
        """
        Detiene todos los listeners activos.
        
        Returns:
            int: Número de listeners detenidos
        """
        listeners_detenidos = 0
        
        for listener_id in list(self.listeners_activos.keys()):
            if self.detener_listener(listener_id):
                listeners_detenidos += 1
        
        print(f"🔇 [CLIENTE] Total listeners detenidos: {listeners_detenidos}")
        return listeners_detenidos
    
    def obtener_listeners_activos(self):
        """
        Obtiene la lista de listeners actualmente activos.
        
        Returns:
            list: Lista de IDs de listeners activos
        """
        return list(self.listeners_activos.keys())


# Función de conveniencia para uso rápido
def crear_listener_juego():
    """
    Función de conveniencia para crear rápidamente un listener de juego.
    
    Returns:
        RealtimeGameListener: Instancia del listener listo para usar
    """
    return RealtimeGameListener()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear listener
    game_listener = crear_listener_juego()
    
    # Ejemplo 1: Escuchar una sala específica
    def mi_callback_sala(datos_sala, changes, read_time):
        print(f"¡Mi callback personalizado! Sala actualizada: {datos_sala.get('id', 'N/A')}")
    
    # listener_id = game_listener.escuchar_sala_especifica("SALA123", mi_callback_sala)
    
    # Ejemplo 2: Escuchar todas las salas de BlackJack
    def mi_callback_blackjack(salas, changes, read_time):
        print(f"¡Cambios en salas de BlackJack! Total: {len(salas)}")
    
    # listener_id2 = game_listener.escuchar_todas_las_salas("BlackJack", mi_callback_blackjack)
    
    # Para detener listeners:
    # game_listener.detener_listener(listener_id)
    # game_listener.detener_todos_los_listeners()
    
    print("🎮 Ejemplo de uso disponible en el código")
