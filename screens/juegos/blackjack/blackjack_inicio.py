from ....utils.events import add_key_listener
from ....utils.printers import print_text, print_button
from asciimatics.screen import Screen
import pyfiglet
import random
from ....utils.async_wrapper import AsyncScreenManager

# Importar el módulo compartido para evitar importación circular
from . import blackjack_shared

# Importar DIRECTAMENTE el BlackJack
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../servidor'))
from servidor.src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
from servidor.src.model.usuario.Usuario import Usuario
from servidor.src.model.salaDeJuego.SalaDeJuegoServicio import SalaDeJuegoServicio

def blackjack_inicio(screen):
    screen.clear()
    screen.mouse = True 
    
    # Usar AsyncScreenManager para manejar asyncio
    async_manager = AsyncScreenManager()
    
    # Estado de la pantalla
    estado = {"creando_sala": False, "error": None, "sala_creada": False, "sala_id": None}
    
    text = {
        'text': 'BlackJack',
        'x-center': -10,
        'y-center': -5,
        'font': 'big_money-ne',
        'justify': 'center',
        'max-width': 130,
    }
    
    boton_iniciar = {
        'text': '[ INICIAR JUEGO ]',
        'x-center': 0,
        'y-center': 5,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_RED,
    }
    
    def ejecutar_asyncio(coro):
        """Ejecuta una corrutina de forma síncrona usando AsyncScreenManager"""
        try:
            return async_manager.run_async(coro)
        except Exception as e:
            print(f"Error en asyncio: {e}")
            return None
    
    async def crear_sala_firestore(blackjack_instance, usuario):
        """Crea la sala activa en Firestore"""
        try:
            servicio = SalaDeJuegoServicio()
            
            # Preparar datos de la sala
            datos_sala = {
                'tipo_juego': 'BlackJack',
                'capacidad': 4,
                'capacidad_minima': 1,
                'jugadores': [usuario.get_id()],
                'estado': 'activa',
                'valor_entrada_mesa': 100,
                'apuestas': {},
                'historial': [],
                'fecha_hora_inicio': str(blackjack_instance._fechaHoraInicio),
                'creador': usuario.get_id(),
                'manos_inicializadas': False
            }
            
            # Crear sala en Firestore
            sala_id = await servicio.crear_sala_de_juego_activa(datos_sala)
            print(f"🎮 Sala BlackJack creada en Firestore: {sala_id}")
            return sala_id
            
        except Exception as e:
            print(f"❌ Error creando sala en Firestore: {e}")
            return None

    def crear_sala():
        """Crear nueva sala ACTIVA usando BlackJack con Firestore"""
        estado["creando_sala"] = True
        estado["error"] = None
        
        try:
            # Crear usuario
            jugador_actual = Usuario(
                id="",                       # ID vacío = se genera automáticamente
                nombre="Jugador1",           
                apellido="Test",             
                correo="jugador1@email.com",
                contraseña="1234",
                saldo=1000.0
            )
            
            print(f"🧑 Usuario creado con ID: {jugador_actual.get_id()}")
            
            # Crear BlackJack DIRECTAMENTE
            blackjack_instance = BlackJack(
                jugador=jugador_actual.get_id(),
                capacidad=4, 
                capacidadMinima=1, 
                valor_entrada_mesa=100,
                _plantarse=False,
                _apuesta=10
            )
            
            print(f"🃏 BlackJack creado")
            
            # Guardar en el módulo compartido
            blackjack_shared.set_game_state(blackjack_instance, jugador_actual)
            
            # Crear sala activa en Firestore
            print("🚀 Creando sala activa en Firestore...")
            sala_id = ejecutar_asyncio(crear_sala_firestore(blackjack_instance, jugador_actual))
            
            if sala_id:
                print(f"✅ Sala creada exitosamente: {sala_id}")
                estado["sala_creada"] = True
                estado["sala_id"] = sala_id
                
                # ACTUALIZAR con el sala_id
                blackjack_shared.set_game_state(blackjack_instance, jugador_actual, sala_id)
                
                # Cerrar async_manager antes de pasar a otra pantalla
                async_manager.close()
                
                # Importar y llamar directamente a blackjack_juego
                from .blackjack_juego import blackjack_juego
                return blackjack_juego(screen)
            else:
                estado["error"] = "❌ Error creando sala activa en Firestore"
                return None
                
        except Exception as e:
            estado["error"] = f"❌ Error: {str(e)}"
            print(f"Error completo: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            estado["creando_sala"] = False

    try:
        while True:
            screen.refresh()
            print_text(screen, text, True)
            
            # Mostrar estado
            if estado["creando_sala"]:
                estado_text = {
                    'text': '⏳ Creando sala de juego en Firestore...',
                    'x-center': 0,
                    'y-center': 10,
                    'color': Screen.COLOUR_YELLOW,
                }
                print_text(screen, estado_text)
            
            if estado["sala_creada"] and estado["sala_id"]:
                exito_text = {
                    'text': f'✅ Sala creada: {estado["sala_id"]}',
                    'x-center': 0,
                    'y-center': 10,
                    'color': Screen.COLOUR_GREEN,
                }
                print_text(screen, exito_text)
            
            if estado["error"]:
                error_text = {
                    'text': estado["error"],
                    'x-center': 0,
                    'y-center': 12,
                    'color': Screen.COLOUR_RED,
                }
                print_text(screen, error_text)
            
            # Instrucciones
            instrucciones = {
                'text': 'Presiona F para salir',
                'x-center': 0,
                'y-center': 15,
                'color': Screen.COLOUR_CYAN,
            }
            print_text(screen, instrucciones)
            
            event = screen.get_event()
            
            # Botón iniciar (solo si no está creando sala)
            if not estado["creando_sala"]:
                button_inicio = print_button(
                    screen,
                    boton_iniciar,
                    event,
                    click=crear_sala
                )
                
                # Si crear_sala retorna algo (la pantalla de juego), lo retornamos
                if button_inicio['result']:
                    return button_inicio['result']
            
            # Tecla para salir
            salir = add_key_listener(ord('f'), event, lambda: 'salir')
            if salir == 'salir':
                # Limpiar estado al salir
                blackjack_shared.clear_game_state()
                async_manager.close()
                return 'salir'
    
    except KeyboardInterrupt:
        print("🛑 Pantalla interrumpida por el usuario")
        blackjack_shared.clear_game_state()
        async_manager.close()
        return 'salir'
    except Exception as e:
        print(f"❌ Error inesperado en blackjack_inicio: {e}")
        blackjack_shared.clear_game_state()
        async_manager.close()
        return 'salir'
    finally:
        # Asegurar que el async manager se cierre
        async_manager.close()
