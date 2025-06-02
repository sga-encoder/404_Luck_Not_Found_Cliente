from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent, MouseEvent
from utils.events import add_key_listener
from utils.printers import print_text, print_button, print_card


def advanced_login_form(screen):
    """
    Formulario de login avanzado con más características:
    - Recordar usuario
    - Mostrar/ocultar contraseña
    - Validación en tiempo real
    - Animaciones
    - Mejor UX
    """
    screen.clear()
    screen.mouse = True
    
    # Estado del formulario
    form_state = {
        'usuario': '',
        'password': '',
        'current_field': 'usuario',
        'remember_me': False,
        'show_password': False,
        'show_error': False,
        'error_message': '',
        'cursor_pos': {'usuario': 0, 'password': 0},
        'validation': {
            'usuario_valid': False,
            'password_valid': False
        }
    }
    
    max_length = {'usuario': 20, 'password': 15}
    min_length = {'usuario': 3, 'password': 6}
    
    def validate_fields():
        """Validar campos en tiempo real"""
        form_state['validation']['usuario_valid'] = len(form_state['usuario']) >= min_length['usuario']
        form_state['validation']['password_valid'] = len(form_state['password']) >= min_length['password']
    
    def get_field_color(field_name):
        """Obtener color según validación"""
        if form_state['current_field'] == field_name:
            return Screen.COLOUR_YELLOW
        elif form_state['validation'][f'{field_name}_valid']:
            return Screen.COLOUR_GREEN
        elif form_state[field_name]:  # Tiene texto pero no es válido
            return Screen.COLOUR_RED
        else:
            return Screen.COLOUR_WHITE
    
    while True:
        screen.clear()
        validate_fields()
        
        # Título animado
        print_text(screen, {
            'text': '🔐 SISTEMA DE AUTENTICACIÓN',
            'x-center': 0,
            'y-center': -10,
            'font': 'slant',
            'justify': 'center',
            'color': Screen.COLOUR_CYAN
        }, asccii_art=True)
        
        # Contenedor principal con diseño moderno
        form_container = {
            'width': 60,
            'height': 20,
            'x-center': 0,
            'y-center': 0,
            'corner': ['╔', '╗', '╚', '╝'],
            'ascii_x': '═',
            'ascii_y': '║',
            'color': Screen.COLOUR_WHITE
        }
        print_card(screen, form_container)
        
        # Título del formulario
        print_text(screen, {
            'text': 'Iniciar Sesión',
            'x-center': 0,
            'y-center': -7,
            'color': Screen.COLOUR_WHITE
        })
        
        # Campo Usuario con validación visual
        usuario_color = get_field_color('usuario')
        print_text(screen, {
            'text': f"👤 Usuario (mín. {min_length['usuario']} chars):",
            'x-center': -20,
            'y-center': -4,
            'color': usuario_color
        })
        
        # Indicador de validación para usuario
        if form_state['usuario']:
            validation_icon = '✓' if form_state['validation']['usuario_valid'] else '✗'
            validation_color = Screen.COLOUR_GREEN if form_state['validation']['usuario_valid'] else Screen.COLOUR_RED
            print_text(screen, {
                'text': validation_icon,
                'x-center': 22,
                'y-center': -4,
                'color': validation_color
            })
        
        # Campo de entrada para usuario
        usuario_display = form_state['usuario']
        if form_state['current_field'] == 'usuario':
            cursor_pos = form_state['cursor_pos']['usuario']
            if len(usuario_display) >= cursor_pos:
                usuario_display = usuario_display[:cursor_pos] + '█' + usuario_display[cursor_pos:]
        
        usuario_field = {
            'width': 30,
            'height': 3,
            'text': usuario_display,
            'x-center': 0,
            'y-center': -3,
            'corner': ['┌', '┐', '└', '┘'],
            'ascii_x': '─',
            'ascii_y': '│',
            'color': usuario_color,
            'bg': Screen.COLOUR_BLACK if form_state['current_field'] == 'usuario' else Screen.COLOUR_DEFAULT
        }
        print_card(screen, usuario_field)
        
        # Campo Contraseña
        password_color = get_field_color('password')
        show_text = "👁️ Mostrar" if not form_state['show_password'] else "🙈 Ocultar"
        print_text(screen, {
            'text': f"🔒 Contraseña (mín. {min_length['password']} chars):",
            'x-center': -20,
            'y-center': -1,
            'color': password_color
        })
        
        # Botón mostrar/ocultar contraseña
        show_hide_btn = {
            'text': f"[{show_text}]",
            'x-center': 18,
            'y-center': -1,
            'color': Screen.COLOUR_BLUE
        }
        
        # Indicador de validación para contraseña
        if form_state['password']:
            validation_icon = '✓' if form_state['validation']['password_valid'] else '✗'
            validation_color = Screen.COLOUR_GREEN if form_state['validation']['password_valid'] else Screen.COLOUR_RED
            print_text(screen, {
                'text': validation_icon,
                'x-center': 22,
                'y-center': -1,
                'color': validation_color
            })
        
        # Campo de entrada para contraseña
        if form_state['show_password']:
            password_display = form_state['password']
        else:
            password_display = '*' * len(form_state['password'])
            
        if form_state['current_field'] == 'password':
            cursor_pos = form_state['cursor_pos']['password']
            if len(password_display) >= cursor_pos:
                password_display = password_display[:cursor_pos] + '█' + password_display[cursor_pos:]
        
        password_field = {
            'width': 30,
            'height': 3,
            'text': password_display,
            'x-center': 0,
            'y-center': 0,
            'corner': ['┌', '┐', '└', '┘'],
            'ascii_x': '─',
            'ascii_y': '│',
            'color': password_color,
            'bg': Screen.COLOUR_BLACK if form_state['current_field'] == 'password' else Screen.COLOUR_DEFAULT
        }
        print_card(screen, password_field)
        
        # Checkbox "Recordarme"
        remember_icon = '☑️' if form_state['remember_me'] else '☐'
        remember_color = Screen.COLOUR_GREEN if form_state['remember_me'] else Screen.COLOUR_WHITE
        print_text(screen, {
            'text': f"{remember_icon} Recordarme",
            'x-center': -15,
            'y-center': 2,
            'color': remember_color
        })
        
        # Botones con mejores colores
        all_valid = form_state['validation']['usuario_valid'] and form_state['validation']['password_valid']
        
        login_btn_color = Screen.COLOUR_WHITE if all_valid else Screen.COLOUR_BLACK
        login_btn_bg = Screen.COLOUR_GREEN if all_valid else Screen.COLOUR_MAGENTA
        
        if form_state['current_field'] == 'login_btn':
            login_btn_color = Screen.COLOUR_BLACK
            login_btn_bg = Screen.COLOUR_YELLOW
        
        login_button = {
            'text': '🚀 [ INICIAR SESIÓN ]',
            'x-center': -10,
            'y-center': 4,
            'color': login_btn_color,
            'bg': login_btn_bg
        }
        
        cancel_btn_color = Screen.COLOUR_WHITE
        cancel_btn_bg = Screen.COLOUR_RED
        
        if form_state['current_field'] == 'cancel_btn':
            cancel_btn_color = Screen.COLOUR_BLACK
            cancel_btn_bg = Screen.COLOUR_YELLOW
        
        cancel_button = {
            'text': '❌ [ CANCELAR ]',
            'x-center': 10,
            'y-center': 4,
            'color': cancel_btn_color,
            'bg': cancel_btn_bg
        }
        
        # Obtener evento
        screen.refresh()
        event = screen.get_event()
        
        # Renderizar botones
        login_result = print_button(screen, login_button, event, 
                                   click=lambda: 'login' if all_valid else 'error')
        cancel_result = print_button(screen, cancel_button, event, click=lambda: 'cancel')
        show_hide_result = print_button(screen, show_hide_btn, event, click=lambda: 'toggle_password')
        
        # Mostrar error
        if form_state['show_error']:
            print_text(screen, {
                'text': f"❌ {form_state['error_message']}",
                'x-center': 0,
                'y-center': 6,
                'color': Screen.COLOUR_RED
            })
        
        # Barra de progreso de validación
        progress = 0
        if form_state['validation']['usuario_valid']:
            progress += 50
        if form_state['validation']['password_valid']:
            progress += 50
            
        progress_bar = '█' * (progress // 10) + '░' * (10 - progress // 10)
        print_text(screen, {
            'text': f"Completado: {progress}% [{progress_bar}]",
            'x-center': 0,
            'y-center': 7,
            'color': Screen.COLOUR_CYAN
        })
        
        # Instrucciones mejoradas
        print_text(screen, {
            'text': '⌨️  TAB: Navegar | ENTER: Confirmar | ESC: Salir | ESPACIO: Recordarme',
            'x-center': 0,
            'y-center': 9,
            'color': Screen.COLOUR_CYAN
        })
        
        # Procesar eventos (mismo código que antes pero con mejoras)
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            
            # ESC - Salir
            if key == 27:
                return 'cancel'
            
            # TAB - Navegar
            elif key == 9:
                fields = ['usuario', 'password', 'login_btn', 'cancel_btn']
                current_index = fields.index(form_state['current_field'])
                form_state['current_field'] = fields[(current_index + 1) % len(fields)]
                form_state['show_error'] = False
            
            # ESPACIO - Toggle recordarme
            elif key == 32 and form_state['current_field'] not in ['usuario', 'password']:
                form_state['remember_me'] = not form_state['remember_me']
            
            # ENTER - Confirmar
            elif key in [10, 13]:
                if form_state['current_field'] == 'login_btn':
                    if all_valid:
                        return {
                            'action': 'login',
                            'usuario': form_state['usuario'],
                            'password': form_state['password'],
                            'remember_me': form_state['remember_me']
                        }
                    else:
                        form_state['show_error'] = True
                        form_state['error_message'] = 'Complete todos los campos correctamente'
                elif form_state['current_field'] == 'cancel_btn':
                    return 'cancel'
            
            # BACKSPACE
            elif key == 8:
                current_field = form_state['current_field']
                if current_field in ['usuario', 'password']:
                    cursor_pos = form_state['cursor_pos'][current_field]
                    if cursor_pos > 0:
                        text = form_state[current_field]
                        form_state[current_field] = text[:cursor_pos-1] + text[cursor_pos:]
                        form_state['cursor_pos'][current_field] = cursor_pos - 1
                        form_state['show_error'] = False
            
            # Flechas y entrada de texto (mismo código que antes)
            elif key == Screen.KEY_LEFT:
                current_field = form_state['current_field']
                if current_field in ['usuario', 'password']:
                    cursor_pos = form_state['cursor_pos'][current_field]
                    form_state['cursor_pos'][current_field] = max(0, cursor_pos - 1)
                    
            elif key == Screen.KEY_RIGHT:
                current_field = form_state['current_field']
                if current_field in ['usuario', 'password']:
                    cursor_pos = form_state['cursor_pos'][current_field]
                    max_pos = len(form_state[current_field])
                    form_state['cursor_pos'][current_field] = min(max_pos, cursor_pos + 1)
            
            # Entrada de texto
            elif 32 <= key <= 126:
                current_field = form_state['current_field']
                if current_field in ['usuario', 'password']:
                    if len(form_state[current_field]) < max_length[current_field]:
                        cursor_pos = form_state['cursor_pos'][current_field]
                        text = form_state[current_field]
                        char = chr(key)
                        form_state[current_field] = text[:cursor_pos] + char + text[cursor_pos:]
                        form_state['cursor_pos'][current_field] = cursor_pos + 1
                        form_state['show_error'] = False
        
        # Procesar clicks
        if login_result['result']:
            if login_result['result'] == 'login':
                return {
                    'action': 'login',
                    'usuario': form_state['usuario'],
                    'password': form_state['password'],
                    'remember_me': form_state['remember_me']
                }
            elif login_result['result'] == 'error':
                form_state['show_error'] = True
                form_state['error_message'] = 'Complete todos los campos correctamente'
                
        if cancel_result['result']:
            return 'cancel'
            
        if show_hide_result['result']:
            form_state['show_password'] = not form_state['show_password']


def simple_input_field(screen, label, x_center=0, y_center=0, max_length=20, password=False):
    """
    Campo de entrada simple reutilizable
    """
    text = ''
    cursor_pos = 0
    
    while True:
        screen.clear()
        
        # Label
        print_text(screen, {
            'text': label,
            'x-center': x_center,
            'y-center': y_center - 1,
            'color': Screen.COLOUR_CYAN
        })
        
        # Campo de entrada
        display_text = text
        if password:
            display_text = '*' * len(text)
            
        # Mostrar cursor
        display_text = display_text[:cursor_pos] + '█' + display_text[cursor_pos:]
        
        field = {
            'width': max_length + 4,
            'height': 3,
            'text': display_text,
            'x-center': x_center,
            'y-center': y_center,
            'corner': ['┌', '┐', '└', '┘'],
            'color': Screen.COLOUR_WHITE,
            'bg': Screen.COLOUR_BLACK
        }
        print_card(screen, field)
        
        print_text(screen, {
            'text': 'ENTER: Confirmar | ESC: Cancelar',
            'x-center': x_center,
            'y-center': y_center + 3,
            'color': Screen.COLOUR_YELLOW
        })
        
        screen.refresh()
        event = screen.get_event()
        
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            
            if key == 27:  # ESC
                return None
            elif key in [10, 13]:  # ENTER
                return text
            elif key == 8:  # BACKSPACE
                if cursor_pos > 0:
                    text = text[:cursor_pos-1] + text[cursor_pos:]
                    cursor_pos -= 1
            elif key == Screen.KEY_LEFT:
                cursor_pos = max(0, cursor_pos - 1)
            elif key == Screen.KEY_RIGHT:
                cursor_pos = min(len(text), cursor_pos + 1)
            elif 32 <= key <= 126 and len(text) < max_length:
                char = chr(key)
                text = text[:cursor_pos] + char + text[cursor_pos:]
                cursor_pos += 1
