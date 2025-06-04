import copy
from .dados import get_dado
from ....utils.events import add_key_listener, get_remaining_cooldown
from ....utils.printers import print_card, print_text
from asciimatics.screen import Screen
import pyfiglet
from asciimatics.event import MouseEvent

# Variable global para almacenar el último evento del mouse
last_mouse_event = None

def knucklebones_juego(screen):
    global last_mouse_event
    screen.mouse = True
    screen.clear()
    contador = 0
    # Inicializa color para cada celda
    color1 = [Screen.COLOUR_DEFAULT] * 9
    color2 = [Screen.COLOUR_DEFAULT] * 9
    print_card_data = {
        'width': 55,
        'height': 27,
        'text': '',
        'ascii_y': '│',
        'ascii_x': '─',
        'grid_divider_x': 3,
        'grid_divider_y': 3,
        'corner': ['╭', '╮', '╰', '╯'],
        'grid': True,
        'grid_click': 'row',
        'color': Screen.COLOUR_MAGENTA,
    }

    while True:
        vs = print_text(screen, {'text': 'V.S', 'x-center': 0, 'y-center': 0, 'font': "big_money-ne"}, True)
        
        # Mostrar información de cooldown para debug (opcional)
        cooldown_info = []
        for i in range(3):
            element_id = f"grid_column_{i}_"  # Prefijo del ID
            remaining = get_remaining_cooldown(element_id + "0_0")  # Aproximación para debug
            if remaining > 0:
                cooldown_info.append(f"Col {i}: {remaining:.1f}s")
        
        if cooldown_info:
            cooldown_text = " | ".join(cooldown_info)
            print_text(screen, {
                'text': f"Cooldown: {cooldown_text}",
                'x-center': 0,
                'y-center': -15,
                'color': Screen.COLOUR_YELLOW
            })
        # screen.clear()
        
        screen.refresh()
        event = screen.get_event()
        # Guardar el último MouseEvent válido
        if isinstance(event, MouseEvent):
            last_mouse_event = event
        event_mouse = last_mouse_event
        contador += 1
        
        print_card_data_1 = copy.deepcopy(print_card_data)
        print_card_data_1['x-center'] = -40
        print_card_data_1['y-center'] = 0
        print_card_data_1['click'] = {
            '0': {'event': event_mouse, 'click': lambda: '0'},
            '1': {'event': event_mouse, 'click': lambda: '1'},
            '2': {'event': event_mouse, 'click': lambda: '2'},
        }
        print_card_data_1['content']= {
            str(i): {
                    'text': get_dado((i % 3) + 1),
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color1[i],
                } for i in range(9)
        }
        print_card_data_2 =  copy.deepcopy(print_card_data)
        print_card_data_2['x-center'] = 40
        print_card_data_2['y-center'] = 0
        print_card_data_2['click'] = {
            '0': {'event': event_mouse, 'click': lambda: '0'},
            '1': {'event': event_mouse, 'click': lambda: '1'},
            '2': {'event': event_mouse,  'click': lambda: '2'},
        }
        print_card_data_2['content']= {
            str(i): {
                    'text': get_dado((i % 3) + 1),
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color2[i],
                } for i in range(9)
        }
        card_1 = print_card(screen, print_card_data_1, event_mouse)
        card_2 = print_card(screen, print_card_data_2, event_mouse)
        card_1_result = card_1['result']
        card_2_result = card_2['result']
        print(f"Resultado de clicks: {card_1_result}" )
        # Cuando proceses los clicks:
        for idx, result in enumerate(card_1_result):
            if result is not None:
                print(f"Click en fila/columna: {idx}")
                color1[idx] = Screen.COLOUR_GREEN if color1[idx] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                color1[idx + 3] = Screen.COLOUR_GREEN if color1[idx + 3] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                color1[idx + 6] = Screen.COLOUR_GREEN if color1[idx + 6] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                
        for idx, result in enumerate(card_2_result):
            if result is not None:
                print(f"Click en fila/columna: {idx}")
                color2[idx] = Screen.COLOUR_GREEN if color2[idx] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                color2[idx + 3] = Screen.COLOUR_GREEN if color2[idx + 3] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                color2[idx + 6] = Screen.COLOUR_GREEN if color2[idx + 6] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'