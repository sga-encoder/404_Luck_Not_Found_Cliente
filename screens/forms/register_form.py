"""
Formulario de registro de usuario usando print_form
"""
# Importaciones estándar
import json
import os
import re
import sys
import asyncio

# Importaciones de terceros
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent

# Importaciones locales
from ...utils.printers import print_form, print_text
from ...utils.user_session import UserSessionManager

def validate_email(email):
    """Valida el formato del email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_name(name):
    """Valida que el nombre tenga entre 3 y 30 caracteres"""
    return name and len(name.strip()) >= 3 and len(name.strip()) <= 30

def register_form(screen):
    """
    Formulario de registro de usuario usando print_form.
    """
    screen.clear()
    screen.mouse = True
    
    # Variables para almacenar el estado de registro
    auth_state = {
        'message': '',
        'message_color': Screen.COLOUR_WHITE,
        'result': None
    }
    
    # Gestor de sesión
    session_manager = UserSessionManager()
    
    async def handle_register_submit(form_state, form_config):
        from servidor.src.model.usuario.Usuario import Usuario
        """Maneja el proceso de registro de usuario"""
        nombre = form_state['form_data'].get('nombre', '').strip()
        apellido = form_state['form_data'].get('apellido', '').strip()
        email = form_state['form_data'].get('email', '').strip()
        password = form_state['form_data'].get('password', '')
        confirm_password = form_state['form_data'].get('confirm_password', '')
        
        # Validaciones locales adicionales
        # if not validate_name(nombre):
        #     form_state['error_message'] = 'El nombre debe tener entre 3 y 30 caracteres'
        #     form_state['show_error'] = True
        #     return False
        # if not validate_name(apellido):
        #     form_state['error_message'] = 'El apellido debe tener entre 3 y 30 caracteres'
        #     form_state['show_error'] = True
        #     return False
        
        # if not validate_email(email):
        #     form_state['error_message'] = 'Formato de email inválido'
        #     form_state['show_error'] = True
        #     return False
        
        # if len(password) < 8:
        #     form_state['error_message'] = 'La contraseña debe tener al menos 8 caracteres'
        #     form_state['show_error'] = True
        #     return False
        if password != confirm_password:
            form_state['error_message'] = 'Las contraseñas no coinciden'
            form_state['show_error'] = True
            return False
        
        # Extraer solo datos seguros para mostrar
        safe_form_data = {
            'form_data': form_state.get('form_data', {}),
            'current_field': form_state.get('current_field', ''),
            'error_message': form_state.get('error_message', ''),
            'show_error': form_state.get('show_error', False)
        }
        
        # print_text(screen, {
        #     'text': json.dumps(safe_form_data, indent=2, ensure_ascii=False),
        #     'x': 2,
        #     'y': 2,
        #     'color': Screen.COLOUR_WHITE
        # })

        # print_text(screen, {
        #     'text': form_config,
        #     'x-right': 0,
        #     'y': 0,
        #     'color': Screen.COLOUR_GREEN
        # })        # Mostrar mensaje de carga
        auth_state['message'] = 'Registrando usuario...'
        auth_state['message_color'] = Screen.COLOUR_YELLOW
        
        try:
            # Crear usuario usando el método del servidor
            usuario = await Usuario.crear_usuario(nombre, apellido, email, password)
            
            # Guardar sesión local
            user_data = usuario.to_dict()
            if session_manager.save_user_session(user_data):
                auth_state['message'] = 'Usuario registrado exitosamente'
                auth_state['message_color'] = Screen.COLOUR_GREEN
                auth_state['result'] = {
                    'success': True,
                    'user': usuario,
                    'email': email,
                    'action': 'register_success'
                }
                form_state['result'] = {
                    'action': 'register_success',
                    'data': auth_state['result']
                }
                return True
            else:
                form_state['error_message'] = 'Error al guardar la sesión del usuario'
                form_state['show_error'] = True
                return False
        except Exception as e:
            form_state['error_message'] = f'Error al registrar usuario: {str(e)}'
            form_state['show_error'] = True
            auth_state['message'] = f'Error: {str(e)}'
            auth_state['message_color'] = Screen.COLOUR_RED
            return False
                
    
    # Configuración del formulario usando print_form
    form_config = {
        'title': 'REGISTRO DE USUARIO',
        'title_config': {
            'font': 'slant',
            'color': Screen.COLOUR_CYAN,
            'x-center': 0,
            'y': 1,
            'justify': 'center',
            'max-width': 75
        },
        'container': {
            'width': 55,
            'height': 26,
            'x-center': 0,
            'y-center': 0,
            'corner': ['╭', '╮', '╰', '╯'],
            'ascii_x': '─',
            'ascii_y': '│',
            'color': Screen.COLOUR_WHITE
        },
        'inputs': {
            'nombre': {
                'label': 'Nombre:',
                'width': 47,
                'height': 4,
                'x-center': 0,
                'y-center': -8,
                'placeholder': 'Tu nombre',
                'max_length': 30,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            },
            'apellido': {
                'label': 'Apellido:',
                'width': 47,
                'height': 4,
                'x-center': 0,
                'y-center': -4,
                'placeholder': 'Tu apellido',
                'max_length': 30,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            },
            'email': {
                'label': 'Email:',
                'width': 47,
                'height': 4,
                'x-center': 0,
                'y-center': 0,
                'placeholder': 'ejemplo@correo.com',
                'max_length': 50,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            },
            'password': {
                'label': 'Contraseña:',
                'width': 47,
                'height': 4,
                'x-center': 0,
                'y-center': 4,
                'placeholder': 'Tu contraseña (mín. 8 caracteres)',
                'is_password': True,
                'max_length': 50,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            },
            'confirm_password': {
                'label': 'Confirmar Contraseña:',
                'width': 47,
                'height': 4,
                'x-center': 0,
                'y-center': 8,
                'placeholder': 'Confirma tu contraseña',
                'is_password': True,
                'max_length': 50,
                'color_focused': Screen.COLOUR_YELLOW,
                'color_normal': Screen.COLOUR_WHITE
            }
        },
        'buttons': {
            'grid': True,
            'width': 45,
            'height': 3,
            'x-center': 0,
            'y-center': 12,
            'grid_divider_x': 2,
            'grid_divider_y': 1,
            'content': {
                '0': {
                    'text': 'REGISTRARSE',
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_GREEN,
                    'action': 'submit',
                    'click': lambda: handle_register_submit
                },
                '1': {
                    'text': 'CANCELAR',
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_RED,
                    'action': 'cancel',
                    'click': lambda: None
                }
            }
        },
        'validation': {
            'nombre': {
                'required': True,
                'min_length': 3,
                'max_length': 30,
                'custom': validate_name
            },
            'apellido': {
                'required': True,
                'min_length': 3,
                'max_length': 30,
                'custom': validate_name
            },
            'email': {
                'required': True,
                'min_length': 5,
                'custom': validate_email
            },
            'password': {
                'required': True,
                'min_length': 8
            },
            'confirm_password': {
                'required': True,
                'min_length': 8
            }
        },
        'navigation_order': ['nombre', 'apellido', 'email', 'password', 'confirm_password', 'btn_0', 'btn_1'],
        'initial_focus': 'nombre'
    }
    
    # Loop principal del formulario
    while True:
        # Renderizar el formulario
        event = screen.get_event()
        form_result = print_form(screen, form_config, event)
        
        # Mostrar mensaje de estado de registro si existe
        if auth_state['message']:
            print_text(screen, {
                'text': auth_state['message'],
                'x-center': 0,
                'y-center': 16,
                'color': auth_state['message_color']
            })
        
        # Mostrar instrucciones
        print_text(screen, {
            'text': 'TAB: Navegar | ENTER: Aceptar | ESC: Salir',
            'x-center': 0,
            'y-center': 18,
            'color': Screen.COLOUR_CYAN
        })
        screen.refresh()
        
        # Verificar si el formulario fue completado
        if form_result['form_state']['result']:
            action = form_result['form_state']['result']['action']
            
            if action == 'register_success':
                return form_result['form_state']['result']['data']
            elif action == 'submit':
                # Ejecutar lógica de registro (async)
                if asyncio.run(handle_register_submit(form_result['form_state'], form_config)):
                    if auth_state['result']:
                        return auth_state['result']
            elif action == 'cancel':
                return {'success': False, 'action': 'cancel'}
        
        # Manejar tecla ESC para salir
        if event and hasattr(event, 'key_code') and event.key_code == 27:
            return {'success': False, 'action': 'exit'}
