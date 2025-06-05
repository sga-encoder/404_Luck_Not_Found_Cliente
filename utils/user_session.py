"""
Módulo para manejar la persistencia local del usuario en el cliente
"""
import json
import os

from servidor.src.model.usuario import UsuarioServicio

class UserSessionManager:
    """
    Gestiona la sesión del usuario guardando y cargando datos desde un archivo JSON local.
    """
    
    def __init__(self, session_file_path: str = "activo/jugadorActivo.json"):
        """
        Inicializa el gestor de sesión de usuario.
        
        Args:
            session_file_path (str): Ruta del archivo donde se guardará la sesión del usuario.
        """
        self.session_file_path = session_file_path
        
    async def load(self, id):
        usuario_servicio = UsuarioServicio()
        usuario_data = await usuario_servicio.obtener_usuario(id)
        self.save_user_session(usuario_data.to_dict())
        return usuario_data.to_dict()

    def save_user_session(self, user_data: dict) -> bool:
        """
        Guarda los datos del usuario en el archivo JSON.
        
        Args:
            user_data (dict): Diccionario con los datos del usuario.
            
        Returns:
            bool: True si se guardó correctamente, False en caso de error.
        """
        try:
            with open(self.session_file_path, 'w', encoding='utf-8') as file:
                json.dump(user_data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar la sesión del usuario: {e}")
            return False
    
    async def load_user_session(self) -> dict | None:
        """
        Carga los datos del usuario desde el archivo JSON.
        
        Returns:
            dict | None: Diccionario con los datos del usuario o None si no existe o hay error.
        """
        try:
            if os.path.exists(self.session_file_path):
                with open(self.session_file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    print(f"Datos de sesión cargados: {json_data}")
                    data = await self.load(json_data.get('id'))
                    return data
            return None
        except Exception as e:
            print(f"Error al cargar la sesión del usuario: {e}")
            return None
    
    def clear_user_session(self) -> bool:
        """
        Elimina el archivo de sesión del usuario.
        
        Returns:
            bool: True si se eliminó correctamente, False en caso de error.
        """
        try:
            if os.path.exists(self.session_file_path):
                os.remove(self.session_file_path)
            return True
        except Exception as e:
            print(f"Error al eliminar la sesión del usuario: {e}")
            return False
    
    def has_active_session(self) -> bool:
        """
        Verifica si existe una sesión activa del usuario.
        
        Returns:
            bool: True si existe una sesión activa, False en caso contrario.
        """
        return os.path.exists(self.session_file_path)
    
    def update_user_session(self, updated_data: dict) -> bool:
        """
        Actualiza datos específicos de la sesión del usuario.
        
        Args:
            updated_data (dict): Datos a actualizar en la sesión.
            
        Returns:
            bool: True si se actualizó correctamente, False en caso de error.
        """
        try:
            current_session = self.load_user_session()
            if current_session:
                current_session.update(updated_data)
                return self.save_user_session(current_session)
            return False
        except Exception as e:
            print(f"Error al actualizar la sesión del usuario: {e}")
            return False
