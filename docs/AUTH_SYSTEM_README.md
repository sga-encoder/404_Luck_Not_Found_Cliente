# Sistema de Autenticación con Firestore

Este documento describe el nuevo sistema de autenticación que utiliza Firestore directamente en lugar de Firebase Auth.

## Componentes del Sistema

### 1. **Servidor**

#### `UsuarioServicio.py` (Métodos Agregados)
- `buscar_usuario_por_correo(correo)`: Busca un usuario por su correo electrónico
- `autenticar_usuario(correo, contraseña)`: Autentica un usuario verificando correo y contraseña

### 2. **Cliente**

#### `utils/user_session.py`
Gestor de persistencia local del usuario:
- `save_user_session(user_data)`: Guarda la sesión del usuario en un archivo JSON
- `load_user_session()`: Carga la sesión del usuario desde el archivo JSON
- `clear_user_session()`: Elimina la sesión del usuario
- `has_active_session()`: Verifica si existe una sesión activa
- `update_user_session(updated_data)`: Actualiza datos específicos de la sesión

#### `utils/auth_controller.py`
Controlador principal de autenticación:
- `check_existing_session()`: Verifica sesiones existentes
- `handle_authentication_flow(screen)`: Maneja el flujo completo de login/registro
- `logout_user()`: Cierra la sesión del usuario

#### Formularios

##### `screens/forms/login_firestore_form.py`
- Formulario de login que usa solo email y contraseña
- Comunica directamente con Firestore a través de `UsuarioServicio`
- Maneja mensajes específicos: "correo no registrado" y "contraseña incorrecta"

##### `screens/forms/register_form.py`
- Formulario de registro con campos: nombre, apellido, email, contraseña, confirmar contraseña
- Usa el método `Usuario.crear_usuario()` del servidor
- Valida todos los campos según las reglas de negocio

##### `screens/forms/login_with_print_form.py` (Actualizado)
- Ahora redirige al nuevo sistema para mantener compatibilidad

## Flujo de Autenticación

### 1. **Verificación de Sesión Existente**
```python
from utils.auth_controller import auth_flow_with_session_check

result = auth_flow_with_session_check(screen)
if result['action'] == 'existing_session':
    # Usuario ya tiene sesión activa
    user_data = result['user_data']
```

### 2. **Login**
1. Usuario ingresa email y contraseña
2. Sistema busca usuario por correo en Firestore
3. Si no existe: "Correo no registrado"
4. Si existe: verifica contraseña
5. Si contraseña incorrecta: "Contraseña incorrecta"
6. Si todo es correcto: guarda sesión local y continúa

### 3. **Registro**
1. Usuario llena: nombre, apellido, email, contraseña, confirmar contraseña
2. Sistema valida todos los campos
3. Crea usuario usando `Usuario.crear_usuario()`
4. Guarda automáticamente en Firestore
5. Guarda sesión local

### 4. **Persistencia Local**
- Se crea archivo `user_session.json` en la carpeta del cliente
- Contiene todos los datos del usuario autenticado
- Se actualiza automáticamente cuando cambian los datos del usuario
- Se elimina al hacer logout

## Estructura del Archivo de Sesión

```json
{
    "id": "MJ123",
    "nombre": "Miguel",
    "apellido": "Ospina",
    "correo": "miguel@email.com",
    "contraseña": "password123",
    "saldo": 1000.0,
    "total_apostado": 0.0,
    "historial": []
}
```

## Comunicación Servidor-Cliente

El sistema utiliza importaciones directas para la comunicación:

```python
# En el cliente
sys.path.append(os.path.join(os.path.dirname(__file__), '../../servidor/src'))
from model.usuario.Usuario import Usuario
from model.usuario.UsuarioServicio import UsuarioServicio
```

## Uso

### Implementación Básica
```python
from utils.auth_controller import auth_flow_with_session_check

def main(screen):
    result = auth_flow_with_session_check(screen)
    
    if result['success']:
        if result.get('action') == 'existing_session':
            user_data = result['user_data']
            print(f"Sesión existente: {user_data['nombre']}")
        else:
            user = result['user']
            print(f"Login exitoso: {user.get_nombre()}")
    else:
        print("Autenticación cancelada")
```

### Logout
```python
from utils.auth_controller import AuthController

auth_controller = AuthController()
auth_controller.logout_user()  # Elimina la sesión local
```

## Configuración

### Ubicación del Archivo de Sesión
Por defecto se guarda como `user_session.json` en la carpeta del cliente. Para cambiar la ubicación:

```python
from utils.user_session import UserSessionManager

# Cambiar ubicación
session_manager = UserSessionManager("ruta/personalizada/session.json")
```

## Ventajas del Nuevo Sistema

1. **Simplicidad**: No depende de Firebase Auth
2. **Control total**: Manejo directo de la lógica de autenticación
3. **Persistencia local**: Sesiones persistentes sin depender de tokens externos
4. **Flexibilidad**: Fácil modificación de la lógica de autenticación
5. **Integración directa**: Usa las clases existentes del servidor
