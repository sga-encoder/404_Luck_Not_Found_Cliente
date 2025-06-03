from ....utils.events import add_key_listener
from ....utils.printers import print_text, print_button
from asciimatics.screen import Screen
import pyfiglet
from .blackjack_juego import blackjack_juego


def blackjack_inicio(screen):
    screen.clear()
    screen.mouse = True 
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
    while True:
        screen.refresh()
        print_text(screen, text, True)
        event = screen.get_event()
        button_inicio = print_button(
            screen,
            boton_iniciar,
            event,
            click=lambda: True
        )
        if button_inicio['result']:
            return 'iniciar blackjack'
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'
