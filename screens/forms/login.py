from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent, MouseEvent
from ...utils.events import add_key_listener, key_listener_test, add_mouse_listener
from ...utils.printers import print_text, print_button, print_card, print_input


def login_form(screen):
    """
    Formulario de login completo con campos de entrada independientes.
    
    Características:
    - Campos de entrada completamente autónomos usando print_input
    - Navegación con Tab entre campos
    - Soporte para teclado y mouse
    - Validación de campos
    - Manejo de eventos independiente para cada input
    """
    screen.clear()
    screen.mouse = True
    
    # Estados independientes para cada campo de entrada
    usuario_state = {
        'value': '',
        'cursor_pos': 0,
        'is_focused': True,  # Usuario comienza enfocado
        'changed': False,
        'clicked': False
    }
    
    password_state = {
        'value': '',
        'cursor_pos': 0,
        'is_focused': False,
        'changed': False,
        'clicked': False
    }
    
    # Estado del formulario
    form_state = {
        'current_field': 'usuario',  # 'usuario', 'password', 'login_btn', 'cancel_btn'
        'show_error': False,
        'error_message': '',
        'result': None
    }
    
    def validate_form():
        """Valida los campos del formulario"""
        if not usuario_state['value'].strip():
            form_state['error_message'] = 'El usuario es requerido'
            form_state['show_error'] = True
            return False
        if not password_state['value'].strip():
            form_state['error_message'] = 'La contraseña es requerida'
            form_state['show_error'] = True
            return False
        if len(usuario_state['value']) < 3:
            form_state['error_message'] = 'El usuario debe tener al menos 3 caracteres'
            form_state['show_error'] = True
            return False
        if len(password_state['value']) < 4:
            form_state['error_message'] = 'La contraseña debe tener al menos 4 caracteres'
            form_state['show_error'] = True
            return False
        return True
    
    def handle_login():
        """Maneja el intento de login"""
        if validate_form():
            form_state['result'] = {
                'action': 'login',
                'usuario': usuario_state['value'],
                'password': password_state['value']
            }
            return True
        return False
    
    def handle_cancel():
        """Maneja la cancelación del formulario"""
        form_state['result'] = {'action': 'cancel'}
        return True
    
    # Variable para almacenar el último evento de mouse
    last_mouse_event = None
    
    while form_state['result'] is None:
        # Título del formulario
        print_text(screen, {
            'text': 'INICIAR SESIÓN',
            'x-center': 0,
            'y': 2,
            'max-width': 75,
            'font': 'slant',
            'justify': 'center',
            'color': Screen.COLOUR_CYAN
        }, asccii_art=True)
        
        # Contenedor principal del formulario
        container_form = print_card(screen, {
            'width': 50,
            'height': 18,
            'x-center': 0,
            'y-center': 0,
            'text': '',
            'color': Screen.COLOUR_WHITE,
            'corner': ['╭', '╮', '╰', '╯'],
            'ascii_x': '─',
            'ascii_y': '│'
        })
        
        # Obtener evento para pasar a los inputs
        event = screen.get_event()
        
        # Guardar último evento de mouse
        if isinstance(event, MouseEvent):
            last_mouse_event = event        # Campo de entrada Usuario usando print_input
        usuario_result = print_input(screen, {
            'id': 'usuario',
            'label': 'Usuario:',
            'x-center': 0,
            'y-center': -4,
            'width': 44,
            'height': 4,
            'placeholder': 'Ingresa tu usuario',
            'border_color': Screen.COLOUR_YELLOW if form_state['current_field'] == 'usuario' else Screen.COLOUR_WHITE,
            'text_color': Screen.COLOUR_WHITE,
            'bg_color': Screen.COLOUR_BLACK
        }, event, usuario_state)
          # Campo de entrada Contraseña usando print_input
        password_result = print_input(screen, {
            'id': 'password',
            'label': 'Contraseña:',
            'x-center': 0,
            'y-center': 0,
            'width': 44,
            'height': 4,
            'placeholder': 'Ingresa tu contraseña',
            'is_password': True,
            'border_color': Screen.COLOUR_YELLOW if form_state['current_field'] == 'password' else Screen.COLOUR_WHITE,
            'text_color': Screen.COLOUR_WHITE,
            'bg_color': Screen.COLOUR_BLACK
        }, event, password_state)
          # Actualizar el estado de focus basado en los clicks
        click_detected = False
        if usuario_result and usuario_result.get('clicked'):
            form_state['current_field'] = 'usuario'
            usuario_state['is_focused'] = True
            password_state['is_focused'] = False
            form_state['show_error'] = False
            click_detected = True
        elif password_result and password_result.get('clicked'):
            form_state['current_field'] = 'password'
            usuario_state['is_focused'] = False
            password_state['is_focused'] = True
            form_state['show_error'] = False
            click_detected = True
        
        # Solo actualizar estado de focus automáticamente si NO se detectó un click
        if not click_detected:
            usuario_state['is_focused'] = (form_state['current_field'] == 'usuario')
            password_state['is_focused'] = (form_state['current_field'] == 'password')
        
        # Botón Login
        login_btn_result = print_button(screen, {
            'text': '  INICIAR SESIÓN  ',
            'x-center': -12,
            'y-center': 5,
            'color': Screen.COLOUR_GREEN if form_state['current_field'] == 'login_btn' else Screen.COLOUR_WHITE,
            'bg': Screen.COLOUR_GREEN if form_state['current_field'] == 'login_btn' else Screen.COLOUR_BLACK
        }, last_mouse_event, handle_login)
        
        # Botón Cancelar
        cancel_btn_result = print_button(screen, {
            'text': '  CANCELAR  ',
            'x-center': 8,
            'y-center': 5,
            'color': Screen.COLOUR_RED if form_state['current_field'] == 'cancel_btn' else Screen.COLOUR_WHITE,
            'bg': Screen.COLOUR_RED if form_state['current_field'] == 'cancel_btn' else Screen.COLOUR_BLACK
        }, last_mouse_event, handle_cancel)
        
        # Mostrar error si existe
        if form_state['show_error']:
            print_text(screen, {
                'text': f"❌ {form_state['error_message']}",
                'x-center': 0,
                'y-center': 8,
                'color': Screen.COLOUR_RED
            })
        
        # Instrucciones
        print_text(screen, {
            'text': 'TAB: Cambiar campo | ENTER: Aceptar | ESC: Cancelar',
            'x-center': 0,
            'y-center': 10,
            'color': Screen.COLOUR_CYAN
        })
        
        # Área de debug - Campo actual
        print_text(screen, {
            'text': f"Campo actual: {form_state['current_field']}",
            'x-center': 0,
            'y-center': -9,
            'color': Screen.COLOUR_YELLOW
        })
        
        screen.refresh()
        
        # Verificar si se presionaron los botones
        if login_btn_result['result']:
            if handle_login():
                break
        
        if cancel_btn_result['result']:
            if handle_cancel():
                break
        
        # Manejo de navegación con TAB
        def handle_tab():
            fields = ['usuario', 'password', 'login_btn', 'cancel_btn']
            current_index = fields.index(form_state['current_field'])
            form_state['current_field'] = fields[(current_index + 1) % len(fields)]
            form_state['show_error'] = False
            
            # Actualizar focus de los inputs
            usuario_state['is_focused'] = (form_state['current_field'] == 'usuario')
            password_state['is_focused'] = (form_state['current_field'] == 'password')

        def handle_enter():
            form_state['show_error'] = False
            if form_state['current_field'] == 'login_btn':
                return handle_login()
            elif form_state['current_field'] == 'cancel_btn':
                return handle_cancel()
            else:
                # En un campo de texto, cambiar al siguiente
                if form_state['current_field'] == 'usuario':
                    form_state['current_field'] = 'password'
                    usuario_state['is_focused'] = False
                    password_state['is_focused'] = True
                elif form_state['current_field'] == 'password':
                    form_state['current_field'] = 'login_btn'
                    password_state['is_focused'] = False
            return False

        def handle_escape():
            return handle_cancel()

        def handle_exit():
            form_state['result'] = {'action': 'exit'}
            return True
        
        # Usar add_key_listener para manejar eventos globales de navegación
        # TAB - cambiar campo
        result = add_key_listener(-301, event, handle_tab)
        if result:
            continue
            
        # ENTER - aceptar/siguiente campo
        result = add_key_listener([10, 13], event, handle_enter)
        if result:
            if result is True:  # Si retorna True, salir del bucle
                break
            continue
            
        # ESCAPE - cancelar
        result = add_key_listener(-1, event, handle_escape)
        if result:
            break
            
        # Tecla F - salir
        result = add_key_listener([102, 70], event, handle_exit)
        if result:
            break

    return form_state['result']


def simple_input_field(screen, x, y, width, value, is_password=False, is_focused=False):
    """
    Función auxiliar para renderizar un campo de entrada simple
    """
    display_value = '*' * len(value) if is_password else value
    
    # Fondo del campo
    color = Screen.COLOUR_YELLOW if is_focused else Screen.COLOUR_WHITE
    
    print_card(screen, {
        'width': width + 2,
        'height': 3,
        'x': x,
        'y': y,
        'text': '',
        'color': color,
        'bg': Screen.COLOUR_BLACK
    })
    
    # Texto del campo
    display_text = display_value.ljust(width-2)
    if is_focused:
        display_text += '|'  # Cursor
    
    print_text(screen, {
        'text': display_text,
        'x': x + 1,
        'y': y + 1,
        'color': Screen.COLOUR_WHITE,
        'bg': Screen.COLOUR_BLACK
    })