"""
Archivo de prueba para el nuevo sistema de autenticación
"""
from asciimatics.screen import Screen
from utils.auth_controller import auth_flow_with_session_check

def test_auth_system(screen):
    """
    Prueba el sistema de autenticación completo.
    """
    screen.clear()
    
    # Mostrar mensaje de bienvenida
    screen.print_at("=== SISTEMA DE AUTENTICACIÓN CON FIRESTORE ===", 10, 2, Screen.COLOUR_CYAN)
    screen.print_at("Iniciando flujo de autenticación...", 10, 4, Screen.COLOUR_WHITE)
    screen.refresh()
    screen.wait_for_input(2)
    
    # Ejecutar flujo de autenticación
    result = auth_flow_with_session_check(screen)
    
    # Mostrar resultado
    screen.clear()
    
    if result['success']:
        if result.get('action') == 'existing_session':
            user_data = result['user_data']
            screen.print_at("=== SESIÓN EXISTENTE ENCONTRADA ===", 10, 2, Screen.COLOUR_GREEN)
            screen.print_at(f"Bienvenido de nuevo: {user_data.get('nombre', 'Usuario')} {user_data.get('apellido', '')}", 10, 4, Screen.COLOUR_WHITE)
            screen.print_at(f"Email: {user_data.get('correo', 'N/A')}", 10, 5, Screen.COLOUR_WHITE)
            screen.print_at(f"Saldo: ${user_data.get('saldo', 0)}", 10, 6, Screen.COLOUR_WHITE)
        else:
            user = result.get('user')
            if user:
                screen.print_at("=== AUTENTICACIÓN EXITOSA ===", 10, 2, Screen.COLOUR_GREEN)
                screen.print_at(f"Bienvenido: {user.get_nombre()} {user.get_apellido()}", 10, 4, Screen.COLOUR_WHITE)
                screen.print_at(f"Email: {user.get_correo()}", 10, 5, Screen.COLOUR_WHITE)
                screen.print_at(f"Saldo: ${user.get_saldo()}", 10, 6, Screen.COLOUR_WHITE)
            else:
                screen.print_at("=== AUTENTICACIÓN EXITOSA ===", 10, 2, Screen.COLOUR_GREEN)
                screen.print_at("Usuario autenticado correctamente", 10, 4, Screen.COLOUR_WHITE)
    else:
        screen.print_at("=== AUTENTICACIÓN CANCELADA ===", 10, 2, Screen.COLOUR_RED)
        screen.print_at(f"Acción: {result.get('action', 'desconocida')}", 10, 4, Screen.COLOUR_WHITE)
    
    screen.print_at("Presiona cualquier tecla para salir...", 10, 10, Screen.COLOUR_CYAN)
    screen.refresh()
    screen.wait_for_input(30)

if __name__ == "__main__":
    Screen.wrapper(test_auth_system)
