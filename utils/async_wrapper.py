"""
Utilidades para manejar funciones asíncronas con asciimatics
"""
import asyncio
import functools
from typing import Callable, Any


def async_screen_wrapper(async_func: Callable) -> Callable:
    """
    Decorador para envolver funciones async y que funcionen con Screen.wrapper()
    
    Usage:
        @async_screen_wrapper
        async def my_async_screen_function(screen):
            # ... código async ...
            pass
        
        Screen.wrapper(my_async_screen_function)
    """
    @functools.wraps(async_func)
    def wrapper(screen):
        loop = None
        try:
            # Intentar obtener el loop existente
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No hay loop corriendo, crear uno nuevo
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            created_new_loop = True
        else:
            created_new_loop = False
            
        try:
            result = loop.run_until_complete(async_func(screen))
            
            # Limpiar tareas pendientes
            pending_tasks = asyncio.all_tasks(loop)
            if pending_tasks:
                # Cancelar tareas pendientes
                for task in pending_tasks:
                    if not task.done():
                        task.cancel()
                
                # Esperar a que se cancelen
                loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
            
            return result
            
        except KeyboardInterrupt:
            # Manejar Ctrl+C gracefully
            return None
        except Exception as e:
            print(f"Error en función async: {e}")
            return None
        finally:
            # Limpiar si creamos el loop
            if created_new_loop and loop and not loop.is_closed():
                try:
                    loop.close()
                except Exception:
                    pass  # Ignorar errores al cerrar el loop
    
    return wrapper


def run_async_in_screen(async_func: Callable, *args, **kwargs) -> Any:
    """
    Ejecuta una función async dentro del contexto de una pantalla de asciimatics
    
    Args:
        async_func: La función async a ejecutar
        *args: Argumentos posicionales para la función
        **kwargs: Argumentos de palabra clave para la función
    
    Returns:
        El resultado de la función async
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(async_func(*args, **kwargs))


class AsyncScreenManager:
    """
    Gestor para manejar operaciones asíncronas en pantallas de asciimatics
    """
    
    def __init__(self):
        self._loop = None
    
    def ensure_loop(self):
        """Asegura que existe un loop de eventos"""
        if self._loop is None or self._loop.is_closed():
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop
    
    def run_async(self, coro):
        """Ejecuta una corrutina y retorna el resultado"""
        loop = self.ensure_loop()
        return loop.run_until_complete(coro)
    
    def close(self):
        """Cierra el loop de eventos"""
        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None


# Instancia global del gestor async
async_manager = AsyncScreenManager()
