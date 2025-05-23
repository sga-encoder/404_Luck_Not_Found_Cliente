# 404 Luck Not Found - Cliente

Este proyecto es el cliente del casino virtual "404 Luck Not Found", desarrollado con Python y Kivy.

## Requisitos previos

- Python 3.9 o superior
- Poetry (gestor de dependencias)

## Instalación para desarrollo

### 1. Clonar el repositorio

```powershell
git clone [URL del repositorio]
cd 404_luck_not_found/cliente
```

### 2. Instalar Poetry (si no está instalado)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 3. Crear entorno virtual e instalar dependencias

```powershell
# Crear un entorno virtual en el directorio del proyecto
poetry config virtualenvs.in-project true

# Instalar todas las dependencias
poetry install
```

### 4. Activar el entorno virtual

```powershell
poetry shell
```

## Ejecución de la aplicación

### Modo normal

```powershell
# Desde dentro del entorno virtual
python CasinoScreenManager.py
```

O usando Poetry directamente:

```powershell
poetry run python CasinoScreenManager.py
```

### Modo desarrollo

Para ejecutar la versión de desarrollo con hot-reloading:

```powershell
# Editar CasinoScreenManager.py y cambiar la línea "main()" por:
# MyAppDev().run()

python CasinoScreenManager.py
```

## Estructura del proyecto

```
cliente/
├── CasinoScreenManager.py    # Punto de entrada principal
├── pyproject.toml           # Configuración de Poetry
├── src/
│   ├── assets/              # Recursos (imágenes, sonidos, etc.)
│   ├── screens/             # Pantallas de la aplicación
│   │   ├── inicio/          # Pantalla de inicio con sus componentes
│   │   │   ├── BottomBar/   # Barra de navegación inferior
│   │   │   └── JuegoSeccion/# Sección de juegos
│   │   └── portada/         # Pantalla de portada
│   └── CasinoScreenManager.kv # Definición KV del administrador de pantallas
```

## Dependencias principales

- **Kivy**: Framework para interfaz gráfica multiplataforma
- **websockets**: Comunicación con el servidor
- **asyncio**: Programación asíncrona para manejo de eventos
- **kivy-garden-frostedglass**: Efecto de vidrio escarchado en UI

## Consejos para desarrollo

- Las pantallas se definen en la carpeta `src/screens/`
- Los archivos `.kv` contienen la definición de la interfaz
- Los archivos `.py` contienen la lógica de la aplicación
- Para añadir una nueva pantalla:
  1. Crear una clase que herede de `Screen`
  2. Crear el archivo `.kv` correspondiente
  3. Registrar la pantalla en `CasinoScreenManager.py`