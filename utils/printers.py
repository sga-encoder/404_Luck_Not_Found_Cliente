from asciimatics.screen import Screen
from pyfiglet import Figlet

from utils.helpers import create_card


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
    from utils.events import add_mouse_listener  # Importación local para evitar ciclo

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
    from utils.events import add_mouse_listener  # Importación local para evitar ciclo

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
    """
    # establecer valores por defecto o usar los proporcionados en el diccionario data
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
    max_width = data.get('max-width', 100)
    grid_ascii_x = data.get('grid_ascii_x', ascii_x)
    grid_ascii_y = data.get('grid_ascii_y', ascii_y)
    grid_intersections = data.get('grid_intersection', ['┼', '┬', '┴', '├', '┤'])
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
                        'padding-left': padding_left,
                        'padding-bottom': padding_bottom,
                        'padding-right': padding_right,
                        }
                    if 'button' in content[str(i)] and content[str(i)]['button']:
                        data_aux['button'] = content[str(i)]['button']
                    if 'event' in content[str(i)]:
                        data_aux['event'] = content[str(i)]['event']
                    if 'click' in content[str(i)]:
                        data_aux = content[str(i)]['click']
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
                        x - len(text_cell.split('\n')[0])+1,
                    ]
                    posicion_cell_y = [
                        y - data_position['grid_cell_height']+1,
                        y - len(text_cell.split('\n'))+1,
                        y - len(text_cell.split('\n')[0])+1
                    ]

                posicion_cell = {
                    'top_left_corner': (posicion_cell_x[0], posicion_cell_y[0]),
                    'top_right_corner': (posicion_cell_x[1], posicion_cell_y[0]),
                    'bottom_right_corner': (posicion_cell_x[2], posicion_cell_y[1]),
                    'bottom_left_corner': (posicion_cell_x[0], posicion_cell_y[2])
                }
                
                if posicion < grid_num_cells and grid_cell[posicion] != []:
                    if 'button' in grid_cell[posicion]:
                        print_button(screen, {
                            'text': text_cell,
                            'color': grid_cell[posicion]['color'],
                            'bg': grid_cell[posicion]['bg'],
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        }, grid_cell[posicion]['event'] if 'event' in grid_cell[posicion] else None, grid_cell[posicion]['click'] if 'click' in grid_cell[posicion] else None)
                    else:
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
                'height': height
            }
            if str(i) in data['click']:
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
                'height': height
            }
            
            if str(i) in data['click']:
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
                print(f"Usuario cambió a: {user_input_state['value']}")
    """
    from utils.events import add_key_listener, add_mouse_listener
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
