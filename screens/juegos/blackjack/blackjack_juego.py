from ....utils.events import add_key_listener
from ....utils.printers import print_text, print_button, print_card
from asciimatics.screen import Screen
import pyfiglet
from .cartas import cartas

# Importar del módulo compartido para evitar importación circular
from . import blackjack_shared


def blackjack_juego(screen):
    screen.clear()
    screen.mouse = True
    
    # Obtener las variables del módulo compartido
    blackjack_instance, jugador_actual = blackjack_shared.get_game_state()
    
    # Verificar que tenemos todo lo necesario
    if not blackjack_instance or not jugador_actual:
        error_text = {
            'text': '❌ Error: No se encontró la instancia del juego',
            'x-center': 0,
            'y-center': 0,
            'color': Screen.COLOUR_RED,
        }
        while True:
            screen.refresh()
            print_text(screen, error_text)
            event = screen.get_event()
            salir = add_key_listener(ord('f'), event, lambda: 'salir')
            if salir == 'salir':
                return 'salir'
    
    # Estado del juego
    estado_juego = {
        "mensaje": "🎮 Presiona INICIAR para comenzar la partida",
        "error": None,
        "juego_iniciado": False
    }
    
    mesa = {
        'text': f'🃏 Mesa BlackJack - Sala: {blackjack_instance.sala_activa_id[:8] if blackjack_instance.sala_activa_id else "N/A"}...',
        'x-center': 0,
        'y-center': -20,
        'font': 'elite',
        'justify': 'center',
        'color': Screen.COLOUR_CYAN,
    }

    boton_iniciar = {
        'text': '┌─────────────┐\n'
                '│   INICIAR   │\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 14,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
    }

    boton_pedirCarta = {
        'text': '┌─────────────┐\n'
                '│ PEDIR CARTA │\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 18,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_GREEN,
    }

    boton_plantarse = {
        'text': '┌─────────────┐\n'
                '│  PLANTARSE  │\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 22,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_RED,
    }
    
    boton_nueva_partida = {
        'text': '┌─────────────┐\n'
                '│NUEVA PARTIDA│\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 26,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_YELLOW,
    }
    
    def iniciar_partida():
        """Inicia el juego DIRECTAMENTE en BlackJack"""
        try:
            print("🎮 Iniciando partida...")
            
            # DIRECTO al método de BlackJack
            resultado = blackjack_instance.iniciar_partida_blackjack(jugador_actual.get_id())
            
            print(f"📋 Resultado de iniciar partida: {resultado}")
            
            if resultado.get('success'):
                estado_juego["juego_iniciado"] = True
                estado_juego["mensaje"] = "🎉 ¡Juego iniciado! Cartas repartidas"
                estado_juego["error"] = None
                print("✅ Partida iniciada exitosamente")
            else:
                estado_juego["error"] = f"❌ {resultado.get('error', 'Error al iniciar juego')}"
                print(f"❌ Error iniciando partida: {estado_juego['error']}")
            
            return True
        except Exception as e:
            estado_juego["error"] = f"💥 Error: {str(e)}"
            print(f"💥 Excepción en iniciar_partida: {e}")
            import traceback
            traceback.print_exc()
            return True
    
    def pedir_carta():
        """Pide una carta DIRECTAMENTE en BlackJack"""
        try:
            print("🃏 Pidiendo carta...")
            
            # DIRECTO al método de BlackJack
            resultado = blackjack_instance.pedir_carta_jugador(jugador_actual.get_id())
            
            print(f"📋 Resultado de pedir carta: {resultado}")
            
            if resultado.get('success'):
                estado_juego["mensaje"] = f"🎯 {resultado.get('mensaje', 'Carta repartida')}"
                estado_juego["error"] = None
            else:
                estado_juego["error"] = f"❌ {resultado.get('error', 'Error pidiendo carta')}"
            
            return True
        except Exception as e:
            estado_juego["error"] = f"💥 Error: {str(e)}"
            print(f"💥 Excepción en pedir_carta: {e}")
            return True
    
    def plantarse():
        """Se planta DIRECTAMENTE en BlackJack"""
        try:
            print("🛑 Plantándose...")
            
            # DIRECTO al método de BlackJack
            resultado = blackjack_instance.plantarse_jugador(jugador_actual.get_id())
            
            print(f"📋 Resultado de plantarse: {resultado}")
            
            if resultado.get('success'):
                estado_juego["mensaje"] = f"🏁 {resultado.get('mensaje', 'Te plantaste')}"
                estado_juego["error"] = None
            else:
                estado_juego["error"] = f"❌ {resultado.get('error', 'Error al plantarse')}"
            
            return True
        except Exception as e:
            estado_juego["error"] = f"💥 Error: {str(e)}"
            print(f"💥 Excepción en plantarse: {e}")
            return True
    
    def nueva_partida():
        """Reinicia el juego para una nueva partida"""
        try:
            # Limpiar estado del juego
            blackjack_instance.manos_jugadores = {}
            blackjack_instance.mano_crupier = []
            blackjack_instance.estado_juego = "esperando"
            
            estado_juego["juego_iniciado"] = False
            estado_juego["mensaje"] = "🎮 Presiona INICIAR para comenzar nueva partida"
            estado_juego["error"] = None
            
            return True
        except Exception as e:
            estado_juego["error"] = f"💥 Error reiniciando: {str(e)}"
            return True
    
    def convertir_carta_a_visual(carta_nombre: str) -> str:
        """Convierte carta del backend al formato visual existente"""
        # Mapear cartas del diccionario _cartas a cartas visuales
        carta_map = {
            '2': '2_de_corazones', '3': '3_de_diamantes', '4': '4_de_treboles',
            '5': '5_de_picas', '6': '6_de_corazones', '7': '7_de_diamantes',
            '8': '8_de_treboles', '9': '9_de_picas', '10': '10_de_corazones',
            'J': 'J_de_diamantes', 'Q': 'Q_de_treboles', 'K': 'K_de_picas',
            'A': 'A_de_picas'
        }
        return carta_map.get(carta_nombre, 'A_de_picas')
    
    while True:
        screen.refresh()
        print_text(screen, mesa, True)
        
        # Mostrar mensaje de estado
        mensaje_estado = {
            'text': estado_juego["mensaje"],
            'x-center': 0,
            'y-center': -15,
            'color': Screen.COLOUR_WHITE,
        }
        print_text(screen, mensaje_estado)
        
        # Mostrar error si existe
        if estado_juego["error"]:
            error_text = {
                'text': estado_juego["error"],
                'x-center': 0,
                'y-center': -12,
                'color': Screen.COLOUR_RED,
            }
            print_text(screen, error_text)
        
        # Mostrar información de debug
        debug_text = {
            'text': f'🔍 Debug: Juego iniciado: {estado_juego["juego_iniciado"]} | Instancia: {blackjack_instance is not None}',
            'x-center': 0,
            'y-center': 18,
            'color': Screen.COLOUR_BLACK,
        }
        print_text(screen, debug_text)
        
        # Obtener estado DIRECTAMENTE del BlackJack
        if blackjack_instance and jugador_actual:
            estado_actual = blackjack_instance.obtener_estado_completo(jugador_actual.get_id())
            
            # Mostrar cartas del jugador
            if 'manos_jugadores' in estado_actual:
                jugador_id = jugador_actual.get_id()
                
                if jugador_id in estado_actual['manos_jugadores']:
                    mi_mano = estado_actual['manos_jugadores'][jugador_id]
                    cartas_jugador = mi_mano.get('cartas', [])
                    puntos_jugador = mi_mano.get('puntos', 0)
                    
                    # Mostrar cartas del jugador
                    for i, carta_nombre in enumerate(cartas_jugador):
                        carta_visual = convertir_carta_a_visual(carta_nombre)
                        
                        if carta_visual in cartas:
                            carta = {
                                'text': cartas[carta_visual],
                                'x-center': -30 + (i * 18),
                                'y-center': 5,
                                'color': Screen.COLOUR_BLACK,
                                'bg': Screen.COLOUR_WHITE,
                                'height': 4,
                                'width': 15
                            }
                            print_card(screen, carta)
                    
                    # Mostrar puntos del jugador
                    if cartas_jugador:  # Solo mostrar si hay cartas
                        puntos_text = {
                            'text': f"🎯 Tus puntos: {puntos_jugador}",
                            'x-center': 0,
                            'y-center': 15,
                            'color': Screen.COLOUR_YELLOW,
                        }
                        print_text(screen, puntos_text)
                
                # Mostrar cartas del crupier
                mano_crupier = estado_actual.get('mano_crupier', [])
                plantado = estado_actual.get('manos_jugadores', {}).get(jugador_id, {}).get('plantado', False)
                
                for i, carta_nombre in enumerate(mano_crupier):
                    # Primera carta siempre visible, segunda solo si está plantado
                    if i == 0 or plantado:
                        carta_visual = convertir_carta_a_visual(carta_nombre)
                        
                        if carta_visual in cartas:
                            carta = {
                                'text': cartas[carta_visual],
                                'x-center': -10 + (i * 18),
                                'y-center': -8,
                                'color': Screen.COLOUR_BLACK,
                                'bg': Screen.COLOUR_WHITE,
                                'height': 4,
                                'width': 15
                            }
                            print_card(screen, carta)
                    elif i == 1:
                        # Carta oculta del crupier
                        carta_oculta = {
                            'text': '┌─────────────┐\n'
                                   '│ ?           │\n'
                                   '│             │\n'
                                   '│             │\n'
                                   '│      #      │\n'
                                   '│             │\n'
                                   '│             │\n'
                                   '│           ? │\n'
                                   '└─────────────┘',
                            'x-center': -10 + (i * 18),
                            'y-center': -8,
                            'color': Screen.COLOUR_BLACK,
                            'bg': Screen.COLOUR_WHITE,
                            'height': 4,
                            'width': 15
                        }
                        print_card(screen, carta_oculta)
                
                # Mostrar puntos del crupier si el juego terminó
                if plantado and mano_crupier:
                    puntos_crupier = blackjack_instance.calcular_puntos(mano_crupier)
                    
                    puntos_crupier_text = {
                        'text': f"🤵 Puntos crupier: {puntos_crupier}",
                        'x-center': 0,
                        'y-center': -3,
                        'color': Screen.COLOUR_CYAN,
                    }
                    print_text(screen, puntos_crupier_text)

        # Instrucciones
        instrucciones = {
            'text': 'Presiona F para salir',
            'x-center': 50,
            'y-center': 26,
            'color': Screen.COLOUR_BLACK,
        }
        print_text(screen, instrucciones)

        event = screen.get_event()

        # Botón iniciar (solo si no ha iniciado el juego)
        if not estado_juego["juego_iniciado"]:
            print_button(
                screen,
                boton_iniciar,
                event,
                click=iniciar_partida
            )

        # Botones de acción (solo si el juego está iniciado y no está plantado)
        if estado_juego["juego_iniciado"] and blackjack_instance and jugador_actual:
            plantado = False
            if blackjack_instance.manos_jugadores.get(jugador_actual.get_id()):
                plantado = blackjack_instance.manos_jugadores[jugador_actual.get_id()].get('plantado', False)
            
            if not plantado:
                print_button(
                    screen,
                    boton_pedirCarta,
                    event,
                    click=pedir_carta
                )

                print_button(
                    screen,
                    boton_plantarse,
                    event,
                    click=plantarse
                )
            else:
                # Botón para nueva partida cuando el juego terminó
                print_button(
                    screen,
                    boton_nueva_partida,
                    event,
                    click=nueva_partida
                )

        # Tecla para salir
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            # Limpiar estado al salir
            blackjack_shared.clear_game_state()
            return 'salir'
