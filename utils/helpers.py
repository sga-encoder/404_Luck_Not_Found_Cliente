def filler_text(text, filler, width, posicion='center') -> str:
    text_long = len(text)
    total_fill = int(width - text_long)
    left = int(total_fill // 2)
    right = int(total_fill - left)
    if posicion == 'center':
        return (filler * left) + text + (filler * right)
    elif posicion == 'left':
        return text + (filler * int(total_fill))
    elif posicion == 'right':
        return (filler * int(total_fill)) + text

def create_card(data: dict) -> str:
    width = data['width'] if 'width' in data else 21
    height = data['height'] if 'height' in data else 13
    text = data['text'] if 'text' in data else ''
    ascii_y = data['ascii_y'] if 'ascii_y' in data else '│'
    ascii_x = data['ascii_x'] if 'ascii_x' in data else '─'
    corner = data['corner'] if 'corner' in data else ['╭', '╮', '╰', '╯']
    
    grid = data['grid'] if 'grid' in data else False
    grid_ascii_x = data['grid_ascii_x'] if 'grid_ascii_x' in data else ascii_x
    grid_ascii_y = data['grid_ascii_y'] if 'grid_ascii_y' in data else ascii_y
    grid_intersections = data['grid_intersections'] if 'grid_intersections' in data else ['┼', '┬', '┴', '├', '┤']
    grid_corners = data['grid_corners'] if 'grid_corners' in data else corner  # Bordes específicos para grid
    grid_divider_x = data['grid_divider_x'] if 'grid_divider_x' in data else 2
    grid_divider_y = data['grid_divider_y'] if 'grid_divider_y' in data else 2
    grid_cell_width = (width) // grid_divider_x
    grid_cell_height = (height) // grid_divider_y
    height = height + grid_divider_y - 1 if grid else height

    # Dividir el texto en líneas para ajustarlo al ancho de la carta
    palabras = text.split(' ')
    text_line = []
    linea_actual = ''
    for palabra in palabras:
        if len(linea_actual + ' ' + palabra) <= width:
            if linea_actual:
                linea_actual += ' '
            linea_actual += palabra
        else:
            text_line.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        text_line.append(linea_actual)    # Centramos verticalmente el bloque de texto
    lineas_texto = len(text_line)
    lineas_vacias_arriba = (height - 2 - lineas_texto) // 2
    lineas_vacias_abajo = height - 2 - lineas_texto - lineas_vacias_arriba

    card_text = ''
    # Línea superior
    contador = 0
    position_cell_divider_x = []
    position_cell_divider_y = []
    for i in range(1, grid_divider_x):
        position_cell_divider_x.append((i * grid_cell_width)+ i-1)
        
    for i in range(1, grid_divider_y ):
        position_cell_divider_y.append((i * grid_cell_height)+ i-1)

    if grid:
        text_grid = ''
        for i in range(grid_divider_x):
            if i == grid_divider_x -1:
                text_grid += filler_text('', ascii_x, grid_cell_width, 'center')
            else:
                text_grid += filler_text('', ascii_x, grid_cell_width, 'center') + grid_intersections[1]
        card_text += grid_corners[0] + text_grid + grid_corners[1] + '\n'
        for i in range(height):
            text_grid = ''
            # Solo accedemos si hay más divisiones
            if contador < len(position_cell_divider_y) and i == position_cell_divider_y[contador]:
                for j in range(grid_divider_x):
                    if j == grid_divider_x -1:
                        text_grid += filler_text('', grid_ascii_x, grid_cell_width, 'center')
                    else:
                        text_grid += filler_text('', grid_ascii_x, grid_cell_width, 'center') + grid_intersections[0]
                card_text += grid_intersections[3] + text_grid + grid_intersections[4] + '\n'
                contador += 1  # Incrementar el contador para la siguiente división
            else:
                for j in range(grid_divider_x):
                    if j == grid_divider_x -1:
                        text_grid += filler_text('', ' ', grid_cell_width, 'center')
                    else:
                        text_grid += filler_text('', ' ', grid_cell_width, 'center') + grid_ascii_y
                card_text += ascii_y + text_grid + ascii_y + '\n'
                
        text_grid = ''
        for i in range(grid_divider_x):
            if i == grid_divider_x -1:
                text_grid += filler_text('', ascii_x, grid_cell_width, 'center')
            else:
                text_grid += filler_text('', ascii_x, grid_cell_width, 'center') + grid_intersections[2]
        card_text += grid_corners[2] + text_grid + grid_corners[3]
    else:
        card_text += corner[0] + filler_text('', ascii_x, width - (len(corner[0]) + len(corner[1])) + (2 * len(ascii_y)), 'center') + corner[1] + '\n'
        for _ in range(lineas_vacias_arriba):
            card_text += ascii_y + filler_text('', ' ', width, 'center') + ascii_y + '\n'
        for linea in text_line:
            card_text += ascii_y + filler_text(linea.strip(), ' ', width, 'center') + ascii_y + '\n'
            
        for _ in range(lineas_vacias_abajo):
            card_text += ascii_y + filler_text('', ' ', width, 'center') + ascii_y + '\n'
            
        card_text += corner[2] + filler_text('', ascii_x, width - (len(corner[2]) + len(corner[3])) + (2 * len(ascii_y)), 'center') + corner[3]

    position_cell_divider_x = []
    position_cell_divider_y = []
    for i in range(1, grid_divider_x + 1):
        position_cell_divider_x.append((i * grid_cell_width)+ i-1)
        
    for i in range(1, grid_divider_y + 1):
        position_cell_divider_y.append((i * grid_cell_height)+ i-1)
    if grid:
        return {
            'text': card_text,
            'data':{
                'grid_divider_x': grid_divider_x,
                'grid_divider_y': grid_divider_y,
                'grid_cell_width': grid_cell_width,
                'grid_cell_height': grid_cell_height,
                'position_cell_divider_x': position_cell_divider_x,
                'position_cell_divider_y': position_cell_divider_y
            }
        }
    else:
        return card_text

def font_tester(text, pagina=0):
    import pyfiglet
    fonts = pyfiglet.FigletFont.getFonts()
    p = [[0, 60], [60, 120], [120, 180], [180, 240], [240, 300], [300, 360], [360, 420], [420, 480], [480, 540], [540, len(fonts)]]
    font_texts = {}
    for i in range(p[pagina][0], p[pagina][1]):
        font_name = fonts[i]
        try:
            figlet = pyfiglet.Figlet(font=font_name, width=150, justify='center')
            font_texts[font_name] = figlet.renderText(text)
            print(f"Font: {font_name}")
            print(figlet.renderText(text))
        except Exception as e:
            font_texts[font_name] = f"Error: {str(e)}"
    # print(font_texts)
    
def font_tester_recomded(text):
    import pyfiglet
    recommended_fonts = [
        'cosmic',
        'delta_corps_priest_1',
        'dos_rebel',
        'elite',
        'georgia11',
        'modular',
        'ogre',
        'patorjk-hex',
        'starwars',
        'this',
        'whimsy',
        'banner3-D',
        'big_money-ne'
    ]
    font_texts = {}
    for font in recommended_fonts:
        try:
            figlet = pyfiglet.Figlet(font=font, width=150, justify='center')
            print(f"Font: {font}")
            print(figlet.renderText(text))
        except Exception as e:
            font_texts[font] = f"Error: {str(e)}"

