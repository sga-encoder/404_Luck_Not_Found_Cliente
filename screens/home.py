from asciimatics.screen import Screen

from ..utils.events import add_key_listener
from ..utils.printers import print_card

def home(screen):
    screen.mouse = True
    
    card_poker_data={
        'text': 'poker texas hold\'em',
        'x-center': -30,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
        'height': 13,
        'width': 21,
    }
    
    card_blackjack_data = {
        'text': 'blackjack european',
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
        'height': 13,
        'width': 21
    }

    card_knucklebones_data = {
        'text': 'knucklebones',
        'x-center': 30,
        'y-center': 0,
        'bg': Screen.COLOUR_BLUE,
        'color': Screen.COLOUR_BLACK,
        'height': 13,
        'width': 21
    }

    screen.clear()
    while True:
        screen.refresh()
        event = screen.get_event()
        card_poker = print_card(screen, card_poker_data, event, click=lambda: True)
        card_blackjack = print_card(screen, card_blackjack_data , event, click=lambda: True)
        card_knucklebones = print_card(screen, card_knucklebones_data, event, click=lambda: True)

        if card_poker['result']:
            return 'poker'
        if card_blackjack['result']:
            return 'blackjack'
        if card_knucklebones['result']:
            return 'knucklebones'
        
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'