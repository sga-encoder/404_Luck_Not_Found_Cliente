from asciimatics.screen import Screen

from ...utils.events import add_key_listener
from ...utils.printers import print_card


def login_hub(screen):
    screen.mouse = True
    
    card_registro_data={
        'text': 'registrarse',
        'x-center': -15,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
        'height': 13,
        'width': 21,
    }
    
    card_iniciar_sesion_data = {
        'text': 'iniciar sesion',
        'x-center': 15,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
        'height': 13,
        'width': 21
    }


    screen.clear()
    while True:
        screen.refresh()
        event = screen.get_event()
        card_registro = print_card(screen, card_registro_data, event, click=lambda: True)
        card_iniciar_sesion = print_card(screen, card_iniciar_sesion_data , event, click=lambda: True)

        if card_registro['result']:
            return 'registro'
        if card_iniciar_sesion['result']:
            return 'iniciar_sesion'


        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'