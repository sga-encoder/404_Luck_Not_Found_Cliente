"""
Formulario de login - REDIRIGIR AL NUEVO SISTEMA CON FIRESTORE
Este archivo ahora redirige al nuevo sistema de autenticación basado en Firestore
"""
from asciimatics.screen import Screen
from ...utils.auth_controller import auth_flow_with_session_check

def login_form_with_print_form(screen):
    """
    Función principal que redirige al nuevo sistema de autenticación con Firestore.
    Mantiene compatibilidad con el código existente.
    """
    return auth_flow_with_session_check(screen)

if __name__ == "__main__":
    # Ejemplo de uso
    def main(screen):
        result = login_form_with_print_form(screen)
        screen.clear()
        screen.print_at(f"Resultado: {result}", 0, 0, Screen.COLOUR_WHITE)
        screen.refresh()
        screen.wait_for_input(5)
    
    Screen.wrapper(main)

if __name__ == "__main__":
    # Ejemplo de uso
    def main(screen):
        result = login_form_with_print_form(screen)
        screen.clear()
        screen.print_at(f"Resultado: {result}", 0, 0, Screen.COLOUR_WHITE)
        screen.refresh()
        screen.wait_for_input(5)
    
    Screen.wrapper(main)
