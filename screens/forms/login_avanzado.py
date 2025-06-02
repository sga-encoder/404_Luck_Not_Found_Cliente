from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent, MouseEvent
from utils.events import add_key_listener
from utils.printers import print_text, print_button, print_card, print_input


def advanced_login_form(screen):
    """
    Formulario de login avanzado con características mejoradas.
    
    Características:
    - Validación en tiempo real
    - Indicadores visuales de estado
    - Opción "Recordar usuario"
    - Mostrar/ocultar contraseña
    - Barra de progreso de completitud
    - Mejor experiencia de usuario
    """
    screen.clear()
    screen.mouse = True
    
    # Estado del formulario
    form_state = {
        'show_error': False,
        'error_message': '',
        'result': None,
        'show_password': False,
        'remember_user': False
    }
    
    # Estados de los inputs para print_input
    usuario_input_state = None
    password_input_state = None
    
    max_length = {'usuario': 20, 'password': 15}
    
    def validate_field(field, value):
        """Valida un campo específico en tiempo real"""
        if field == 'usuario':
            return len(value.strip()) >= 3
        elif field == 'password':
            return len(value.strip()) >= 4
        return False
    
    def get_completion_percentage():
        """Calcula el porcentaje de completitud del formulario"""
        usuario_val = usuario_input_state['value'] if usuario_input_state else ''
        password_val = password_input_state['value'] if password_input_state else ''
        
        total_fields = 2
        completed_fields = 0
        if validate_field('usuario', usuario_val):
            completed_fields += 1
        if validate_field('password', password_val):
            completed_fields += 1
        return int((completed_fields / total_fields) * 100)
    
    def validate_form():
        """Valida todo el formulario"""
        usuario_val = usuario_input_state['value'] if usuario_input_state else ''
        password_val = password_input_state['value'] if password_input_state else ''
        
        if not usuario_val.strip():
            form_state['error_message'] = 'El usuario es requerido'
            return False
        if not password_val.strip():
            form_state['error_message'] = 'La contraseña es requerida'
            return False
        if not validate_field('usuario', usuario_val):
            form_state['error_message'] = 'El usuario debe tener al menos 3 caracteres'
            return False
        if not validate_field('password', password_val):
            form_state['error_message'] = 'La contraseña debe tener al menos 4 caracteres'
            return False
        return True
    
    def handle_login():
        """Maneja el intento de login"""
        if validate_form():
            usuario_val = usuario_input_state['value'] if usuario_input_state else ''
            password_val = password_input_state['value'] if password_input_state else ''
            
            form_state['result'] = {
                'action': 'login',
                'usuario': usuario_val,
                'password': password_val,
                'remember_user': form_state['remember_user']
            }
            return True
        else:
            form_state['show_error'] = True
        return False
    
    def handle_cancel():
        """Maneja la cancelación del formulario"""
        form_state['result'] = {'action': 'cancel'}
        return True
    
    def toggle_password_visibility():
        """Alterna la visibilidad de la contraseña"""
        form_state['show_password'] = not form_state['show_password']
    
    def toggle_remember_user():
        """Alterna la opción de recordar usuario"""
        form_state['remember_user'] = not form_state['remember_user']
    
    while form_state['result'] is None:
        screen.clear()
        
        # Obtener valores actuales para validación
        usuario_val = usuario_input_state['value'] if usuario_input_state else ''
        password_val = password_input_state['value'] if password_input_state else ''
        usuario_valid = validate_field('usuario', usuario_val)
        password_valid = validate_field('password', password_val)
        
        # Título del formulario
        print_text(screen, {
            'text': 'INICIO DE SESIÓN',
            'x-center': 0,
            'y-center': -12,
            'font': 'slant',
            'justify': 'center',
            'color': Screen.COLOUR_CYAN
        }, asccii_art=True)
        
        # Barra de progreso de completitud
        completion = get_completion_percentage()
        progress_width = 40
        filled_width = int((completion / 100) * progress_width)
        progress_bar = '█' * filled_width + '░' * (progress_width - filled_width)
        
        print_text(screen, {
            'text': f'Completitud: {completion}%',
            'x-center': 0,
            'y-center': -8,
            'color': Screen.COLOUR_WHITE
        })
        
        print_text(screen, {
            'text': f'[{progress_bar}]',
            'x-center': 0,
            'y-center': -7,
            'color': Screen.COLOUR_GREEN if completion == 100 else Screen.COLOUR_YELLOW
        })
        
        # Contenedor principal del formulario
        print_card(screen, {
            'width': 60,
            'height': 22,
            'x-center': 0,
            'y-center': 2,
            'text': '',
            'color': Screen.COLOUR_WHITE,
            'corner': ['╭', '╮', '╰', '╯'],
            'ascii_x': '─',
            'ascii_y': '│'
        })
        
        # Campo Usuario
        print_text(screen, {
            'text': 'Usuario:',
            'x-center': -25,
            'y-center': -5,
            'color': Screen.COLOUR_WHITE
        })
        
        # Indicador de validación del usuario
        user_icon = '✅' if usuario_valid else ('❌' if usuario_val else '⚪')
        print_text(screen, {
            'text': user_icon,
            'x-center': 20,
            'y-center': -5,
            'color': Screen.COLOUR_GREEN if usuario_valid else Screen.COLOUR_RED
        })
        
        # Campo Contraseña
        print_text(screen, {
            'text': 'Contraseña:',
            'x-center': -25,
            'y-center': -1,
            'color': Screen.COLOUR_WHITE
        })
        
        # Indicador de validación de la contraseña
        pass_icon = '✅' if password_valid else ('❌' if password_val else '⚪')
        print_text(screen, {
            'text': pass_icon,
            'x-center': 20,
            'y-center': -1,
            'color': Screen.COLOUR_GREEN if password_valid else Screen.COLOUR_RED
        })
        
        # Botón para mostrar/ocultar contraseña
        show_hide_btn = print_button(screen, {
            'text': '👁️' if form_state['show_password'] else '🔒',
            'x-center': 24,
            'y-center': 1,
            'color': Screen.COLOUR_CYAN
        })
        
        # Checkbox "Recordar usuario"
        remember_checkbox = print_button(screen, {
            'text': '[✓]' if form_state['remember_user'] else '[ ]',
            'x-center': -25,
            'y-center': 4,
            'color': Screen.COLOUR_GREEN if form_state['remember_user'] else Screen.COLOUR_WHITE
        })
        
        print_text(screen, {
            'text': 'Recordar usuario',
            'x-center': -19,
            'y-center': 4,
            'color': Screen.COLOUR_WHITE
        })
        
        # Botones principales
        login_btn_result = print_button(screen, {
            'text': '  🔑 INICIAR SESIÓN  ',
            'x-center': -12,
            'y-center': 7,
            'color': Screen.COLOUR_BLACK if completion == 100 else Screen.COLOUR_WHITE,
            'bg': Screen.COLOUR_GREEN if completion == 100 else Screen.COLOUR_BLACK
        })
        
        cancel_btn_result = print_button(screen, {
            'text': '  ❌ CANCELAR  ',
            'x-center': 12,
            'y-center': 7,
            'color': Screen.COLOUR_WHITE,
            'bg': Screen.COLOUR_RED
        })
        
        # Mostrar error si existe
        if form_state['show_error']:
            print_text(screen, {
                'text': f"❌ {form_state['error_message']}",
                'x-center': 0,
                'y-center': 10,
                'color': Screen.COLOUR_RED
            })
        
        # Instrucciones
        print_text(screen, {
            'text': 'ESC: Cancelar | Click en los campos para escribir',
            'x-center': 0,
            'y-center': 12,
            'color': Screen.COLOUR_CYAN
        })
        
        # Renderizar campos de entrada
        screen.refresh()
        event = screen.get_event()
        
        # Campo de entrada Usuario
        usuario_result = print_input(screen, {
            'id': 'usuario',
            'label': 'Usuario',
            'x-center': 0,
            'y-center': -3,
            'width': 36,
            'height': 3,
            'max_length': max_length['usuario'],
            'placeholder': 'Ingrese su usuario...',
            'color_focused': Screen.COLOUR_GREEN if usuario_valid else Screen.COLOUR_YELLOW,
            'color_normal': Screen.COLOUR_GREEN if usuario_valid else Screen.COLOUR_WHITE
        }, event, usuario_input_state)
        
        # Campo de entrada Contraseña
        password_result = print_input(screen, {
            'id': 'password',
            'label': 'Contraseña',
            'x-center': 0,
            'y-center': 1,
            'width': 36,
            'height': 3,
            'max_length': max_length['password'],
            'placeholder': 'Ingrese su contraseña...',
            'color_focused': Screen.COLOUR_GREEN if password_valid else Screen.COLOUR_YELLOW,
            'color_normal': Screen.COLOUR_GREEN if password_valid else Screen.COLOUR_WHITE,
            'is_password': not form_state['show_password']
        }, event, password_input_state)
        
        # Actualizar estados de los inputs
        usuario_input_state = usuario_result['input_state']
        password_input_state = password_result['input_state']
        
        # Manejar clicks en botones
        if event and hasattr(event, 'buttons') and event.buttons != 0:
            # Verificar click en botón mostrar/ocultar contraseña
            show_x = show_hide_btn['x_position']
            show_y = show_hide_btn['y_position']
            show_w = show_hide_btn['width']
            show_h = show_hide_btn['height']
            
            if (show_x <= event.x < show_x + show_w and 
                show_y <= event.y < show_y + show_h):
                toggle_password_visibility()
            
            # Verificar click en checkbox
            check_x = remember_checkbox['x_position']
            check_y = remember_checkbox['y_position']
            check_w = remember_checkbox['width']
            check_h = remember_checkbox['height']
            
            if (check_x <= event.x < check_x + check_w and 
                check_y <= event.y < check_y + check_h):
                toggle_remember_user()
            
            # Verificar click en botón login
            login_x = login_btn_result['x_position']
            login_y = login_btn_result['y_position']
            login_w = login_btn_result['width']
            login_h = login_btn_result['height']
            
            if (login_x <= event.x < login_x + login_w and 
                login_y <= event.y < login_y + login_h and completion == 100):
                if handle_login():
                    break
            
            # Verificar click en botón cancelar
            cancel_x = cancel_btn_result['x_position']
            cancel_y = cancel_btn_result['y_position']
            cancel_w = cancel_btn_result['width']
            cancel_h = cancel_btn_result['height']
            
            if (cancel_x <= event.x < cancel_x + cancel_w and 
                cancel_y <= event.y < cancel_y + cancel_h):
                if handle_cancel():
                    break
        
        # Manejo de eventos de teclado
        if isinstance(event, KeyboardEvent):
            form_state['show_error'] = False
            
            # Escape - cancelar
            if event.key_code == 27:
                if handle_cancel():
                    break
            
            # Enter - intentar login si está completo
            elif event.key_code in [10, 13]:
                if completion == 100:
                    if handle_login():
                        break
    
    return form_state['result']
