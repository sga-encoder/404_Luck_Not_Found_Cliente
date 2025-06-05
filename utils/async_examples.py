"""
Ejemplo de cómo usar funciones async dentro de pantallas síncronas
"""
import asyncio
from cliente.utils.async_wrapper import run_async_in_screen


def ejemplo_pantalla_con_async(screen):
    """
    Ejemplo de una pantalla síncrona que necesita llamar funciones async
    """
    
    # Método 1: Usar la función helper
    resultado = run_async_in_screen(mi_funcion_async, screen)
    
    # Método 2: Usar asyncio.run directamente (Python 3.7+)
    resultado2 = asyncio.run(mi_funcion_async(screen))
    
    # Continuar con lógica síncrona
    return resultado


async def mi_funcion_async(screen):
    """Función async de ejemplo"""
    # Aquí va tu lógica async
    await asyncio.sleep(0.1)  # Simular operación async
    return "resultado"
