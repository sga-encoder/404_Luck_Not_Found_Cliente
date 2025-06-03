"""
Formulario de login usando Firestore y la clase Usuario del servidor
"""
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent
from ...utils.printers import print_form, print_text
from ...utils.user_session import UserSessionManager
import re
import sys
import os

def validate_email(email):
    """Valida el formato del email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def login_form_with_firestore(screen):
    """
    Formulario de login usando Firestore directamente.
    """
    screen.clear()
    screen.mouse = True
    
    # Variables para almacenar el estado de autenticación
    auth_state = {
        'message': '',
        'message_color': Screen.COLOUR_WHITE,
        'result': None
    }
      # Gestor de sesión y servicio de usuario


    session_manager = UserSessionManager()      
    
    async def handle_login_submit(form_state, form_config):
        """Maneja el proceso de inicio de sesión con Firestore"""
        # Importar el servicio de usuario aquí para evitar errores de importación
        server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..', 'servidor/src'))
        sys.path.append(server_path)
        try:
            from model.usuario.UsuarioServicio import UsuarioServicio
            
            usuario_servicio = UsuarioServicio()
            email = form_state['form_data'].get('email', '').strip()
            password = form_state['form_data'].get('password', '')
        except ImportError as e:
            print(f"Error importando el servicio de usuario: {e}")
            form_state['error_message'] = "Error al conectar con el servicio de autenticación."
            form_state['show_error'] = True
            auth_state['message'] = "Error al conectar con el servicio de autenticación."
            auth_state['message_color'] = Screen.COLOUR_RED
            return False
        
        # Validaciones locales adicionales
        if not validate_email(email):
            form_state['error_message'] = 'Formato de email inválido'
            form_state['show_error'] = True
            return False
        
        # Mostrar mensaje de carga
        auth_state['message'] = 'Iniciando sesión...'
        auth_state['message_color'] = Screen.COLOUR_YELLOW
        
        try:
            # Autenticar usuario usando el servicio
            result = await usuario_servicio.autenticar_usuario(email, password)
            
            if result['success']:
                # Guardar sesión local
                user_data = result['user'].to_dict()
                if session_manager.save_user_session(user_data):
                    auth_state['message'] = result['message']
                    auth_state['message_color'] = Screen.COLOUR_GREEN
                    auth_state['result'] = {
                        'success': True,
                        'user': result['user'],
                        'email': email
                    }
                    form_state['result'] = {
                        'action': 'login_success',
                        'data': auth_state['result']
                    }
                    return True
                else:
                    form_state['error_message'] = 'Error al guardar la sesión del usuario'
                    form_state['show_error'] = True
                    return False
            else:
                auth_state['message'] = result['message']
                auth_state['message_color'] = Screen.COLOUR_RED
                form_state['error_message'] = result['message']
                form_state['show_error'] = True
                return False
                
        except Exception as e:
            auth_state['message'] = f'Error en la autenticación: {str(e)}'
            auth_state['message_color'] = Screen.COLOUR_RED
            form_state['error_message'] = f'Error en la autenticación: {str(e)}'
            form_state['show_error'] = True
            return False
    
    # Configuración del formulario usando print_form
    form_config = {
        'title': 'INICIAR SESIÓN',
        'title_config': {
            'font': 'slant',
            'color': Screen.COLOUR_CYAN,
            'x-center': 0,
            'y': 2,
            'justify': 'center',
            'max-width': 75
        },
        'container': {
            'width': 50,
            'height': 18,
            'x-center': 0,
            'y-center': 0,
            'corner': ['╭', '╮', '╰', '╯'],
            'ascii_x': '─',
            'ascii_y': '│',
            'color': Screen.COLOUR_WHITE
        },
        'inputs': {
            'email': {
                'label': 'Email:',
                'width': 42,
                'height': 4,
                'x-center': 0,
                'y-center': -3,
                'placeholder': 'ejemplo@correo.com',
                'max_length': 50,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            },
            'password': {
                'label': 'Contraseña:',
                'width': 42,
                'height': 4,
                'x-center': 0,
                'y-center': 1,
                'placeholder': 'Tu contraseña',
                'is_password': True,
                'max_length': 50,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            }
        },
        'buttons': {
            'grid': True,
            'width': 40,
            'height': 3,
            'x-center': 0,
            'y-center': 6,
            'grid_divider_x': 2,
            'grid_divider_y': 1,
            'content': {
                '0': {
                    'text': 'INICIAR SESIÓN',
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_GREEN,
                    'action': 'submit',
                    'click': lambda: handle_login_submit
                },
                '1': {
                    'text': 'REGISTRARSE',
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_BLUE,
                    'action': 'register',
                    'click': lambda: None
                }
            }
        },
        'validation': {
            'email': {
                'required': True,
                'min_length': 5,
                'custom': validate_email
            },
            'password': {
                'required': True,
                'min_length': 8
            }
        },
        'navigation_order': ['email', 'password', 'btn_0', 'btn_1'],
        'initial_focus': 'email'
    }
    
    # Loop principal del formulario
    while True:
        # Renderizar el formulario
        event = screen.get_event()
        form_result = print_form(screen, form_config, event)
        
        # Mostrar mensaje de estado de autenticación si existe
        if auth_state['message']:
            print_text(screen, {
                'text': auth_state['message'],
                'x-center': 0,
                'y-center': 10,
                'color': auth_state['message_color']
            })
        
        # Mostrar instrucciones
        print_text(screen, {
            'text': 'TAB: Navegar | ENTER: Aceptar | ESC: Salir',
            'x-center': 0,
            'y-center': 13,
            'color': Screen.COLOUR_CYAN
        })
        
        screen.refresh()
        
        # Verificar si el formulario fue completado
        if form_result['form_state']['result']:
            action = form_result['form_state']['result']['action']
            
            if action == 'login_success':
                return form_result['form_state']['result']['data']
            elif action == 'submit':
                # Ejecutar lógica de login (async)
                import asyncio
                if asyncio.run(handle_login_submit(form_result['form_state'], form_config)):
                    if auth_state['result']:
                        return auth_state['result']
            elif action == 'register':
                # Redirigir al formulario de registro
                return {'success': False, 'action': 'show_register'}
            elif action == 'cancel':
                return {'success': False, 'action': 'exit'}
        
        # Manejar tecla ESC para salir
        if event and hasattr(event, 'key_code') and event.key_code == 27:
            return {'success': False, 'action': 'exit'}

if __name__ == "__main__":
    # Ejemplo de uso
    def main(screen):
        result = login_form_with_firestore(screen)
        screen.clear()
        screen.print_at(f"Resultado: {result}", 0, 0, Screen.COLOUR_WHITE)
        screen.refresh()
        screen.wait_for_input(5)
    
    Screen.wrapper(main)
