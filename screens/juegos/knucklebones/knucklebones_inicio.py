from asciimatics.screen import Screen


from ....utils.events import add_key_listener
from ....utils.printers import print_button, print_text

def knucklebones_inicio(screen):
    screen.mouse = True
    text = {
        'text': 'KUCKLEBONES',
        'x-center': 0,
        'y-center': -5,
        'font': 'big_money-ne',
        'justify': 'center',
        'max-width': 120,
    }
    boton_text = {
        'text': '[  INICIAR JUEGO  ]',
        'x-center': 0,
        'y-center': 5,
        'color': Screen.COLOUR_WHITE,
        'bg': Screen.COLOUR_CYAN
    }
    screen.clear()
    while True:
        screen.refresh()
        print_text(screen, text, True)
        event = screen.get_event()  # Solo aquí
        button_inicio = print_button(
            screen,
            boton_text,
            event,
            click=lambda: True
        )
        if button_inicio['result']:
            return button_inicio['result']