import copy
from servidor.src.utils.pretty_printer import PrettyPrinter
from servidor.src.model.usuario import UsuarioServicio

from servidor.src.utils.firestore import add_realtime_listener
from .dados import get_dado
from ....utils.events import add_key_listener, get_remaining_cooldown
from ....utils.printers import print_card, print_text
from asciimatics.screen import Screen
import pyfiglet
from asciimatics.event import MouseEvent

# Variable global para almacenar el último evento del mouse
last_mouse_event = None



def knucklebones_juego(screen, id_sala=None, jugador=None, salaDeJuego=None):
    global last_mouse_event
    
    screen.mouse = True
    screen.clear()
    # Inicializa color para cada celda
    color1 = [Screen.COLOUR_DEFAULT] * 9
    color2 = [Screen.COLOUR_DEFAULT] * 9
    print_vs_data ={
        'text': 'V.S', 
        'x-center': 0, 
        'y-center': 0, 
        'font': "big_money-ne"
    }
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
    
    data = None
    index_jugador = 0
    
    usuario_servicio = UsuarioServicio()
    def mi_callback(doc_data, changes, read_time):
        """Callback que se ejecuta cuando hay cambios"""
        nonlocal data, index_jugador
        if doc_data:
            data = doc_data
            index_jugador = next((i for i, uid in enumerate(doc_data.get('jugadores', [])) if uid == jugador.get_id()), 0)
        else:
            print("📡 Documento eliminado o no existe")
            data = None
    
    
    def mi_error_callback(error):
        """Callback para manejar errores"""
        print(f"❌ Error en listener: {error}")
    
    unsubscribe = add_realtime_listener(
        'salas_de_juego_activas', 
        id_sala,
        mi_callback,
        mi_error_callback
    )

    while True:
        vs = print_text(screen, print_vs_data, True)
        
        
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
        
        # Obtener eventos
        event = screen.get_event()
        # Guardar el último MouseEvent válido
        if isinstance(event, MouseEvent):
            last_mouse_event = event
        event_mouse = last_mouse_event
        
        # Configuración de la primera carta (jugador 1)
        print_card_data_1 = copy.deepcopy(print_card_data)
        print_card_data_1['x-center'] = -40
        print_card_data_1['y-center'] = 0
        print_card_data_1['click'] = {
            '0': {'event': event_mouse, 'click': lambda: '0'},
            '1': {'event': event_mouse, 'click': lambda: '1'},
            '2': {'event': event_mouse, 'click': lambda: '2'},
        }
        print_card_data_1['content'] = {
            str(i): {
                'text': get_dado((i % 3) + 1),
                'padding-top': 1,
                'padding-left': 2,
                'color': color1[i],
            } for i in range(9)
        }
        if data is not None:
            # Si hay datos de la sala, usar los dados del jugador 2
            print_card_data_1['content'] = {
                str(i): {
                    'text': get_dado(data['mesa_jugador_0'][i]),
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color1[i],
                } for i in range(len(data['mesa_jugador_0']))
            }
        else:
            print_card_data_1['content'] = {
                str(i): {
                    'text': get_dado(0),
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color1[i],
                } for i in range(9)
            }
        
        # Configuración de la segunda carta (jugador 2)
        print_card_data_2 = copy.deepcopy(print_card_data)
        print_card_data_2['x-center'] = 40
        print_card_data_2['y-center'] = 0
        print_card_data_2['click'] = {
            '0': {'event': event_mouse, 'click': lambda: '0'},
            '1': {'event': event_mouse, 'click': lambda: '1'},
            '2': {'event': event_mouse, 'click': lambda: '2'},
        }
        if data is not None:
            # Si hay datos de la sala, usar los dados del jugador 2
            print_card_data_2['content'] = {
                str(i): {
                    'text': get_dado(data['mesa_jugador_1'][i]),
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color2[i],
                } for i in range(len(data['mesa_jugador_1']))
            }
        else:
            print_card_data_2['content'] = {
                str(i): {
                    'text': get_dado(0),
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color2[i],
                } for i in range(9)
            }        # Dibujar las cartas
        card_1 = print_card(screen, print_card_data_1, event_mouse)
        card_2 = print_card(screen, print_card_data_2, event_mouse)
        
        jugador_print = print_text(screen, {
            'text': (data['jugadores'][0] if 
                    data is not None and len(data['jugadores']) > index_jugador else ''),
            'x': card_1['x_position'] + 2,
            'y': card_1['y_position'] + card_1['height'] + 5,
            'color': Screen.COLOUR_CYAN        })
        
        jugador_activo = print_text(screen, {
            'text': data['turnoActivo'] if data is not None else '',
            'x-center': 0,
            'y-center': card_2['y_position'],
            'color': Screen.COLOUR_CYAN
        })
        card_1_result = card_1['result']
        # card_2_result = card_2['result']
        
        # Procesar clicks de la primera carta
        for idx, result in enumerate(card_1_result):
            if (data is not None and jugador.get_id() == data['jugadores'][index_jugador]):
                # Si hay datos y el jugador es el activo, permitir clicks
                if result is not None:
                    print(f"Click en fila/columna: {idx}")
                    color1[idx] = Screen.COLOUR_GREEN if color1[idx] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                    color1[idx + 3] = Screen.COLOUR_GREEN if color1[idx + 3] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                    color1[idx + 6] = Screen.COLOUR_GREEN if color1[idx + 6] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
                    
        # Procesar clicks de la segunda carta
        # for idx, result in enumerate(card_2_result):
        #     if result is not None:
        #         print(f"Click en fila/columna: {idx}")
        #         color2[idx] = Screen.COLOUR_GREEN if color2[idx] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
        #         color2[idx + 3] = Screen.COLOUR_GREEN if color2[idx + 3] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
        #         color2[idx + 6] = Screen.COLOUR_GREEN if color2[idx + 6] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT
          # Verificar si el usuario quiere salir
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            # Detener el listener antes de salir
            if unsubscribe:
                unsubscribe()
            return 'salir'
        
        # Actualizar la pantalla después de dibujar todo el contenido
        screen.refresh()