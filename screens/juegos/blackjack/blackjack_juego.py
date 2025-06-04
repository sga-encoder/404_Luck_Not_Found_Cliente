from ....utils.events import add_key_listener
from ....utils.printers import print_text, print_button, print_card
from asciimatics.screen import Screen
import pyfiglet
import time
from .cartas import sacar_carta

# Importar del módulo compartido para evitar importación circular
from . import blackjack_shared

# Importar las cartas desde cartas.py
from .cartas import cartas

def blackjack_juego(screen):
    screen.clear()
    screen.mouse = True
    
    # ================= INTEGRACIÓN CON BACKEND =================
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
    
    # Inicializar partida automáticamente
    try:
        print("🎮 Iniciando partida automáticamente...")
        resultado = blackjack_instance.iniciar_partida_blackjack(jugador_actual.get_id())
        if not resultado.get('success'):
            print(f"❌ Error iniciando partida: {resultado.get('error')}")
    except Exception as e:
        print(f"💥 Error iniciando partida: {e}")
    
    # ================= TU FRONTEND EXACTO =================
    mesa = {
        'text': 'Mesa BlackJack',
        'x-center': 0,
        'y-center': -20,
        'font': 'elite',
        'justify': 'center',
        'color': Screen.COLOUR_CYAN,
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

    boton_jugadorActivo = {
        'text': '[JUGADOR ACTIVO]',
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
    }
    
    boton_jugadorEspera = {
        'text': '[JUGADOR ESPERANDO]',
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_MAGENTA,
    }

    # ================= FUNCIONES DE INTEGRACIÓN =================
    def obtener_datos_del_backend():
        """Obtiene los datos del juego desde el backend BlackJack"""
        try:
            if not blackjack_instance or not jugador_actual:
                return [], []
            
            # Obtener estado completo desde Firestore
            estado_actual = blackjack_instance.obtener_estado_completo(jugador_actual.get_id())
            
            if 'manos_jugadores' in estado_actual:
                jugador_id = jugador_actual.get_id()
                
                # Obtener cartas del jugador
                jugadores_cartas = []
                if jugador_id in estado_actual['manos_jugadores']:
                    mi_mano = estado_actual['manos_jugadores'][jugador_id]
                    cartas_jugador = mi_mano.get('cartas', [])
                    
                    # Convertir a formato que espera el frontend (4 jugadores)
                    for i in range(4):
                        if i == 0:  # El jugador actual es el jugador 1
                            jugadores_cartas.append(cartas_jugador)
                        else:  # Otros jugadores ficticios
                            jugadores_cartas.append([sacar_carta(), sacar_carta()])
                else:
                    # Si no hay datos, usar cartas por defecto
                    jugadores_cartas = [[sacar_carta(), sacar_carta()] for _ in range(4)]
                
                # Obtener cartas del crupier
                crupier_cartas = estado_actual.get('mano_crupier', [sacar_carta(), sacar_carta()])
                
                return jugadores_cartas, crupier_cartas
            else:
                # Fallback: datos por defecto
                return [[sacar_carta(), sacar_carta()] for _ in range(4)], [sacar_carta(), sacar_carta()]
                
        except Exception as e:
            print(f"⚠️ Error obteniendo datos del backend: {e}")
            # Fallback: datos por defecto
            return [[sacar_carta(), sacar_carta()] for _ in range(4)], [sacar_carta(), sacar_carta()]

    def obtener_carta_desde_cartas_py(carta_nombre: str) -> str:
        """Obtiene la carta ASCII desde cartas.py o genera una básica"""
        if not carta_nombre:
            return sacar_carta()
        
        # Buscar la carta en el diccionario de cartas
        carta_ascii = cartas.get(carta_nombre)
        
        if carta_ascii:
            return carta_ascii
        else:
            # Fallback: carta básica
            palos = ['♠', '♣', '♥', '♦']
            palo = palos[hash(carta_nombre) % len(palos)]
            
            return (f'┌─────────────┐\n'
                   f'│{carta_nombre:<2}           │\n'
                   f'│             │\n'
                   f'│             │\n'
                   f'│      {palo}      │\n'
                   f'│             │\n'
                   f'│             │\n'
                   f'│          {carta_nombre:>2}│\n'
                   f'└─────────────┘')

    def pedir_carta_backend():
        """Función que conecta con el backend para pedir carta"""
        try:
            print("🃏 Pidiendo carta al backend...")
            resultado = blackjack_instance.pedir_carta_jugador(jugador_actual.get_id())
            
            if resultado.get('success'):
                print(f"✅ Carta recibida: {resultado.get('nueva_carta')} - Puntos: {resultado.get('puntos')}")
                return True
            else:
                print(f"❌ Error pidiendo carta: {resultado.get('error')}")
                return False
        except Exception as e:
            print(f"💥 Error en pedir_carta_backend: {e}")
            return False

    def plantarse_backend():
        """Función que conecta con el backend para plantarse"""
        try:
            print("🛑 Plantándose en el backend...")
            resultado = blackjack_instance.plantarse_jugador(jugador_actual.get_id())
            
            if resultado.get('success'):
                print(f"✅ Plantado exitosamente: {resultado.get('mensaje')}")
                return True
            else:
                print(f"❌ Error al plantarse: {resultado.get('error')}")
                return False
        except Exception as e:
            print(f"💥 Error en plantarse_backend: {e}")
            return False

    # ================= OBTENER DATOS INICIALES =================
    # Inicializar 4 jugadores y 1 crupier con datos del backend
    jugadores, crupier = obtener_datos_del_backend()

    posiciones = [
        (-65, -5),  # Jugador 1
        (-47, 15),   # Jugador 2
        (25, 15),    # Jugador 3
        (30, -3),   # Jugador 4
    ]
    posicion_crupier = (0, -13)

    jugador_actual_indice = 0

    def avanzar_turno():
        nonlocal jugador_actual_indice
        if jugador_actual_indice < len(jugadores)-1:
            jugador_actual_indice += 1
        
        # También llamar al backend para plantarse
        plantarse_backend()

    # ================= BUCLE PRINCIPAL CON INTEGRACIÓN =================
    while True:
        # Actualizar datos del backend periódicamente
        if hasattr(blackjack_juego, '_last_update'):
            import time
            if time.time() - blackjack_juego._last_update > 1:  # Actualizar cada segundo
                jugadores, crupier = obtener_datos_del_backend()
                blackjack_juego._last_update = time.time()
        else:
            blackjack_juego._last_update = time.time()
        
        screen.refresh()
        print_text(screen, mesa, True)
        
        # Mostrar todas las cartas del jugador alineadas horizontalmente
        for idx, mano in enumerate(jugadores):
            x_base, y_base = posiciones[idx]
            for j, carta_texto in enumerate(mano):
                # Usar cartas reales desde cartas.py
                carta_ascii = obtener_carta_desde_cartas_py(carta_texto)
                
                carta = {
                    'text': '',
                    'x-center': x_base + (j * 18),
                    'y-center': y_base,
                    'color': Screen.COLOUR_BLACK,
                    'bg': Screen.COLOUR_WHITE,
                    'height': 15,
                    'width': 15,
                    'ascii_x': " ",
                    'ascii_y': " ",
                    'grid': True,
                    'grid_divider_x': 1,
                    'grid_divider_y': 1,
                    'content': {
                        '0': {
                            'text': carta_ascii,  # Usar carta ASCII real
                            'color': Screen.COLOUR_BLACK,
                            'bg': Screen.COLOUR_WHITE,             
                        }
                    }
                }
                   
                print_card(screen, carta)

            if idx == jugador_actual_indice:
                boton_jugadorActivo['x-center'] = x_base
                boton_jugadorActivo['y-center'] = y_base - 8
                print_button(screen, boton_jugadorActivo, None)
            else:
                boton_jugadorEspera['x-center'] = x_base
                boton_jugadorEspera['y-center'] = y_base - 8
                print_button(screen, boton_jugadorEspera, None, False)

        # Mostrar cartas del crupier
        for i, carta_texto in enumerate(crupier):
            # Verificar si el jugador se plantó para mostrar todas las cartas del crupier
            plantado = False
            try:
                if blackjack_instance.manos_jugadores.get(jugador_actual.get_id()):
                    plantado = blackjack_instance.manos_jugadores[jugador_actual.get_id()].get('plantado', False)
            except:
                pass
            
            # Primera carta siempre visible, segunda solo si se plantó
            if i == 0 or plantado:
                carta_ascii = obtener_carta_desde_cartas_py(carta_texto)
            else:
                carta_ascii = (
                    '┌─────────────┐\n'
                    '│ ?           │\n'
                    '│             │\n'
                    '│             │\n'
                    '│      #      │\n'
                    '│             │\n'
                    '│             │\n'
                    '│           ? │\n'
                    '└─────────────┘'
                )
            
            carta_oculta = {
                'text': carta_ascii,
                'x-center': posicion_crupier[0] + (i * 18),  # Posicionar cartas del crupier
                'y-center': posicion_crupier[1],
                'color': Screen.COLOUR_BLACK,
                'bg': Screen.COLOUR_WHITE,
                'height': 15,
                'width': 15
            }
            print_card(screen, carta_oculta)

        event = screen.get_event()

        # Jugadores pueden pedir más cartas - CONECTADO AL BACKEND
        resultado_pedir = print_button(
            screen,
            boton_pedirCarta,
            event,
            click=lambda: pedir_carta_backend() and obtener_datos_del_backend()
        )
        
        # Al hacer click en pedir carta, actualizar datos
        if resultado_pedir.get('result'):
            time.sleep(0.5)  # Pequeña pausa para que se actualice Firestore
            jugadores, crupier = obtener_datos_del_backend()

        # Plantarse - CONECTADO AL BACKEND
        resultado_plantarse = print_button(
            screen,
            boton_plantarse,
            event,
            click=avanzar_turno
        )
        
        # Al plantarse, actualizar datos
        if resultado_plantarse.get('result'):
            time.sleep(0.5)  # Pequeña pausa para que se actualice Firestore
            jugadores, crupier = obtener_datos_del_backend()

        # Salir del juego
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            print("🚪 Saliendo del BlackJack...")
            try:
                blackjack_shared.clear_game_state()
                time.sleep(0.2)
            except Exception as e:
                print(f"⚠️ Error durante limpieza al salir: {e}")
            finally:
                print("👋 Salida del BlackJack completada")
            return 'salir'
