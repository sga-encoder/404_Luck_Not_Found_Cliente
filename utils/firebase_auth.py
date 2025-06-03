"""
Utilidades de Firebase Authentication para el cliente
"""
import pyrebase
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Firebase para el cliente (Web App Config)
firebase_config = {
    "apiKey": "AIzaSyBvOiM2-qQp3YPXK8r7S5L8M9N1O2P3Q4R",
    "authDomain": "casino-virtual-7ddaa.firebaseapp.com",
    "projectId": "casino-virtual-7ddaa", 
    "storageBucket": "casino-virtual-7ddaa.appspot.com",
    "messagingSenderId": "104657042562380559855",
    "appId": "1:104657042562380559855:web:abcd1234efgh5678",
    "databaseURL": "https://casino-virtual-7ddaa-default-rtdb.firebaseio.com/"
}

# Inicializar Firebase
try:
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
    database = firebase.database()
    print("Firebase inicializado correctamente")
except Exception as e:
    print(f"Error al inicializar Firebase: {e}")
    auth = None
    database = None

class FirebaseAuthManager:
    """Manejador de autenticación con Firebase"""
    def __init__(self):
        self.current_user = None
        self.id_token = None
    
    def register_user(self, email: str, password: str) -> dict:
        """
        Registra un nuevo usuario con email y contraseña
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña del usuario
            
        Returns:
            dict: Resultado del registro con 'success', 'message' y 'user'
        """        
        if not auth:
            return {
                'success': False,
                'message': 'Error: Firebase no está configurado correctamente',
                'user': None
            }
            
        try:
            print(f"Intentando registrar usuario: {email}")
            # Crear usuario en Firebase Auth
            user = auth.create_user_with_email_and_password(email, password)
            print(f"Usuario creado exitosamente: {user.get('localId', 'ID no disponible')}")
              # Enviar email de verificación
            try:
                auth.send_email_verification(user['idToken'])
                print("Email de verificación enviado")
            except Exception as e:
                print(f"Error al enviar email de verificación: {e}")
                # No fallar el registro por esto
            
            self.current_user = user
            self.id_token = user['idToken']
            
            return {
                'success': True,
                'message': 'Usuario registrado exitosamente. Verifica tu email.',
                'user': user['localId'],
                'email': email
            }
            
        except Exception as e:
            error_message = str(e)
            print(f"Error completo al registrar usuario: {error_message}")
            print(f"Tipo de error: {type(e)}")
            
            # Manejar errores específicos de Firebase
            if "EMAIL_EXISTS" in error_message:
                return {
                    'success': False,
                    'message': 'El email ya está registrado',
                    'user': None
                }
            elif "WEAK_PASSWORD" in error_message:
                return {
                    'success': False,
                    'message': 'La contraseña debe tener al menos 6 caracteres',
                    'user': None
                }
            elif "INVALID_EMAIL" in error_message:
                return {
                    'success': False,
                    'message': 'El formato del email no es válido',
                    'user': None
                }
            elif "API_KEY_INVALID" in error_message or "Bad Request" in error_message:
                return {
                    'success': False,
                    'message': 'Error de configuración de Firebase. Contacte al administrador.',
                    'user': None
                }
            else:
                return {
                    'success': False,
                    'message': f'Error al registrar usuario: {error_message}',
                    'user': None
                }
    
    def login_user(self, email: str, password: str) -> dict:
        """
        Inicia sesión con email y contraseña
        
        Args:
            email (str): Email del usuario
            password (str): Contraseña del usuario
            
        Returns:
            dict: Resultado del login con 'success', 'message' y 'user'
        """
        try:
            # Autenticar usuario
            user = auth.sign_in_with_email_and_password(email, password)
            
            # Verificar si el email está verificado
            account_info = auth.get_account_info(user['idToken'])
            if not account_info['users'][0]['emailVerified']:
                return {
                    'success': False,
                    'message': 'Por favor verifica tu email antes de iniciar sesión',
                    'user': None
                }
            
            self.current_user = user
            self.id_token = user['idToken']
            
            return {
                'success': True,
                'message': 'Inicio de sesión exitoso',
                'user': user['localId'],
                'email': email
            }
            
        except Exception as e:
            error_message = str(e)
            
            # Manejar errores específicos de Firebase
            if "INVALID_PASSWORD" in error_message or "EMAIL_NOT_FOUND" in error_message:
                return {
                    'success': False,
                    'message': 'Email o contraseña incorrectos',
                    'user': None
                }
            elif "USER_DISABLED" in error_message:
                return {
                    'success': False,
                    'message': 'Esta cuenta ha sido deshabilitada',
                    'user': None
                }
            else:
                return {
                    'success': False,
                    'message': f'Error al iniciar sesión: {error_message}',
                    'user': None
                }
    
    def logout_user(self) -> dict:
        """
        Cierra la sesión del usuario actual
        
        Returns:
            dict: Resultado del logout
        """
        try:
            self.current_user = None
            self.id_token = None
            
            return {
                'success': True,
                'message': 'Sesión cerrada exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al cerrar sesión: {str(e)}'
            }
    
    def reset_password(self, email: str) -> dict:
        """
        Envía un email para restablecer la contraseña
        
        Args:
            email (str): Email del usuario
            
        Returns:
            dict: Resultado del restablecimiento
        """
        try:
            auth.send_password_reset_email(email)
            
            return {
                'success': True,
                'message': 'Email de restablecimiento enviado'
            }
            
        except Exception as e:
            error_message = str(e)
            
            if "EMAIL_NOT_FOUND" in error_message:
                return {
                    'success': False,
                    'message': 'No se encontró una cuenta con ese email'
                }
            else:
                return {
                    'success': False,
                    'message': f'Error al enviar email: {error_message}'
                }
    
    def is_authenticated(self) -> bool:
        """
        Verifica si hay un usuario autenticado
        
        Returns:
            bool: True si hay usuario autenticado
        """
        return self.current_user is not None and self.id_token is not None
    
    def get_current_user_info(self) -> dict:
        """
        Obtiene información del usuario actual
        
        Returns:
            dict: Información del usuario o None
        """
        if not self.is_authenticated():
            return None
            
        try:
            account_info = auth.get_account_info(self.id_token)
            user_data = account_info['users'][0]
            
            return {
                'user_id': user_data['localId'],
                'email': user_data['email'],
                'email_verified': user_data['emailVerified'],
                'created_at': user_data['createdAt']
            }
            
        except Exception as e:
            return None

# Instancia global del manejador de autenticación
firebase_auth_manager = FirebaseAuthManager()
