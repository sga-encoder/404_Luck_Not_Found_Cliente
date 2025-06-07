"""
Formulario de login usando print_form
"""
# Importaciones estándar
import json
import asyncio

# Importaciones de terceros
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent

# Importaciones locales
from ...utils.printers import print_form, print_text
from ...utils.user_session import UserSessionManager
from servidor.src.model.usuario import UsuarioServicio


async def login_form(screen):
    """
    Formulario de login usando print_form.
    """
    screen.clear()
    screen.mouse = True
    
    # Variables para almacenar el estado de login
    auth_state = {
        'message': '',
        'message_color': Screen.COLOUR_WHITE,
        'result': None
    }
    
    # Gestor de sesión
    session_manager = UserSessionManager()
    
    async def handle_login_submit(form_state, form_config):
        """Maneja el proceso de login"""
        usuario = form_state['form_data'].get('usuario', '').strip()
        password = form_state['form_data'].get('password', '')
        
        # Extraer solo datos seguros para mostrar
        safe_form_data = {
            'form_data': form_state.get('form_data', {}),
            'current_field': form_state.get('current_field', ''),
            'error_message': form_state.get('error_message', ''),
            'show_error': form_state.get('show_error', False)
        }
        
        # Mostrar mensaje de carga
        auth_state['message'] = 'Iniciando sesión...'
        auth_state['message_color'] = Screen.COLOUR_YELLOW
        
        try:
            # Autenticar usuario
            servicio = UsuarioServicio()
            response = await servicio.autenticar_usuario(usuario, password)
            
            if response.get('success'):
                # Guardar sesión
                user_data = response.get('user').to_dict()
                if session_manager.save_user_session(user_data):
                    auth_state['message'] = 'Inicio de sesión exitoso'
                    auth_state['message_color'] = Screen.COLOUR_GREEN
                    auth_state['result'] = {
                        'success': True,
                        'user': response.get('user'),
                        'action': 'login_success'
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
                form_state['error_message'] = response.get('error', 'Credenciales inválidas')
                form_state['show_error'] = True
                auth_state['message'] = f'Error: {response.get("error", "Credenciales inválidas")}'
                auth_state['message_color'] = Screen.COLOUR_RED
                return False
        except Exception as e:
            form_state['error_message'] = f'Error al iniciar sesión: {str(e)}'
            form_state['show_error'] = True
            auth_state['message'] = f'Error: {str(e)}'
            auth_state['message_color'] = Screen.COLOUR_RED
            return False
    
    # Configuración del formulario usando print_form
    form_config = {
        'title': 'INICIAR SESIÓN',
        'title_config': {
            'font': 'slant',
            'color': Screen.COLOUR_CYAN,
            'x-center': 0,
            'y': 1,
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
            'usuario': {
                'label': 'Usuario:',
                'width': 44,
                'height': 4,
                'x-center': 0,
                'y-center': -4,
                'placeholder': 'Ingresa tu usuario',
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            },
            'password': {
                'label': 'Contraseña:',
                'width': 44,
                'height': 4,
                'x-center': 0,
                'y-center': 0,
                'placeholder': 'Ingresa tu contraseña',
                'is_password': True,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
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
                    'text': '  INICIAR SESIÓN  ',
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_GREEN,
                    'action': 'submit',
                    'click': lambda: handle_login_submit
                },
                '1': {
                    'text': '  CANCELAR  ',
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_RED,
                    'action': 'cancel',
                    'click': lambda: None
                }
            }
        },
        'validation': {
            'usuario': {
                'required': True,
                'min_length': 3
            },
            'password': {
                'required': True,
                'min_length': 4
            }
        },
        'navigation_order': ['usuario', 'password', 'btn_0', 'btn_1'],
        'initial_focus': 'usuario'
    }
    
    # Loop principal del formulario
    while True:
        # Renderizar el formulario
        event = screen.get_event()
        form_result = print_form(screen, form_config, event)
        
        # Mostrar mensaje de estado de login si existe
        if auth_state['message']:
            print_text(screen, {
                'text': auth_state['message'],
                'x-center': 0,
                'y-center': 8,
                'color': auth_state['message_color']
            })
        
        # Mostrar instrucciones
        print_text(screen, {
            'text': 'TAB: Cambiar campo | ENTER: Aceptar | ESC: Cancelar',
            'x-center': 0,
            'y-center': 10,
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
                if await handle_login_submit(form_result['form_state'], form_config):
                    if auth_state['result']:
                        return auth_state['result']
            elif action == 'cancel':
                return {'success': False, 'action': 'cancel'}
        
        # Manejar tecla ESC para salir
        if event and hasattr(event, 'key_code') and event.key_code == 27:
            return {'success': False, 'action': 'exit'}


if __name__ == "__main__":
    # Ejemplo de uso
    def main(screen):
        result = login_form(screen)
        screen.clear()
        screen.print_at(f"Resultado: {result}", 0, 0, Screen.COLOUR_WHITE)
        screen.refresh()
        screen.wait_for_input(5)
    
    Screen.wrapper(main)
