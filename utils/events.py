from asciimatics.event import MouseEvent, KeyboardEvent
from asciimatics.screen import Screen
import time

from .printers import print_text

# Diccionario global para almacenar los últimos tiempos de click por elemento
_last_click_times = {}

def key_listener_test(screen, event):
    """
    Función de debug para mostrar información sobre las teclas presionadas.
    Muestra el debug directamente en pantalla y también retorna el texto.
    
    Args:
        screen: Pantalla de asciimatics donde mostrar el debug.
        event: Evento de entrada (generalmente obtenido con screen.get_event()).
        
    Returns:
        str: Descripción de la tecla presionada o cadena vacía si no es un evento de teclado.
    """
    debug_key = ""
    if event and isinstance(event, KeyboardEvent):
        key_names = {
            -301: "TAB",
            10: "ENTER (LF)",
            13: "ENTER (CR)",
            -1: "ESCAPE",
            -300: "BACKSPACE",
            -203: "FLECHA ←",
            -205: "FLECHA →",
            -204: "FLECHA ↑",
            -206: "FLECHA ↓",
            32: "ESPACIO"
        }
        
        if event.key_code in key_names:
            debug_key = f"Tecla: {key_names[event.key_code]} (código: {event.key_code})"
        elif 32 <= event.key_code <= 126:
            debug_key = f"Carácter: '{chr(event.key_code)}' (código: {event.key_code})"
        else:
            debug_key = f"Tecla desconocida (código: {event.key_code})"
        
        # Mostrar debug de teclas en pantalla
        if debug_key:
            print_text(screen, {
                'text': debug_key,
                'x-center': 0,
                'y-bottom': 0,
                'color': Screen.COLOUR_MAGENTA,
                'bg': Screen.COLOUR_BLACK
            })
    
    return debug_key

def add_key_listener(key_codes, event, callback):
    """
    Agrega un listener para una o varias teclas específicas en la pantalla.

    Args:
        key_codes (int | list): Código(s) de la(s) tecla(s) a escuchar.
        event: Evento de entrada (generalmente obtenido con screen.get_event()).
        callback (callable): Función a ejecutar cuando se presiona la tecla.

    Returns:
        None
    """
    if not isinstance(key_codes, (list, tuple)):
        key_codes = [key_codes]
    if event is not None and hasattr(event, 'key_code') and event.key_code in key_codes:
        return callback()
        
    return None

def add_mouse_listener(screen, data, event, callback, test=False, cooldown_seconds=0.3, element_id=None):
    """
    Agrega un listener de mouse con capacidad de cooldown para evitar clicks múltiples rápidos.
    
    Args:
        screen: Pantalla de asciimatics
        data: Diccionario con datos de posición y dimensiones
        event: Evento de mouse
        callback: Función a ejecutar cuando se hace click
        test: Si mostrar marcadores de debug
        cooldown_seconds: Tiempo mínimo entre clicks (en segundos)
        element_id: ID único del elemento para el cooldown (opcional)
    """
    # print(f"[DEBUG] add_mouse_listener llamada. Data: {data}")
    if event is not None:
        if test:
            print_text(screen, {'text': f'8', 'x_position': data['x_position'], 'y_position': data['y_position'], 'color': Screen.COLOUR_RED})
            print_text(screen, {'text': f'8', 'x_position': data['x_position']+data['width'], 'y_position': data['y_position'], 'color': Screen.COLOUR_RED})
            print_text(screen, {'text': f'8', 'x_position': data['x_position']+data['width'], 'y_position': data['y_position']+data['height'], 'color': Screen.COLOUR_RED})
            print_text(screen, {'text': f'8', 'x_position': data['x_position'], 'y_position': data['y_position']+data['height'], 'color': Screen.COLOUR_RED})
        # print(f"[DEBUG] Tipo de evento recibido: {type(event)}")
        if isinstance(event, MouseEvent):
            # print(f"[DEBUG] MouseEvent: x={event.x}, y={event.y}, buttons={event.buttons}")
            # print(f"[DEBUG] Área fila/columna: x={data['x_position']} y={data['y_position']} w={data['width']} h={data['height']}")
            if event.buttons != 0:
                
                if data['x_position'] <= event.x < data['x_position'] + data['width'] and data['y_position'] <= event.y < data['y_position'] + data['height']:
                    
                    # Verificar cooldown si se especifica un element_id
                    if element_id is not None:
                        current_time = time.time()
                        last_click_time = _last_click_times.get(element_id, 0)
                        
                        # Si no ha pasado suficiente tiempo desde el último click, ignorar
                        if current_time - last_click_time < cooldown_seconds:
                            return None
                        
                        # Actualizar el tiempo del último click
                        _last_click_times[element_id] = current_time
                    
                        # print("[DEBUG] ¡Click detectado en área!")
                    return callback()
    #             else:
    #                 # print("[DEBUG] Click dentro de MouseEvent pero fuera del área")
    #         else:
    #             print("[DEBUG] MouseEvent sin botón presionado")
    #     else:
    #         print(f"[DEBUG] Evento no es MouseEvent: {type(event)}")
    # else:
    #     print("[DEBUG] add_mouse_listener llamada sin evento")
    return None

def clear_click_cooldowns():
    """
    Limpia todos los cooldowns almacenados. Útil para resetear el estado entre pantallas.
    """
    global _last_click_times
    _last_click_times.clear()

def set_custom_cooldown(element_id, cooldown_seconds=0.3):
    """
    Establece un cooldown personalizado para un elemento específico.
    
    Args:
        element_id: ID único del elemento
        cooldown_seconds: Tiempo de cooldown en segundos
    """
    global _last_click_times
    current_time = time.time()
    _last_click_times[element_id] = current_time + cooldown_seconds

def get_remaining_cooldown(element_id):
    """
    Obtiene el tiempo restante de cooldown para un elemento.
    
    Args:
        element_id: ID único del elemento
        
    Returns:
        float: Tiempo restante en segundos, 0 si no hay cooldown activo
    """
    global _last_click_times
    if element_id not in _last_click_times:
        return 0
    
    current_time = time.time()
    last_click_time = _last_click_times[element_id]
    remaining = last_click_time - current_time
    return max(0, remaining)