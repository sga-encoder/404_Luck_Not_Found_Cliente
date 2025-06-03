"""
Controlador principal para manejar la autenticación (login y registro)
"""
from asciimatics.screen import Screen
from ..screens.forms.login_firestore_form import login_form_with_firestore
from ..screens.forms.register_form import register_form_with_print_form
from .user_session import UserSessionManager

class AuthController:
    """
    Controlador para manejar el flujo de autenticación entre login y registro.
    """
    
    def __init__(self):
        self.session_manager = UserSessionManager()
    
    def check_existing_session(self) -> dict | None:
        """
        Verifica si existe una sesión activa del usuario.
        
        Returns:
            dict | None: Datos del usuario si existe sesión activa, None en caso contrario.
        """
        if self.session_manager.has_active_session():
            return self.session_manager.load_user_session()
        return None
    
    def handle_authentication_flow(self, screen) -> dict:
        """
        Maneja el flujo completo de autenticación (login/registro).
        
        Args:
            screen: Pantalla de asciimatics.
            
        Returns:
            dict: Resultado de la autenticación con información del usuario.
        """
        current_form = 'login'  # Empezar con login
        
        while True:
            if current_form == 'login':
                result = login_form_with_firestore(screen)
                
                if result.get('success'):
                    return result
                elif result.get('action') == 'show_register':
                    current_form = 'register'
                    screen.clear()
                elif result.get('action') == 'exit':
                    return {'success': False, 'action': 'exit'}
                    
            elif current_form == 'register':
                result = register_form_with_print_form(screen)
                
                if result.get('success'):
                    return result
                elif result.get('action') == 'cancel':
                    current_form = 'login'
                    screen.clear()
                elif result.get('action') == 'exit':
                    return {'success': False, 'action': 'exit'}
    
    def logout_user(self) -> bool:
        """
        Cierra la sesión del usuario eliminando el archivo de sesión.
        
        Returns:
            bool: True si se cerró la sesión correctamente.
        """
        return self.session_manager.clear_user_session()

def auth_flow_with_session_check(screen) -> dict:
    """
    Función principal que maneja el flujo de autenticación con verificación de sesión existente.
    
    Args:
        screen: Pantalla de asciimatics.
        
    Returns:
        dict: Resultado de la autenticación.
    """
    auth_controller = AuthController()
    
    # Verificar si ya existe una sesión activa
    existing_session = auth_controller.check_existing_session()
    if existing_session:
        return {
            'success': True,
            'user_data': existing_session,
            'action': 'existing_session'
        }
    
    # Si no hay sesión activa, iniciar flujo de autenticación
    return auth_controller.handle_authentication_flow(screen)

if __name__ == "__main__":
    # Ejemplo de uso
    def main(screen):
        result = auth_flow_with_session_check(screen)
        screen.clear()
        screen.print_at(f"Resultado: {result}", 0, 0, Screen.COLOUR_WHITE)
        screen.refresh()
        screen.wait_for_input(5)
    
    Screen.wrapper(main)
