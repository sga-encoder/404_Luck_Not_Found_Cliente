from asciimatics.screen import Screen
from pyfiglet import Figlet

from .helpers import create_card


def print_text(screen, data: dict, asccii_art: bool = False) -> dict:
    """
    Dibuja texto en la pantalla usando Asciimatics con soporte para arte ASCII y posicionamiento personalizado avanzado.
    
    Esta función es la base del sistema de renderizado de texto y proporciona múltiples opciones de 
    posicionamiento tanto absoluto como relativo, además de soporte completo para arte ASCII usando pyfiglet.

    Args:
        screen: Objeto Screen de asciimatics donde se imprimirá el texto.
        data (dict): Diccionario de configuración con las siguientes claves posibles:
            
            **Contenido (obligatorio):**
            - 'text' (str): El texto a mostrar. Puede contener saltos de línea (\n) para texto multilínea.
            
            **Configuración de Arte ASCII (opcional):**
            - 'font' (str): Fuente para arte ASCII (por defecto 'slant'). 
              Fuentes disponibles: 'slant', 'banner', 'big', 'block', etc.
            - 'justify' (str): Justificación del arte ASCII ('left', 'center', 'right'). Por defecto 'left'.
            - 'max-width' (int): Ancho máximo para el arte ASCII (por defecto 100).
            
            **Configuración Visual (opcional):**
            - 'color' (int): Color del texto usando constantes de Screen.COLOUR_* (por defecto Screen.COLOUR_WHITE).
            - 'bg' (int): Color de fondo usando constantes de Screen.COLOUR_* (opcional).
            
            **Posicionamiento Absoluto (opcional):**
            - 'x_position' (int): Posición X absoluta en caracteres.
            - 'y_position' (int): Posición Y absoluta en líneas.
            - 'x' (int): Alias para 'x_position'.
            - 'y' (int): Alias para 'y_position'.
            
            **Posicionamiento Relativo al Centro (opcional):**
            - 'x-center' (int): Desplazamiento horizontal desde el centro de la pantalla.
              Valores negativos mueven a la izquierda, positivos a la derecha.
            - 'y-center' (int): Desplazamiento vertical desde el centro de la pantalla.
              Valores negativos mueven hacia arriba, positivos hacia abajo.
            
            **Posicionamiento desde Bordes (opcional):**
            - 'x-right' (int): Distancia desde el borde derecho de la pantalla.
            - 'y-bottom' (int): Distancia desde el borde inferior de la pantalla.
        
        asccii_art (bool): Si es True, renderiza el texto como arte ASCII usando pyfiglet.
            Cuando está activado, utiliza las opciones 'font', 'justify' y 'max-width' del diccionario data.

    Returns:
        dict: Diccionario con información sobre el texto renderizado:
            - 'width' (int): Ancho máximo del texto en caracteres.
            - 'height' (int): Altura del texto en líneas.
            - 'x_position' (int): Posición X final donde se renderizó el texto.
            - 'y_position' (int): Posición Y final donde se renderizó el texto.

    Raises:
        ValueError: Si el diccionario 'data' no contiene la clave 'text'.

    Ejemplos:
        # Texto simple centrado
        print_text(screen, {
            'text': 'Hola Mundo',
            'x-center': 0,
            'y-center': 0,
            'color': Screen.COLOUR_RED
        })
        
        # Arte ASCII con fuente personalizada
        print_text(screen, {
            'text': 'CASINO',
            'font': 'banner',
            'justify': 'center',
            'x-center': 0,
            'y': 5,
            'color': Screen.COLOUR_CYAN
        }, asccii_art=True)
        
        # Texto multilínea posicionado absolutamente
        print_text(screen, {
            'text': 'Línea 1\nLínea 2\nLínea 3',
            'x_position': 10,
            'y_position': 20,
            'color': Screen.COLOUR_GREEN,
            'bg': Screen.COLOUR_BLACK
        })
        
        # Texto desde borde derecho
        print_text(screen, {
            'text': 'Esquina',
            'x-right': 5,
            'y-bottom': 2,
            'color': Screen.COLOUR_YELLOW
        })

    Notas:
        - El sistema de posicionamiento tiene prioridad: absoluto > relativo al centro > desde bordes.
        - Para texto multilínea, 'width' devuelve el ancho de la línea más larga.
        - El arte ASCII puede generar texto significativamente más grande que el texto original.
        - Los colores de fondo solo se aplican a los caracteres del texto, no al área completa.
        - El posicionamiento relativo se calcula dinámicamente basado en el tamaño de la pantalla.
    """
    if( 'text' not in data):
        raise ValueError("El diccionario debe contener la clave 'text'.")
    
    font = data['font'] if 'font' in data else 'slant'
    color = data['color'] if 'color' in data else Screen.COLOUR_WHITE
    bg = data['bg'] if 'bg' in data else None
    justify = data['justify' ] if 'justify' in data else 'left'
    max_width = data['max-width' ] if 'max-width' in data else 100
    x_position = 0
    y_position = 0
    text = []
    height = 0
    if asccii_art:
        f = Figlet(font=font, width=max_width, justify=justify)
        ascii_text = f.renderText(data['text'])
        text = ascii_text.split('\n')
        height = len(text)
    else:
        text = data['text'].split('\n')
        height = len(text)
      # Calcular el ancho máximo de todas las líneas
    width = max(len(line) for line in text) if text else 0
    if 'y_position' in data:
        y_position = data['y_position']
    else:
        if 'y' in data:
            y_position = data['y']
        elif 'y-center' in data:
            y_position = (screen.height // 2 - height // 2) + data['y-center']
        elif 'y-bottom' in data:
            y_position = screen.height - height - data['y-bottom']

    for idx, line in enumerate(text):
        # Usar el ancho máximo para la posición x
        if 'x_position' in data:
            x_position = data['x_position']
        else:
            if 'x' in data:
                x_position = data['x']
            elif 'x-center' in data:
                x_position = (screen.width - width) // 2 + data['x-center']
            elif 'x-right' in data:
                x_position = screen.width - width - data['x-right']
            else:
                x_position = 0  # Valor por defecto si no se especifica posición

        if(bg is not None):
            screen.print_at(line, x_position, y_position + idx, colour=color, bg=bg)
        else:
            screen.print_at(line, x_position, y_position + idx, colour=color)

    # print(f"[DEBUG] print_text: x_position={x_position}, y_position={y_position}, width={width}, height={height}")
    return {
        "width": width,
        "height": height,
        "x_position": x_position,
        "y_position": y_position
    }
    
def print_button(screen, data: dict, event=None, click=None) -> dict:
    from .events import add_mouse_listener  # Importación local para evitar ciclo

    """
    Dibuja un botón en la pantalla y detecta si ha sido presionado mediante un clic del mouse.

    Args:
        screen: Objeto Screen de asciimatics donde se imprimirá el botón.
        data (dict): Diccionario con las siguientes claves posibles:
            - 'text' (str): El texto a mostrar (obligatorio).
            - 'font' (str): Fuente para arte ASCII (opcional, por defecto 'slant').
            - 'color' (int): Color del texto (opcional, por defecto blanco).
            - 'bg' (int): Color de fondo (opcional).
            - 'x', 'x-center', 'x-right' (int): Posición horizontal (opcional).
            - 'y', 'y-center', 'y-bottom' (int): Posición vertical (opcional).
        event: Evento de entrada (generalmente un MouseEvent) a evaluar para detectar el clic.
        click (callable, opcional): Función a ejecutar si el botón es presionado.

    Returns:
        dict: Diccionario con la siguiente información:
            - 'result': Resultado de la función click() si se presionó el botón, None en caso contrario.
            - 'width': Ancho del botón (int)
            - 'height': Alto del botón (int)
            - 'x_position': Posición x del botón (int)
            - 'y_position': Posición y del botón (int)

    Notas importantes:
        - Debes activar el modo mouse: antes de usar botones con clic, asegúrate de tener 'screen.mouse = True'.
        - El orden importa: siempre llama a 'screen.refresh()' antes de 'screen.get_event()'.
        - El área de clic del botón cubre todo el bloque de texto generado, no solo una línea.
        - El evento debe ser un objeto MouseEvent y debe tener 'event.buttons != 0' para que se considere un clic.
        - El botón puede tener varias líneas (por ejemplo, si el texto contiene saltos de línea o es arte ASCII).
        - El área de detección se calcula usando el ancho máximo y la altura total del texto renderizado.
        - Si el usuario hace clic dentro de esa área, se ejecuta la función click y su resultado se devuelve en 'result'.

    Ejemplo de uso:
        screen.mouse = True  # Habilitar eventos de mouse
        while True:
            print_button(screen, data, ...)
            screen.refresh()  # Refresca antes de obtener el evento
            event = screen.get_event()
            resultado = print_button(screen, data, event, click=lambda: True)
            if resultado['result']:
                print("¡Botón presionado!")    """
    button= print_text(screen, data)
    # screen.refresh()
    result = add_mouse_listener(screen, button, event, click, element_id=f"button_{button['x_position']}_{button['y_position']}") if click else None
    return {
        "result": result,
        "width": button['width'],
        "height": button['height'],
        "x_position": button['x_position'],
        "y_position": button['y_position']
    }
    
def print_card(screen, data: dict, event=None, click=None) -> dict:
    from .events import add_mouse_listener  # Importación local para evitar ciclo
    """
    Dibuja una carta visual personalizada en la pantalla usando Asciimatics y permite detectar si ha sido presionada mediante un clic del mouse.

    Parámetros:
        screen: Objeto Screen de asciimatics donde se imprimirá la carta.
        data (dict): Diccionario de configuración de la carta. Claves posibles:
            - 'text' (str): Texto a mostrar dentro de la carta (obligatorio).
            - 'width' (int): Ancho de la carta (opcional, por defecto 21).
            - 'height' (int): Alto de la carta (opcional, por defecto 13).
            - 'ascii_x' (str): Caracter para los bordes horizontales (opcional, por defecto '██').
            - 'ascii_y' (str): Caracter para los bordes verticales (opcional, por defecto '█').
            - 'corner' (list): Caracteres para las esquinas (opcional, por defecto ['█','█','█','█']).
            - 'color' (int): Color del texto y bordes (opcional, por defecto blanco).
            - 'bg' (int): Color de fondo (opcional, por defecto Screen.COLOUR_DEFAULT).
            - 'x', 'x-center', 'x-right' (int): Posición horizontal (opcional).
            - 'y', 'y-center', 'y-bottom' (int): Posición vertical (opcional).
        event: Evento de entrada (MouseEvent) a evaluar para detectar el clic (opcional).
        click (callable, opcional): Función a ejecutar si la carta es presionada.

    Retorna:
        dict: Diccionario con la siguiente información:
            - 'result': Resultado de la función click() si se presionó la carta, None en caso contrario.
            - 'width': Ancho de la carta (int).
            - 'height': Alto de la carta (int).
            - 'x_position': Posición x de la carta (int).
            - 'y_position': Posición y de la carta (int).

    Notas:
        - Es necesario activar el modo mouse: antes de usar cartas con clic, asegúrate de tener 'screen.mouse = True'.
        - El área de clic de la carta cubre todo el bloque generado por la función create_card.
        - El evento debe ser un objeto MouseEvent y debe tener 'event.buttons != 0' para que se considere un clic.
        - El área de detección se calcula usando el ancho y la altura de la carta renderizada.
        - Si el usuario hace clic dentro de esa área, se ejecuta la función click y su resultado se devuelve en 'result'.
    """    # establecer valores por defecto o usar los proporcionados en el diccionario data
    width = data.get('width', 21)
    height = data.get('height', 13)
    text = data.get('text', '')
    ascii_x = data.get('ascii_x', '─')
    ascii_y = data.get('ascii_y', '│')
    corner = data.get('corner', ['╭', '╮', '╰', '╯'])
    color = data.get('color', Screen.COLOUR_WHITE)
    bg = data.get('bg', Screen.COLOUR_DEFAULT)
    justify = data.get('justify', 'left')
    grid = data.get('grid', False)
      # Inicializar buttons_return para evitar UnboundLocalError
    buttons_return = {}
    max_width = data.get('max-width', 100)
    grid_ascii_x = data.get('grid_ascii_x', ascii_x)
    grid_ascii_y = data.get('grid_ascii_y', ascii_y)
    grid_intersections = data.get('grid_intersections', ['┼', '┬', '┴', '├', '┤'])
    grid_corners = data.get('grid_corners', corner)  # Bordes específicos para grid
    grid_divider_x = data.get('grid_divider_x', 2)
    grid_divider_y = data.get('grid_divider_y', 2)
    grid_click = data.get('grid_click', None)
    
    grid_cell_width = width-(2*len(ascii_x))-grid_divider_x+1 // grid_divider_x
    grid_cell_height = height-(2*len(ascii_y))-grid_divider_y+1 // grid_divider_y
    data_card_ascii = {
        'width': width,
        'height': height,
        'text': text,
        'ascii_x': ascii_x,
        'ascii_y': ascii_y,
        'corner': corner,
        'grid': grid,
        'grid_ascii_x': grid_ascii_x,
        'grid_ascii_y': grid_ascii_y,
        'grid_intersections': grid_intersections,
        'grid_divider_x': grid_divider_x,
        'grid_divider_y': grid_divider_y,
        'grid_cell_width': grid_cell_width,
        'grid_cell_height': grid_cell_height	
    }
    data_card_printer = {
        'color': color,
        'bg': bg,
        'justify': justify,
        'max-width': max_width
    }
    
    
    # Crear la carta con los datos proporcionados
    card_create = create_card(data_card_ascii)
    data_card_printer['text'] = card_create['text'] if grid else card_create
    for pos_key in ['x', 'y', 'x-center', 'y-center', 'x-right', 'y-bottom', 'x_position', 'y_position']:
        if pos_key in data:
            data_card_printer[pos_key] = data[pos_key]
    card = print_text(screen, data_card_printer)
    
    grid_num_cells = None
    grid_cell = []
    if grid:
        data_position = card_create['data']
        grid_num_cells = grid_divider_x * grid_divider_y
        if 'content' in data:
            content = data['content']
            for i in range(grid_num_cells):
                if str(i) in content:
                    padding_top = 0
                    padding_left = 0
                    padding_bottom = 0
                    padding_right = 0
                    padding=[]
                    if 'padding' in content[str(i)]:
                        padding = content[str(i)]
                        padding_top, padding_left, padding_bottom, padding_right = padding
                    else:
                        padding_top = content[str(i)].get('padding-top', 0)
                        padding_left = content[str(i)].get('padding-left', 0)
                        padding_bottom = content[str(i)].get('padding-bottom', 0)
                        padding_right = content[str(i)].get('padding-right', 0)

                    data_aux={
                        'text': content[str(i)]['text'], 
                        'color': content[str(i)].get('color', screen.COLOUR_WHITE), 
                        'bg': content[str(i)].get('bg', screen.COLOUR_DEFAULT), 
                        'position': content[str(i)].get('position', 'top_left_corner'),
                        'padding': padding,
                        'padding-top': padding_top,
                        'padding-left': padding_left,                        'padding-bottom': padding_bottom,
                        'padding-right': padding_right,
                        }
                    if 'button' in content[str(i)] and content[str(i)]['button']:
                        data_aux['button'] = content[str(i)]['button']
                    if 'event' in content[str(i)]:
                        data_aux['event'] = content[str(i)]['event']
                    if 'click' in content[str(i)]:
                        data_aux['click'] = content[str(i)]['click']
                    grid_cell.append(data_aux)
                else:
                    grid_cell.append([])
        
        posicion = 0

        for i in range(len(data_position['position_cell_divider_x'])):
            for j in range(len(data_position['position_cell_divider_y'])):
                text_cell = ''
                x=card['x_position'] + data_position['position_cell_divider_x'][i]
                y=card['y_position'] + data_position['position_cell_divider_y'][j]
                if posicion < grid_num_cells and grid_cell[posicion] != []:
                    text_cell = grid_cell[posicion]['text']
                    p=[grid_cell[posicion]['padding-top'], grid_cell[posicion]['padding-left'], grid_cell[posicion]['padding-bottom'], grid_cell[posicion]['padding-right']]
                    posicion_cell_x = [
                        x - data_position['grid_cell_width']+1+p[1]-p[3],
                        x - len(text_cell.split('\n'))+1+p[3]-p[1],
                        x - len(text_cell.split('\n')[0])+1+p[3]-p[1],
                    ]
                    posicion_cell_y = [
                        y - data_position['grid_cell_height']+1+p[0]-p[2],
                        y - len(text_cell.split('\n'))+1+p[2]-p[0],
                        y - len(text_cell.split('\n')[0])+1+p[2]-p[0],
                    ]
                else:
                    text_cell = ' '
                    posicion_cell_x = [
                        x - data_position['grid_cell_width']+1,
                        x - len(text_cell.split('\n'))+1,
                        x - len(text_cell.split('\n')[0])+1,                    ]
                    posicion_cell_y = [
                        y - data_position['grid_cell_height']+1,
                        y - len(text_cell.split('\n'))+1,
                        y - len(text_cell.split('\n')[0])+1
                    ]                # Definir posicion_cell para ambos casos
                posicion_cell = {
                    'top_left_corner': (posicion_cell_x[0], posicion_cell_y[0]),
                    'top_right_corner': (posicion_cell_x[1], posicion_cell_y[0]),                
                    'bottom_right_corner': (posicion_cell_x[2], posicion_cell_y[1]),
                    'bottom_left_corner': (posicion_cell_x[0], posicion_cell_y[2])
                }
                if posicion < grid_num_cells and grid_cell[posicion] != []:
                    # Determinar el tipo de elemento a renderizar
                    element_type = grid_cell[posicion].get('type', 'text')  # 'text', 'button', 'input', 'card'
                    
                    if element_type == 'button' or 'button' in grid_cell[posicion]:
                        # Renderizar botón
                        button_data = print_button(screen, {
                            'text': grid_cell[posicion]['text'],  # Usar el texto real del botón
                            'color': grid_cell[posicion]['color'],
                            'bg': grid_cell[posicion]['bg'],
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        }, event, grid_cell[posicion].get('click', None))
                        
                        # Guardar información completa del botón incluyendo si fue clickeado
                        buttons_return[posicion] = {
                            'clicked': button_data['result'] is not None,
                            'result': button_data['result'],
                            'text': grid_cell[posicion]['text'],  # Usar el texto real del botón
                            'width': button_data['width'],
                            'height': button_data['height'],
                            'x_position': button_data['x_position'],
                            'y_position': button_data['y_position']
                        }
                        
                    elif element_type == 'input':
                        # Renderizar input
                        input_config = grid_cell[posicion].copy()
                        input_config.update({
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        })
                        input_state = grid_cell[posicion].get('input_state', {
                            'value': '',
                            'cursor_pos': 0,
                            'is_focused': False,
                            'changed': False,
                            'clicked': False
                        })
                        input_result = print_input(screen, input_config, event, input_state)
                        buttons_return[posicion] = input_result
                        
                    elif element_type == 'card':
                        # Renderizar carta anidada
                        card_config = grid_cell[posicion].copy()
                        card_config.update({
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        })
                        card_result = print_card(screen, card_config, event, grid_cell[posicion].get('click', None))
                        buttons_return[posicion] = card_result
                        
                    else:
                        # Renderizar texto (comportamiento por defecto)
                        print_text(screen, {
                            'text': text_cell,
                            'color': grid_cell[posicion]['color'],
                            'bg': grid_cell[posicion]['bg'],
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        })
                posicion += 1
    # screen.refresh()
    result = None
    if grid_click == 'column' and grid and 'click' in data:
        result = []
        for i in range(len(data_position['position_cell_divider_x'])):
            # Calcular la posición de la columna
            x = card['x_position'] + len(grid_ascii_y) + (data_position['grid_cell_width'] + 1) * i
            y = card['y_position'] + len(grid_ascii_x)
            
            # Calcular el ancho y alto de la columna
            width = data_position['grid_cell_width'] - len(grid_ascii_x)
            height = card['height'] - (len(grid_ascii_x) * 2)- len(grid_ascii_y)
            
            row = {
                'x_position': x,
                'y_position': y,
                'width': width,
                'height': height            }
            if 'click' in data and str(i) in data['click']:
                click_column = data['click'][str(i)]
                aux = add_mouse_listener(
                    screen,
                    row,
                    click_column['event'],
                    click_column['click'],
                    click_column.get('test', False),
                    element_id=f"grid_column_{i}_{row['x_position']}_{row['y_position']}"
                )
                result.append(aux)

    # detectar clic en filas
    elif grid_click == 'row':
        result = []
        for i in range(len(data_position['position_cell_divider_y'])):
            # Calcular la posición de la fila
            x = card['x_position'] + len(grid_ascii_x)
            y = card['y_position'] + (data_position['grid_cell_height'] * i) + i + len(grid_ascii_y)

            # Calcular el ancho y alto de la fila
            width = card['width'] - (len(grid_ascii_y) * 2) - 1
            height = data_position['grid_cell_height'] - len(grid_ascii_x)

            row = {
                'x_position': x,
                'y_position': y,
                'width': width,
                'height': height            }
            
            if 'click' in data and str(i) in data['click']:
                click_row = data['click'][str(i)]
                aux = add_mouse_listener(
                    screen, 
                    row,
                    click_row['event'],
                    click_row['click'],
                    click_row.get('test', False),
                    element_id=f"grid_row_{i}_{row['x_position']}_{row['y_position']}"
                )
                result.append(aux)
    else:
        result = add_mouse_listener(screen, card, event, click, element_id=f"card_{card['x_position']}_{card['y_position']}") if click else None
    return {
        "result": result,
        "result_buttons": buttons_return,
        "width": width,
        "height": height,
        "x_position": card['x_position'],
        "y_position": card['y_position']
    }
    
def print_input(screen, data: dict, event=None, input_state=None) -> dict:
    """
    Renderiza un campo de entrada de texto independiente con manejo completo de eventos.
    
    Esta función crea un input completamente autónomo que maneja sus propios eventos de teclado
    y mouse usando add_key_listener y add_mouse_listener.
    
    Args:
        screen: Objeto Screen de asciimatics donde se imprimirá el input.
        data (dict): Diccionario de configuración del input:
            **Identificación (obligatorio):**
            - 'id' (str): ID único del input para manejo de estado.
            
            **Configuración Visual (obligatorio):**
            - 'label' (str): Etiqueta del campo (ej: "Usuario:", "Contraseña:").
            - 'width' (int): Ancho del contenedor del input.
            - 'height' (int): Alto del contenedor del input (mínimo 4).
            
            **Configuración de Comportamiento (opcional):**
            - 'is_password' (bool): Si es True, muestra asteriscos (*) en lugar del texto real.
            - 'max_length' (int): Longitud máxima permitida del texto (por defecto 50).
            - 'placeholder' (str): Texto de placeholder cuando está vacío.
            
            **Posicionamiento (opcional):**
            - 'x', 'x-center', 'x-right' (int): Posición horizontal.
            - 'y', 'y-center', 'y-bottom' (int): Posición vertical.
            
            **Estilo (opcional):**
            - 'color_focused' (int): Color cuando está enfocado (por defecto YELLOW).
            - 'color_normal' (int): Color cuando no está enfocado (por defecto WHITE).
            - 'bg' (int): Color de fondo (por defecto BLACK).
        
        event: Evento actual del sistema (para manejo de teclado y mouse).
        input_state (dict): Estado actual del input. Si es None, se inicializa automáticamente.
    
    Returns:
        dict: Diccionario con información del input:
            - 'input_state' (dict): Estado actual del input con:
                - 'value' (str): Valor actual del texto
                - 'cursor_pos' (int): Posición actual del cursor
                - 'is_focused' (bool): Si el input está enfocado
                - 'changed' (bool): Si el valor cambió en esta llamada
                - 'clicked' (bool): Si se hizo click en esta llamada
            - 'width' (int): Ancho del contenedor
            - 'height' (int): Alto del contenedor
            - 'x_position' (int): Posición X del contenedor
            - 'y_position' (int): Posición Y del contenedor
    
    Ejemplo de uso:
        # Inicializar estado del input
        user_input_state = None
        
        while True:
            screen.clear()
            
            # Renderizar input de usuario
            user_result = print_input(screen, {
                'id': 'usuario',
                'label': 'Usuario:',
                'width': 40,
                'height': 4,
                'x-center': 0,
                'y-center': -5,
                'max_length': 20
            }, event, user_input_state)
            
            # Actualizar estado
            user_input_state = user_result['input_state']
            
            screen.refresh()
            event = screen.get_event()
            
            # Verificar cambios
            if user_input_state['changed']:
                print(f"Usuario cambió a: {user_input_state['value']}")    """
    from .events import add_key_listener, add_mouse_listener
    from asciimatics.event import KeyboardEvent
    
    # Validaciones obligatorias
    if 'id' not in data:
        raise ValueError("El campo 'id' es obligatorio en print_input")
    if 'label' not in data:
        raise ValueError("El campo 'label' es obligatorio en print_input")
    if 'width' not in data:
        raise ValueError("El campo 'width' es obligatorio en print_input")
    if 'height' not in data:
        raise ValueError("El campo 'height' es obligatorio en print_input")
      # Configuración del input
    input_id = data['id']
    label = data['label']
    width = data['width']
    height = max(data['height'], 4)  # Mínimo 4 para label + input + bordes
    is_password = data.get('is_password', False)
    placeholder = data.get('placeholder', '')
    
    # Calcular max_length automáticamente basado en el ancho disponible
    # Ancho disponible = ancho total - bordes (2) - espacio para cursor (1)
    calculated_max_length = width - 1
    max_length = data.get('max_length', calculated_max_length)
    
    # Colores
    color_focused = data.get('color_focused', Screen.COLOUR_YELLOW)
    color_normal = data.get('color_normal', Screen.COLOUR_WHITE)
    bg = data.get('bg', Screen.COLOUR_BLACK)
    
    # Inicializar estado si no existe
    if input_state is None:
        input_state = {
            'value': '',
            'cursor_pos': 0,
            'is_focused': False,
            'changed': False,
            'clicked': False
        }
    
    # Resetear flags de eventos
    input_state['changed'] = False
    input_state['clicked'] = False
    
    # Determinar el color basado en el estado de focus
    current_color = color_focused if input_state['is_focused'] else color_normal
    
    # Crear el contenedor del input
    container_data = {
        'width': width,
        'height': height,
        'text': '',
        'color': current_color,
        'bg': bg
    }
    
    # Aplicar posicionamiento
    for pos_key in ['x', 'y', 'x-center', 'y-center', 'x-right', 'y-bottom', 'x_position', 'y_position']:
        if pos_key in data:
            container_data[pos_key] = data[pos_key]
    
    # Renderizar contenedor
    container = print_card(screen, container_data)
    
    # Función para manejar el focus
    def handle_focus():
        input_state['is_focused'] = True
        input_state['cursor_pos'] = len(input_state['value'])  # Cursor al final
        input_state['clicked'] = True
        return True
    
    # Agregar mouse listener para el focus
    add_mouse_listener(screen, container, event, handle_focus, element_id=f"input_{input_id}")
    
    # Solo procesar eventos de teclado si está enfocado
    if input_state['is_focused'] and event:
        
        # Función para mover cursor a la izquierda
        def handle_left_arrow():
            if input_state['cursor_pos'] > 0:
                input_state['cursor_pos'] -= 1
            return True
        
        # Función para mover cursor a la derecha
        def handle_right_arrow():
            if input_state['cursor_pos'] < len(input_state['value']):
                input_state['cursor_pos'] += 1
            return True
        
        # Función para borrar carácter con backspace
        def handle_backspace():
            if input_state['cursor_pos'] > 0:
                cursor_pos = input_state['cursor_pos']
                input_state['value'] = input_state['value'][:cursor_pos-1] + input_state['value'][cursor_pos:]
                input_state['cursor_pos'] -= 1
                input_state['changed'] = True
            return True
        
        # Función para entrada de caracteres
        def handle_character():
            if isinstance(event, KeyboardEvent) and 32 <= event.key_code <= 126:
                if len(input_state['value']) < max_length:
                    cursor_pos = input_state['cursor_pos']
                    char = chr(event.key_code)
                    input_state['value'] = input_state['value'][:cursor_pos] + char + input_state['value'][cursor_pos:]
                    input_state['cursor_pos'] += 1
                    input_state['changed'] = True
            return True
          # Agregar key listeners para eventos de teclado
        add_key_listener(-203, event, handle_left_arrow)      # Flecha izquierda
        add_key_listener(-205, event, handle_right_arrow)     # Flecha derecha
        add_key_listener(-300, event, handle_backspace)       # Backspace
        
        # Manejar entrada de caracteres normales
        if isinstance(event, KeyboardEvent) and 32 <= event.key_code <= 126:
            handle_character()
    
    # Renderizar label
    print_text(screen, {
        'text': label,
        'x_position': container['x_position'] + 1,
        'y_position': container['y_position'] + 1,
        'color': current_color
    })
    
    # Preparar texto a mostrar
    display_value = input_state['value'] if input_state['value'] else placeholder
    
    # Aplicar máscara de contraseña si es necesario
    if is_password and input_state['value']:
        display_value = '*' * len(input_state['value'])
    
    # Agregar cursor si está enfocado
    if input_state['is_focused']:
        cursor_pos = input_state['cursor_pos']
        if cursor_pos < len(display_value):
            display_value = display_value[:cursor_pos] + '|' + display_value[cursor_pos:]
        else:
            display_value += '|'
    
    # Renderizar el texto del input
    input_area_width = width - 2  # Restar bordes
    display_text = display_value.ljust(input_area_width)
    
    print_text(screen, {
        'text': display_text,
        'x_position': container['x_position'] + 1,
        'y_position': container['y_position'] + 2,
        'color': Screen.COLOUR_WHITE,
        'bg': bg
    })
    return {
        'input_state': input_state,
        'width': container['width'],
        'height': container['height'],
        'x_position': container['x_position'],
        'y_position': container['y_position'],
        'clicked': input_state['clicked'],  # Agregar información del clic
        'changed': input_state['changed']   # Agregar información de cambios
    }

def print_form(screen, form_config: dict, event=None) -> dict:
    """
    Función avanzada para crear formularios dinámicos con inputs, botones y navegación automática.
    
    Permite crear formularios complejos usando configuración declarativa, con soporte para:
    - Inputs de texto y contraseña
    - Botones con funciones personalizadas
    - Contenedores opcionales (print_card)
    - Navegación automática con TAB
    - Validación de campos
    - Manejo de eventos de teclado y mouse
    
    Args:
        screen: Objeto Screen de asciimatics
        form_config (dict): Configuración del formulario con las siguientes claves:
            
            **Configuración General:**
            - 'title' (str, opcional): Título del formulario
            - 'title_config' (dict, opcional): Configuración del título (usa print_text)
            - 'position' (dict, opcional): Posición del formulario {'x': int, 'y': int, 'x-center': int, 'y-center': int}
            
            **Contenedor (opcional):**
            - 'container' (dict, opcional): Configuración del contenedor usando print_card
              Si se especifica, todos los elementos se posicionarán relativos al contenedor
            
            **Campos de entrada:**
            - 'inputs' (dict): Diccionario con configuración de inputs
              Clave: ID del input
              Valor: Configuración del input (usa print_input)
              
            **Botones:**
            - 'buttons' (dict, opcional): Configuración de botones
              Puede ser:
              1. Diccionario simple: cada clave es ID del botón, valor es configuración
              2. Configuración de print_card con grid para botones organizados
              
            **Navegación:**
            - 'navigation_order' (list, opcional): Orden de navegación con TAB
              Si no se especifica, usa el orden: inputs (alfabético) + botones (alfabético)
            - 'initial_focus' (str, opcional): ID del campo con focus inicial
            
            **Validación:**
            - 'validation' (dict, opcional): Reglas de validación por campo
              Formato: {'campo_id': {'required': bool, 'min_length': int, 'max_length': int, 'custom': function}}
            
            **Eventos personalizados:**
            - 'key_handlers' (dict, opcional): Manejadores personalizados de teclas
              Formato: {tecla_codigo: función}
        
        event: Evento actual del sistema
    
    Returns:
        dict: Resultado del formulario con:
            - 'form_state' (dict): Estado actual del formulario
                - 'current_field' (str): Campo actualmente enfocado
                - 'form_data' (dict): Datos de todos los inputs
                - 'result' (dict o None): Resultado si el formulario se completó
                - 'show_error' (bool): Si hay error visible
                - 'error_message' (str): Mensaje de error actual
            - 'position' (dict): Información de posición y tamaño
                - 'x' (int): Posición X del formulario
                - 'y' (int): Posición Y del formulario
                - 'width' (int): Ancho total del formulario
                - 'height' (int): Alto total del formulario
            - 'inputs_data' (dict): Estados detallados de todos los inputs
    
    Ejemplo de uso básico:
        form_config = {
            'title': 'LOGIN',
            'title_config': {
                'font': 'slant',
                'color': Screen.COLOUR_CYAN,
                'x-center': 0,
                'y': 2
            },
            'container': {
                'width': 50,
                'height': 18,
                'x-center': 0,
                'y-center': 0
            },
            'inputs': {
                'usuario': {
                    'label': 'Usuario:',
                    'width': 44,
                    'height': 4,
                    'x-center': 0,
                    'y-center': -4,
                    'placeholder': 'Ingresa tu usuario'
                },
                'password': {
                    'label': 'Contraseña:',
                    'width': 44,
                    'height': 4,
                    'x-center': 0,
                    'y-center': 0,
                    'placeholder': 'Ingresa tu contraseña',
                    'is_password': True
                }
            },
            'buttons': {
                'grid': True,
                'width': 40,
                'height': 3,
                'x-center': 0,
                'y-center': 5,
                'grid_divider_x': 2,
                'grid_divider_y': 1,
                'content': {
                    '0': {
                        'text': 'INICIAR SESIÓN',
                        'button': True,
                        'action': 'submit'
                    },
                    '1': {
                        'text': 'CANCELAR',
                        'button': True,
                        'action': 'cancel'
                    }
                }
            },
            'validation': {
                'usuario': {'required': True, 'min_length': 3},
                'password': {'required': True, 'min_length': 4}
            }
        }
        
        result = print_form(screen, form_config, event)
        
        if result['form_state']['result']:
            action = result['form_state']['result']['action']
            if action == 'submit':
                user_data = result['form_state']['form_data']
                print(f"Usuario: {user_data['usuario']}, Password: {user_data['password']}")    """
    from .events import add_key_listener
    from asciimatics.event import MouseEvent
    
    # Inicializar estado del formulario si no existe
    if not hasattr(print_form, '_form_states'):
        print_form._form_states = {}
    
    form_id = id(form_config)  # Usar ID del objeto como identificador único
    
    if form_id not in print_form._form_states:
        # Inicializar estado del formulario
        inputs_config = form_config.get('inputs', {})
        navigation_order = form_config.get('navigation_order', [])
        
        # Si no se especifica orden de navegación, usar orden alfabético
        if not navigation_order:
            navigation_order = sorted(inputs_config.keys())
            if 'buttons' in form_config:
                buttons_config = form_config['buttons']
                if isinstance(buttons_config, dict) and 'content' in buttons_config:
                    # Botones en grid
                    button_ids = [f"btn_{key}" for key in sorted(buttons_config['content'].keys())]
                    navigation_order.extend(button_ids)
                else:
                    # Botones simples
                    navigation_order.extend([f"btn_{key}" for key in sorted(buttons_config.keys())])
        
        initial_focus = form_config.get('initial_focus', navigation_order[0] if navigation_order else '')
        
        # Crear estados de inputs
        input_states = {}
        for input_id in inputs_config.keys():
            input_states[input_id] = {
                'value': '',
                'cursor_pos': 0,
                'is_focused': (input_id == initial_focus),
                'changed': False,
                'clicked': False
            }
        
        print_form._form_states[form_id] = {
            'current_field': initial_focus,
            'navigation_order': navigation_order,
            'input_states': input_states,
            'show_error': False,
            'error_message': '',
            'result': None,
            'form_data': {}
        }
    
    form_state = print_form._form_states[form_id]
    
    # Variables para almacenar información de posición
    form_position = {'x': 0, 'y': 0, 'width': 0, 'height': 0}
    inputs_data = {}
    last_mouse_event = None
    
    # Guardar último evento de mouse
    if isinstance(event, MouseEvent):
        last_mouse_event = event
    
    # 1. Renderizar título si existe
    if 'title' in form_config:
        title_config = form_config.get('title_config', {})
        title_config['text'] = form_config['title']
        print_text(screen, title_config, asccii_art=title_config.get('font') is not None)
    
    # 2. Renderizar contenedor si existe
    container_result = None
    if 'container' in form_config:
        container_result = print_card(screen, form_config['container'])
        form_position.update({
            'x': container_result['x_position'],
            'y': container_result['y_position'],
            'width': container_result['width'],
            'height': container_result['height']
        })
    
    # 3. Renderizar inputs
    for input_id, input_config in form_config.get('inputs', {}).items():
        # Configurar colores basados en el estado de focus
        if form_state['current_field'] == input_id:
            input_config['color_focused'] = input_config.get('color_focused', Screen.COLOUR_YELLOW)
            input_config['color_normal'] = input_config.get('color_normal', Screen.COLOUR_WHITE)
        else:
            input_config['color_focused'] = input_config.get('color_normal', Screen.COLOUR_WHITE)
            input_config['color_normal'] = input_config.get('color_normal', Screen.COLOUR_WHITE)
        
        # Asegurar que el input tenga ID
        input_config['id'] = input_id
        
        # Renderizar input
        input_result = print_input(screen, input_config, event, form_state['input_states'][input_id])
        
        # Actualizar estado del input
        form_state['input_states'][input_id] = input_result['input_state']
        inputs_data[input_id] = input_result
        
        # Actualizar datos del formulario
        form_state['form_data'][input_id] = input_result['input_state']['value']
        
        # Detectar clicks para cambiar focus
        if input_result['input_state']['clicked']:
            form_state['current_field'] = input_id
            form_state['show_error'] = False
            # Actualizar focus de todos los inputs
            for iid in form_state['input_states']:
                form_state['input_states'][iid]['is_focused'] = (iid == input_id)
    
    # 4. Renderizar botones
    button_results = {}
    if 'buttons' in form_config:
        buttons_config = form_config['buttons']
        
        if isinstance(buttons_config, dict) and 'content' in buttons_config:
            # Botones en grid usando print_card
            # Actualizar colores y eventos para cada botón
            for btn_key, btn_config in buttons_config['content'].items():
                btn_id = f"btn_{btn_key}"
                
                # Configurar colores basados en focus
                if form_state['current_field'] == btn_id:
                    btn_config['color'] = btn_config.get('color_focused', Screen.COLOUR_GREEN)
                    btn_config['bg'] = btn_config.get('bg_focused', Screen.COLOUR_GREEN)
                else:
                    btn_config['color'] = btn_config.get('color_normal', Screen.COLOUR_WHITE)
                    btn_config['bg'] = btn_config.get('bg_normal', Screen.COLOUR_BLACK)
                
                # Agregar evento
                btn_config['event'] = last_mouse_event
                
                # Crear función de click si no existe
                if 'action' in btn_config and 'click' not in btn_config:
                    action = btn_config['action']
                    if action == 'submit':
                        btn_config['click'] = lambda: _handle_submit(form_state, form_config)
                    elif action == 'cancel':
                        btn_config['click'] = lambda: _handle_cancel(form_state)
                    else:
                        # Acción personalizada
                        btn_config['click'] = lambda a=action: _handle_custom_action(form_state, a)
            
            # Renderizar botones usando print_card
            buttons_result = print_card(screen, buttons_config, last_mouse_event)
            button_results.update(buttons_result.get('result_buttons', {}))
            
        else:
            # Botones simples
            for btn_id, btn_config in buttons_config.items():
                full_btn_id = f"btn_{btn_id}"
                
                # Configurar colores basados en focus
                if form_state['current_field'] == full_btn_id:
                    btn_config['color'] = btn_config.get('color_focused', Screen.COLOUR_GREEN)
                    btn_config['bg'] = btn_config.get('bg_focused', Screen.COLOUR_GREEN)
                else:
                    btn_config['color'] = btn_config.get('color_normal', Screen.COLOUR_WHITE)
                    btn_config['bg'] = btn_config.get('bg_normal', Screen.COLOUR_BLACK)
                
                # Crear función de click si no existe
                if 'action' in btn_config and 'click' not in btn_config:
                    action = btn_config['action']
                    if action == 'submit':
                        btn_config['click'] = lambda: _handle_submit(form_state, form_config)
                    elif action == 'cancel':
                        btn_config['click'] = lambda: _handle_cancel(form_state)
                    else:
                        btn_config['click'] = lambda a=action: _handle_custom_action(form_state, a)
                
                # Renderizar botón
                btn_result = print_button(screen, btn_config, event, btn_config.get('click'))
                button_results[btn_id] = btn_result['result']
    
    # 5. Mostrar errores si existen
    if form_state['show_error']:
        error_config = {
            'text': f"❌ {form_state['error_message']}",
            'x-center': 0,
            'y-center': 8,
            'color': Screen.COLOUR_RED
        }
        print_text(screen, error_config)
    
    # 6. Verificar si se presionaron botones
    for btn_key, btn_result in button_results.items():
        if btn_result:
            # Un botón fue presionado, su función click ya fue ejecutada
            pass
    
    # 7. Manejo de navegación con TAB
    def handle_tab():
        if form_state['navigation_order']:
            current_index = form_state['navigation_order'].index(form_state['current_field'])
            next_index = (current_index + 1) % len(form_state['navigation_order'])
            form_state['current_field'] = form_state['navigation_order'][next_index]
            form_state['show_error'] = False
            
            # Actualizar focus de inputs
            for input_id in form_state['input_states']:
                form_state['input_states'][input_id]['is_focused'] = (input_id == form_state['current_field'])

    def handle_enter():
        form_state['show_error'] = False
        current = form_state['current_field']
        
        if current.startswith('btn_'):
            # Es un botón, ejecutar su acción
            if current == 'btn_0' or 'submit' in current:
                return _handle_submit(form_state, form_config)
            elif current == 'btn_1' or 'cancel' in current:
                return _handle_cancel(form_state)
        else:
            # Es un input, ir al siguiente campo
            if form_state['navigation_order']:
                current_index = form_state['navigation_order'].index(current)
                next_index = (current_index + 1) % len(form_state['navigation_order'])
                form_state['current_field'] = form_state['navigation_order'][next_index]
                
                # Actualizar focus
                for input_id in form_state['input_states']:
                    form_state['input_states'][input_id]['is_focused'] = (input_id == form_state['current_field'])
        return False

    def handle_escape():
        return _handle_cancel(form_state)

    # 8. Aplicar manejadores de eventos
    result = add_key_listener(-301, event, handle_tab)  # TAB
    if result:
        pass  # Continue normal flow
        
    result = add_key_listener([10, 13], event, handle_enter)  # ENTER
    if result:
        pass  # Continue normal flow
        
    result = add_key_listener(-1, event, handle_escape)  # ESCAPE
    if result:
        pass  # Continue normal flow
    
    # 9. Manejadores personalizados de teclas
    if 'key_handlers' in form_config:
        for key_code, handler in form_config['key_handlers'].items():
            result = add_key_listener(key_code, event, handler)
            if result:
                pass
    
    # Calcular posición y tamaño del formulario si no se definió por contenedor
    if not container_result:
        # Calcular basado en los elementos renderizados
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for input_data in inputs_data.values():
            min_x = min(min_x, input_data['x_position'])
            min_y = min(min_y, input_data['y_position'])
            max_x = max(max_x, input_data['x_position'] + input_data['width'])
            max_y = max(max_y, input_data['y_position'] + input_data['height'])
        
        if min_x != float('inf'):
            form_position.update({
                'x': min_x,
                'y': min_y,
                'width': max_x - min_x,
                'height': max_y - min_y
            })
    
    return {
        'form_state': form_state,
        'position': form_position,
        'inputs_data': inputs_data
    }

def _handle_submit(form_state, form_config):
    """Maneja el envío del formulario con validación"""
    validation_config = form_config.get('validation', {})
    
    # Validar campos
    for field_id, rules in validation_config.items():
        if field_id in form_state['form_data']:
            value = form_state['form_data'][field_id].strip()
            
            if rules.get('required', False) and not value:
                form_state['error_message'] = f'El campo {field_id} es requerido'
                form_state['show_error'] = True
                return False
            
            min_length = rules.get('min_length')
            if min_length and len(value) < min_length:
                form_state['error_message'] = f'El campo {field_id} debe tener al menos {min_length} caracteres'
                form_state['show_error'] = True
                return False
            
            max_length = rules.get('max_length')
            if max_length and len(value) > max_length:
                form_state['error_message'] = f'El campo {field_id} no puede tener más de {max_length} caracteres'
                form_state['show_error'] = True
                return False
            
            custom_validator = rules.get('custom')
            if custom_validator and not custom_validator(value):
                form_state['error_message'] = f'El campo {field_id} no es válido'
                form_state['show_error'] = True
                return False
    
    # Si llegamos aquí, la validación pasó
    form_state['result'] = {
        'action': 'submit',
        'data': form_state['form_data'].copy()
    }
    return True

def _handle_cancel(form_state):
    """Maneja la cancelación del formulario"""
    form_state['result'] = {'action': 'cancel'}
    return True

def _handle_custom_action(form_state, action):
    """Maneja acciones personalizadas"""
    form_state['result'] = {
        'action': action,
        'data': form_state['form_data'].copy()
    }
    return True
