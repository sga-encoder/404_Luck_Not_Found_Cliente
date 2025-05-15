import os
import sys

# Añadir el directorio raíz del proyecto al path de Python
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def read_path(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo y devuelve su ruta absoluta.
    
    :param ruta_archivo: Ruta del archivo a leer.
    :return: Ruta absoluta del archivo.
    """
    try:
        # Obtener la ruta absoluta del directorio actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Construir la ruta absoluta del archivo
        ruta_absoluta = os.path.join(directorio_actual, ruta_archivo)
        return ruta_absoluta
    
    except Exception as e:
        print(f"Error al obtener la ruta del archivo: {e}")
        raise

def leer_archivo(ruta_archivo: str) -> str:
    try:
        with open(read_path(ruta_archivo), 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            return contenido
        
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no existe")
        raise
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        raise