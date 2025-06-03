from ....utils.events import add_key_listener
from ....utils.printers import print_text, print_button, print_card
from asciimatics.screen import Screen
import pyfiglet
from .cartas import sacar_carta


def blackjack_juego(screen):
    screen.clear()
    screen.mouse = True
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

    # Inicializar 4 jugadores y 1 crupier con 2 cartas cada uno
    jugadores = [[sacar_carta(), sacar_carta()] for _ in range(4)]
    crupier = [sacar_carta(), sacar_carta()]

    posiciones = [
        (-65, -5),  # Jugador 1
        (-47, 15),   # Jugador 2
        (25, 15),    # Jugador 3
        (30, -3),   # Jugador 4
    ]
    posicion_crupier = (0, -13)

    jugador_actual = 0

    def avanzar_turno():
        nonlocal jugador_actual
        if jugador_actual < len(jugadores)-1:
            jugador_actual += 1

    while True:
        screen.refresh()
        print_text(screen, mesa, True)
        # Mostrar todas las cartas del jugador alineadas horizontalmente
        for idx, mano in enumerate(jugadores):
            x_base, y_base = posiciones[idx]
            for j, carta_texto in enumerate(mano):
                carta = {
                    'text': carta_texto,
                    'x-center': x_base + (j * 18),
                    'y-center': y_base,
                    'color': Screen.COLOUR_BLACK,
                    'bg': Screen.COLOUR_WHITE,
                    'height': 4,
                    'width': 15
                }   
                print_card(screen, carta)

            if idx == jugador_actual:
                boton_jugadorActivo['x-center'] = x_base
                boton_jugadorActivo['y-center'] = y_base - 8
                print_button(screen, boton_jugadorActivo, None)
            else:
                boton_jugadorEspera['x-center'] = x_base
                boton_jugadorEspera['y-center'] = y_base - 8
                print_button(screen, boton_jugadorEspera, None, False)

        for i, carta_texto in enumerate(crupier):
            carta_oculta = {
                'text': carta_texto if i == 0 else (
                        '┌─────────────┐'
                '        │ ?           │'
                '        │             │'
                '        │             │'
                '        │      #      │'
                '        │             │'
                '        │             │'
                '        │           ? │'
                '        └─────────────┘' 
                ),
                'x-center': 0,
                'y-center': 0,
                'color': Screen.COLOUR_BLACK,
                'bg': Screen.COLOUR_WHITE,
                'height': 4,
                'width': 15
            }
            print_card(screen, carta_oculta)

        event = screen.get_event()

        # Jugadores pueden pedir más cartas
        print_button(
            screen,
            boton_pedirCarta,
            event,
            click=lambda: jugadores[jugador_actual].append(sacar_carta())
        )

        print_button(
            screen,
            boton_plantarse,
            event,
            click=avanzar_turno
        )

        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'
