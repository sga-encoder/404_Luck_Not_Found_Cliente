# Documentación de utilidades de view

# Documentación de utilidades de view

## print_text

La función `print_text` es la base del sistema de renderizado de texto en la terminal usando Asciimatics. Proporciona capacidades avanzadas de posicionamiento y soporte completo para arte ASCII.

### Características Principales

- **Renderizado de texto** simple y multilínea
- **Arte ASCII** con múltiples fuentes disponibles
- **Sistema de posicionamiento flexible** (absoluto, relativo, desde bordes)
- **Configuración visual completa** (colores, fondos)
- **Justificación de texto** para arte ASCII
- **Cálculo automático** de dimensiones y posición final

### Funcionamiento Interno

La función sigue este flujo de procesamiento:

1. **Validación**: Verifica que el diccionario contenga la clave 'text' obligatoria
2. **Configuración**: Extrae parámetros del diccionario con valores por defecto
3. **Procesamiento de texto**:
   - Si `asccii_art=True`: usa pyfiglet para generar arte ASCII
   - Si `asccii_art=False`: procesa texto normal con soporte multilínea
4. **Cálculo de dimensiones**: determina ancho y altura del texto final
5. **Cálculo de posición**: aplica sistema de posicionamiento con prioridades
6. **Renderizado**: dibuja el texto línea por línea en la pantalla
7. **Retorno**: devuelve información sobre dimensiones y posición final

### Sistema de Posicionamiento

El sistema de posicionamiento tiene **prioridades definidas**:

1. **Posicionamiento Absoluto** (máxima prioridad)

   - `x_position`, `y_position`: Coordenadas exactas
   - `x`, `y`: Alias para posicionamiento absoluto

2. **Posicionamiento Relativo al Centro**

   - `x-center`, `y-center`: Desplazamiento desde el centro de pantalla
   - El centro se calcula dinámicamente según el tamaño de pantalla

3. **Posicionamiento desde Bordes** (menor prioridad)
   - `x-right`: Distancia desde borde derecho
   - `y-bottom`: Distancia desde borde inferior

### Parámetros Detallados

#### Configuración de Contenido

| Parámetro | Tipo | Descripción                                          | Obligatorio |
| --------- | ---- | ---------------------------------------------------- | ----------- |
| `text`    | str  | Texto a mostrar (puede incluir `\n` para multilínea) | ✅ Sí       |

#### Configuración de Arte ASCII

| Parámetro   | Tipo | Descripción                                            | Por Defecto |
| ----------- | ---- | ------------------------------------------------------ | ----------- |
| `font`      | str  | Fuente ASCII ('slant', 'banner', 'big', 'block', etc.) | 'slant'     |
| `justify`   | str  | Justificación ('left', 'center', 'right')              | 'left'      |
| `max-width` | int  | Ancho máximo para arte ASCII                           | 100         |

#### Configuración Visual

| Parámetro | Tipo | Descripción                         | Por Defecto         |
| --------- | ---- | ----------------------------------- | ------------------- |
| `color`   | int  | Color del texto (Screen.COLOUR\_\*) | Screen.COLOUR_WHITE |
| `bg`      | int  | Color de fondo (Screen.COLOUR\_\*)  | None                |

#### Posicionamiento Absoluto

| Parámetro    | Tipo | Descripción                       |
| ------------ | ---- | --------------------------------- |
| `x_position` | int  | Posición X absoluta en caracteres |
| `y_position` | int  | Posición Y absoluta en líneas     |
| `x`          | int  | Alias para x_position             |
| `y`          | int  | Alias para y_position             |

#### Posicionamiento Relativo al Centro

| Parámetro  | Tipo | Descripción                                                         |
| ---------- | ---- | ------------------------------------------------------------------- |
| `x-center` | int  | Desplazamiento horizontal desde centro (- = izquierda, + = derecha) |
| `y-center` | int  | Desplazamiento vertical desde centro (- = arriba, + = abajo)        |

#### Posicionamiento desde Bordes

| Parámetro  | Tipo | Descripción                    |
| ---------- | ---- | ------------------------------ |
| `x-right`  | int  | Distancia desde borde derecho  |
| `y-bottom` | int  | Distancia desde borde inferior |

### Valores de Retorno

La función retorna un diccionario con información precisa sobre el renderizado:

```python
{
    'width': int,        # Ancho máximo del texto en caracteres
    'height': int,       # Altura total en líneas
    'x_position': int,   # Posición X final donde se renderizó
    'y_position': int    # Posición Y final donde se renderizó
}
```

### Ejemplos de Uso

#### 1. Texto Simple Centrado

```python
from src.view.utils.printers import print_text
from asciimatics.screen import Screen

# Texto centrado en pantalla
resultado = print_text(screen, {
    'text': 'Hola Mundo',
    'x-center': 0,
    'y-center': 0,
    'color': Screen.COLOUR_RED
})
print(f"Texto renderizado en: {resultado['x_position']}, {resultado['y_position']}")
```

#### 2. Arte ASCII con Fuente Personalizada

```python
# Título grande con arte ASCII
print_text(screen, {
    'text': 'CASINO ROYAL',
    'font': 'banner',           # Fuente grande y llamativa
    'justify': 'center',        # Centrar el arte ASCII
    'x-center': 0,
    'y': 5,
    'color': Screen.COLOUR_CYAN
}, asccii_art=True)
```

#### 3. Texto Multilínea con Posicionamiento Absoluto

```python
# Información del juego en posición fija
info_text = """Estado: En Juego
Jugadores: 2/4
Ronda: 3
Apuesta: $100"""

print_text(screen, {
    'text': info_text,
    'x_position': 10,
    'y_position': 20,
    'color': Screen.COLOUR_GREEN,
    'bg': Screen.COLOUR_BLACK
})
```

#### 4. Texto desde Esquina (Borde Derecho)

```python
# Marcador en esquina superior derecha
print_text(screen, {
    'text': 'Puntos: 1250',
    'x-right': 5,           # 5 caracteres desde borde derecho
    'y': 2,                 # Línea 2 desde arriba
    'color': Screen.COLOUR_YELLOW
})
```

#### 5. Menú con Múltiples Elementos

```python
def mostrar_menu(screen):
    # Título principal
    print_text(screen, {
        'text': 'MENU PRINCIPAL',
        'font': 'slant',
        'x-center': 0,
        'y': 3,
        'color': Screen.COLOUR_MAGENTA
    }, asccii_art=True)

    # Opciones del menú
    opciones = ["1. Jugar", "2. Configuración", "3. Salir"]

    for i, opcion in enumerate(opciones):
        print_text(screen, {
            'text': opcion,
            'x-center': 0,
            'y-center': i * 2,  # Espaciado vertical
            'color': Screen.COLOUR_WHITE
        })
```

#### 6. Sistema de Notificaciones

```python
def mostrar_notificacion(screen, mensaje, tipo="info"):
    colores = {
        "info": Screen.COLOUR_CYAN,
        "warning": Screen.COLOUR_YELLOW,
        "error": Screen.COLOUR_RED,
        "success": Screen.COLOUR_GREEN
    }

    resultado = print_text(screen, {
        'text': f"[{tipo.upper()}] {mensaje}",
        'x-center': 0,
        'y-bottom': 3,  # Cerca del borde inferior
        'color': colores.get(tipo, Screen.COLOUR_WHITE),
        'bg': Screen.COLOUR_BLACK
    })

    return resultado  # Para posicionar elementos relacionados
```

### Casos de Uso Avanzados

#### 1. Texto Adaptativo al Tamaño de Pantalla

```python
def titulo_adaptativo(screen, texto):
    # Calcular tamaño óptimo basado en pantalla
    if screen.width > 100:
        font = 'banner'
        max_width = screen.width - 10
    elif screen.width > 60:
        font = 'slant'
        max_width = screen.width - 5
    else:
        font = None  # Texto normal
        max_width = screen.width - 2

    if font:
        return print_text(screen, {
            'text': texto,
            'font': font,
            'max-width': max_width,
            'justify': 'center',
            'x-center': 0,
            'y': 2,
            'color': Screen.COLOUR_CYAN
        }, asccii_art=True)
    else:
        return print_text(screen, {
            'text': texto,
            'x-center': 0,
            'y': 2,
            'color': Screen.COLOUR_CYAN
        })
```

### Notas Importantes y Mejores Prácticas

1. **Validación de Entrada**: Siempre incluye la clave 'text' en el diccionario
2. **Gestión de Pantalla**: El texto se renderiza inmediatamente, usa `screen.refresh()` después
3. **Dimensiones Dinámicas**: Las dimensiones retornadas son precisas para posicionamiento posterior
4. **Memoria de Posición**: Guarda el resultado para referenciar posiciones en otros elementos
5. **Arte ASCII**: Puede generar texto mucho más grande que el original, planifica el espacio
6. **Texto Multilínea**: Cada `\n` cuenta como una línea adicional en height
7. **Colores de Fondo**: Solo se aplican a caracteres del texto, no llenan áreas completas
8. **Prioridad de Posicionamiento**: Recuerda el orden: absoluto > relativo > desde bordes

### Integración con Otros Componentes

La función `print_text` es utilizada internamente por:

- `print_button`: Para renderizar el texto del botón
- `print_card`: Para renderizar contenido de cartas y grids
- Sistema de menús y navegación
- Notificaciones y mensajes del sistema

### Ejemplo Completo: Dashboard de Juego

```python
def dashboard_casino(screen, datos_juego):
    screen.clear()

    # Título principal
    titulo = print_text(screen, {
        'text': 'CASINO DASHBOARD',
        'font': 'slant',
        'x-center': 0,
        'y': 1,
        'color': Screen.COLOUR_CYAN
    }, asccii_art=True)

    # Información del jugador (esquina superior izquierda)
    info_jugador = f"""Jugador: {datos_juego['nombre']}
Dinero: ${datos_juego['dinero']}
Nivel: {datos_juego['nivel']}"""

    print_text(screen, {
        'text': info_jugador,
        'x': 2,
        'y': titulo['y_position'] + titulo['height'] + 2,
        'color': Screen.COLOUR_GREEN,
        'bg': Screen.COLOUR_BLACK
    })

    # Estado del juego (centro)
    print_text(screen, {
        'text': f"Mesa: {datos_juego['mesa']}\nApuesta Actual: ${datos_juego['apuesta']}",
        'x-center': 0,
        'y-center': -2,
        'color': Screen.COLOUR_WHITE
    })

    # Estadísticas (esquina superior derecha)
    stats = f"""Victorias: {datos_juego['victorias']}
Derrotas: {datos_juego['derrotas']}
Racha: {datos_juego['racha']}"""

    print_text(screen, {
        'text': stats,
        'x-right': 2,
        'y': titulo['y_position'] + titulo['height'] + 2,
        'color': Screen.COLOUR_YELLOW
    })

    # Mensaje de estado (parte inferior)
    print_text(screen, {
        'text': datos_juego['mensaje_estado'],
        'x-center': 0,
        'y-bottom': 3,
        'color': Screen.COLOUR_MAGENTA
    })

    screen.refresh()

# Uso del dashboard
datos = {
    'nombre': 'Jugador1',
    'dinero': 1500,
    'nivel': 5,
    'mesa': 'Blackjack #3',
    'apuesta': 50,
    'victorias': 12,
    'derrotas': 8,
    'racha': 3,
    'mensaje_estado': 'Tu turno - Elige tu acción'
}

Screen.wrapper(lambda screen: dashboard_casino(screen, datos))
```

---

## print_button

Dibuja un "botón" en la pantalla (bloque de texto con formato) y detecta si ha sido presionado mediante un clic del mouse.

**Parámetros:**

- `screen`: Objeto Screen de asciimatics donde se imprimirá el botón.
- `data` (dict): Igual que en print_text, describe el texto y formato del botón.
- `event`: Evento de entrada (generalmente un MouseEvent) a evaluar para detectar el clic.
- `click` (callable, opcional): Función a ejecutar si el botón es presionado.

**Retorna:**
Un diccionario con:

- 'result': Resultado de la función click() si se presionó el botón, None en caso contrario.
- 'width', 'height', 'x_position', 'y_position': Dimensiones y posición del botón.

**Notas importantes:**

- Debes activar el modo mouse: antes de usar botones con clic, asegúrate de tener `screen.mouse = True`.
- El orden importa: siempre llama a `screen.refresh()` antes de `screen.get_event()`.
- El área de clic del botón cubre todo el bloque de texto generado, no solo una línea.
- El evento debe ser un objeto MouseEvent y debe tener `event.buttons != 0` para que se considere un clic.
- El botón puede tener varias líneas (por ejemplo, si el texto contiene saltos de línea o es arte ASCII).
- El área de detección se calcula usando el ancho máximo y la altura total del texto renderizado.
- Si el usuario hace clic dentro de esa área, se ejecuta la función click y su resultado se devuelve en 'result'.

**Ejemplo:**

```python
screen.mouse = True  # Habilitar eventos de mouse
data = {
    'text': 'Hola mundo',
    'x-center': 0,
    'y-center': 0,
    'color': Screen.COLOUR_RED
}
while True:
    screen.refresh()  # Refresca antes de obtener el evento
    event = screen.get_event()
    resultado = print_button(screen, data, event, click=lambda: True)
    if resultado['result']:
        print("¡Botón presionado!")
```

---

## print_card

La función `print_card` es una utilidad avanzada para crear cartas visuales interactivas en la terminal con soporte para detección de clicks del mouse, incluyendo un sistema de cooldown para prevenir clicks múltiples accidentales.

### Características Principales

- **Cartas visuales personalizables** con bordes ASCII
- **Grid interactivo** con detección de clicks por columna o fila
- **Sistema de cooldown** para prevenir spam clicking
- **Detección de clicks precisas** con IDs únicos por elemento
- **Soporte para contenido dinámico** en cada celda del grid

### Uso Básico

#### 1. Configuración Inicial

```python
from src.view.utils.printers import print_card
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent

def mi_juego(screen):
    screen.mouse = True  # ¡IMPORTANTE! Habilitar mouse

    while True:
        # Tu lógica del juego aquí

        screen.refresh()  # ¡IMPORTANTE! Refrescar antes de get_event()
        event = screen.get_event()

        # Guardar el último MouseEvent válido (recomendado)
        if not hasattr(mi_juego, 'last_mouse_event'):
            mi_juego.last_mouse_event = None
        if isinstance(event, MouseEvent):
            mi_juego.last_mouse_event = event

        # Usar el evento guardado
        event_mouse = mi_juego.last_mouse_event
```

#### 2. Carta Simple con Click

```python
# Carta básica clickeable
card_data = {
    'width': 30,
    'height': 15,
    'text': 'Mi Carta',
    'x-center': 0,
    'y-center': 0,
    'color': Screen.COLOUR_WHITE,
}

resultado = print_card(screen, card_data, event_mouse, click=lambda: "carta_clickeada")

if resultado['result'] == "carta_clickeada":
    print("¡Carta clickeada!")
```

#### 3. Grid Interactivo con Clicks por Columna

```python
# Grid 3x3 con clicks por columna
card_data = {
    'width': 55,
    'height': 27,
    'x-center': 0,
    'y-center': 0,
    'grid': True,
    'grid_divider_x': 3,  # 3 columnas
    'grid_divider_y': 3,  # 3 filas
    'grid_click': 'column',  # Detectar clicks por columna
    'click': {
        '0': {'event': event_mouse, 'test': True, 'click': lambda: 'columna_0'},
        '1': {'event': event_mouse, 'test': True, 'click': lambda: 'columna_1'},
        '2': {'event': event_mouse, 'test': True, 'click': lambda: 'columna_2'},
    },
    'content': {
        # Contenido para cada celda (0-8 para un grid 3x3)
        str(i): {
            'text': f'Celda {i}',
            'padding-top': 1,
            'padding-left': 2,
            'color': Screen.COLOUR_WHITE,
        } for i in range(9)
    },
    'color': Screen.COLOUR_MAGENTA,
}

resultado = print_card(screen, card_data, event_mouse)

# Procesar clicks (resultado['result'] es una lista)
for idx, click_result in enumerate(resultado['result']):
    if click_result is not None:
        print(f"Click detectado en columna: {idx}")
        # Cambiar color de la columna clickeada
        for cell_idx in range(idx, 9, 3):  # Celdas de la columna
            card_data['content'][str(cell_idx)]['color'] = Screen.COLOUR_GREEN
```

### Ejemplos Avanzados

#### 1. Juego de Knucklebones con Sistema de Colores

```python
def knucklebones_game(screen):
    screen.mouse = True
    screen.clear()

    # Estado del juego
    color = [Screen.COLOUR_DEFAULT] * 9  # Color para cada celda

    while True:
        screen.refresh()
        event = screen.get_event()

        # Gestión de eventos de mouse
        if not hasattr(knucklebones_game, 'last_mouse_event'):
            knucklebones_game.last_mouse_event = None
        if isinstance(event, MouseEvent):
            knucklebones_game.last_mouse_event = event
        event_mouse = knucklebones_game.last_mouse_event

        # Configuración del grid del jugador 1
        player1_card = {
            'width': 55,
            'height': 27,
            'x-center': -40,  # Posición izquierda
            'y-center': 0,
            'grid': True,
            'grid_divider_x': 3,
            'grid_divider_y': 3,
            'grid_click': 'column',
            'click': {
                '0': {'event': event_mouse, 'test': True, 'click': lambda: '0'},
                '1': {'event': event_mouse, 'test': True, 'click': lambda: '1'},
                '2': {'event': event_mouse, 'test': True, 'click': lambda: '2'},
            },
            'content': {
                str(i): {
                    'text': get_dado((i % 3) + 1),  # Función que devuelve ASCII del dado
                    'padding-top': 1,
                    'padding-left': 2,
                    'color': color[i],
                } for i in range(9)
            },
            'color': Screen.COLOUR_MAGENTA,
        }

        # Renderizar y procesar clicks
        resultado = print_card(screen, player1_card, event_mouse)

        # Actualizar colores basado en clicks
        for idx, click_result in enumerate(resultado['result']):
            if click_result is not None:
                print(f"Click en columna: {idx}")
                # Alternar color de toda la columna
                for row in range(3):
                    cell_idx = idx + (row * 3)
                    color[cell_idx] = Screen.COLOUR_GREEN if color[cell_idx] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT

        # Salir del juego
        if event and hasattr(event, 'key_code') and event.key_code == ord('q'):
            break
```

#### 2. Grid con Clicks por Fila

```python
# Configuración para clicks por fila en lugar de columna
card_data = {
    'width': 40,
    'height': 20,
    'grid': True,
    'grid_divider_x': 2,
    'grid_divider_y': 3,
    'grid_click': 'row',  # Cambiar a detección por fila
    'click': {
        '0': {'event': event_mouse, 'click': lambda: 'fila_0'},
        '1': {'event': event_mouse, 'click': lambda: 'fila_1'},
        '2': {'event': event_mouse, 'click': lambda: 'fila_2'},
    },
    # ... resto de la configuración
}
```

#### 3. Carta con Contenido Dinámico y Botones

```python
# Grid con botones individuales en las celdas
card_data = {
    'width': 60,
    'height': 30,
    'grid': True,
    'grid_divider_x': 2,
    'grid_divider_y': 2,
    'content': {
        '0': {
            'text': 'Botón 1',
            'color': Screen.COLOUR_RED,
            'button': True,  # Hacer esta celda un botón
            'event': event_mouse,
            'click': lambda: 'boton_1_clickeado'
        },
        '1': {
            'text': 'Botón 2',
            'color': Screen.COLOUR_BLUE,
            'button': True,
            'event': event_mouse,
            'click': lambda: 'boton_2_clickeado'
        },
        # ... más celdas
    }
}
```

### Sistema de Cooldown

El sistema de cooldown previene clicks múltiples accidentales. Cada elemento tiene un ID único y un tiempo de espera de 0.3 segundos por defecto.

#### Funciones de Gestión de Cooldown

```python
from src.view.utils.events import clear_click_cooldowns, get_remaining_cooldown, set_custom_cooldown

# Limpiar todos los cooldowns (útil al cambiar de pantalla)
clear_click_cooldowns()

# Establecer cooldown personalizado
set_custom_cooldown("mi_elemento", 1.0)  # 1 segundo de cooldown

# Verificar tiempo restante
tiempo_restante = get_remaining_cooldown("grid_column_0_100_50")
if tiempo_restante > 0:
    print(f"Cooldown activo: {tiempo_restante:.1f}s restantes")
```

### Parámetros Completos de `print_card`

| Parámetro        | Tipo | Descripción                               | Por Defecto             |
| ---------------- | ---- | ----------------------------------------- | ----------------------- |
| `width`          | int  | Ancho de la carta                         | 21                      |
| `height`         | int  | Alto de la carta                          | 13                      |
| `text`           | str  | Texto dentro de la carta                  | ''                      |
| `ascii_x`        | str  | Caracter para bordes horizontales         | '─'                     |
| `ascii_y`        | str  | Caracter para bordes verticales           | '│'                     |
| `corner`         | list | Caracteres de esquinas [TL, TR, BL, BR]   | ['╭', '╮', '╰', '╯']    |
| `color`          | int  | Color del texto y bordes                  | `Screen.COLOUR_WHITE`   |
| `bg`             | int  | Color de fondo                            | `Screen.COLOUR_DEFAULT` |
| `grid`           | bool | Habilitar modo grid                       | False                   |
| `grid_divider_x` | int  | Número de columnas                        | 2                       |
| `grid_divider_y` | int  | Número de filas                           | 2                       |
| `grid_click`     | str  | Tipo de detección: 'column', 'row' o None | None                    |
| `click`          | dict | Configuración de clicks por área          | {}                      |
| `content`        | dict | Contenido de cada celda del grid          | {}                      |

### Posicionamiento

```python
# Posicionamiento absoluto
card_data = {'x_position': 10, 'y_position': 5}

# Posicionamiento relativo al centro
card_data = {'x-center': -20, 'y-center': 10}  # 20 chars a la izquierda, 10 abajo del centro

# Posicionamiento desde bordes
card_data = {'x-right': 5, 'y-bottom': 3}  # 5 chars desde el borde derecho, 3 desde abajo
```

### Consejos y Mejores Prácticas

1. **Siempre habilitar mouse**: `screen.mouse = True`
2. **Refrescar antes de eventos**: `screen.refresh()` antes de `screen.get_event()`
3. **Guardar MouseEvents**: Mantener referencia al último MouseEvent válido
4. **IDs únicos**: El sistema genera IDs únicos automáticamente para el cooldown
5. **Limpiar cooldowns**: Usar `clear_click_cooldowns()` al cambiar de pantalla
6. **Test mode**: Usar `'test': True` en clicks para ver áreas clickeables
7. **Manejar resultados**: `resultado['result']` puede ser None, un valor, o una lista

### Ejemplo Completo Funcional

```python
from src.view.utils.printers import print_card
from src.view.utils.events import clear_click_cooldowns
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent

def ejemplo_completo(screen):
    screen.mouse = True
    clear_click_cooldowns()  # Limpiar cooldowns previos

    colors = [Screen.COLOUR_DEFAULT] * 9
    running = True

    while running:
        screen.clear()
        screen.refresh()
        event = screen.get_event()

        # Gestión de eventos
        if not hasattr(ejemplo_completo, 'last_mouse_event'):
            ejemplo_completo.last_mouse_event = None
        if isinstance(event, MouseEvent):
            ejemplo_completo.last_mouse_event = event
        event_mouse = ejemplo_completo.last_mouse_event

        # Configuración de carta
        card_config = {
            'width': 45,
            'height': 25,
            'x-center': 0,
            'y-center': 0,
            'grid': True,
            'grid_divider_x': 3,
            'grid_divider_y': 3,
            'grid_click': 'column',
            'click': {
                str(i): {
                    'event': event_mouse,
                    'test': True,  # Mostrar áreas clickeables
                    'click': lambda col=i: f'columna_{col}'
                } for i in range(3)
            },
            'content': {
                str(i): {
                    'text': f'[{i}]',
                    'padding-top': 1,
                    'padding-left': 3,
                    'color': colors[i],
                } for i in range(9)
            },
            'color': Screen.COLOUR_CYAN,
        }

        # Renderizar y procesar
        resultado = print_card(screen, card_config, event_mouse)

        # Procesar clicks
        if resultado['result']:
            for idx, click_result in enumerate(resultado['result']):
                if click_result and click_result.startswith('columna_'):
                    col = int(click_result.split('_')[1])
                    # Cambiar color de toda la columna
                    for row in range(3):
                        cell_idx = col + (row * 3)
                        colors[cell_idx] = Screen.COLOUR_GREEN if colors[cell_idx] == Screen.COLOUR_DEFAULT else Screen.COLOUR_DEFAULT

        # Salir con 'q'
        if event and hasattr(event, 'key_code') and event.key_code == ord('q'):
            running = False

# Ejecutar ejemplo
if __name__ == "__main__":
    Screen.wrapper(ejemplo_completo)
```

---

## Funciones de Gestión de Eventos

### clear_click_cooldowns()

Limpia todos los cooldowns almacenados. Útil para resetear el estado entre pantallas.

```python
from src.view.utils.events import clear_click_cooldowns

# Al cambiar de pantalla o reiniciar juego
clear_click_cooldowns()
```

### set_custom_cooldown(element_id, cooldown_seconds)

Establece un cooldown personalizado para un elemento específico.

**Parámetros:**

- `element_id` (str): ID único del elemento
- `cooldown_seconds` (float): Tiempo de cooldown en segundos (por defecto 0.3)

```python
from src.view.utils.events import set_custom_cooldown

# Cooldown más largo para elementos críticos
set_custom_cooldown("boton_importante", 1.5)
```

### get_remaining_cooldown(element_id)

Obtiene el tiempo restante de cooldown para un elemento.

**Parámetros:**

- `element_id` (str): ID único del elemento

**Retorna:**

- `float`: Tiempo restante en segundos, 0 si no hay cooldown activo

```python
from src.view.utils.events import get_remaining_cooldown

tiempo_restante = get_remaining_cooldown("grid_column_0_100_50")
if tiempo_restante > 0:
    print(f"Espera {tiempo_restante:.1f}s antes del próximo click")
```

### add_mouse_listener(screen, data, event, callback, test, cooldown_seconds, element_id)

Función principal para detección de clicks con cooldown avanzado.

**Parámetros:**

- `screen`: Pantalla de asciimatics
- `data` (dict): Diccionario con posición y dimensiones (`x_position`, `y_position`, `width`, `height`)
- `event`: Evento de mouse
- `callback`: Función a ejecutar cuando se hace click
- `test` (bool): Si mostrar marcadores de debug (opcional, por defecto False)
- `cooldown_seconds` (float): Tiempo mínimo entre clicks (opcional, por defecto 0.3)
- `element_id` (str): ID único del elemento para el cooldown (opcional)

```python
from src.view.utils.events import add_mouse_listener

# Uso manual con cooldown personalizado
result = add_mouse_listener(
    screen=screen,
    data={'x_position': 10, 'y_position': 5, 'width': 20, 'height': 3},
    event=event_mouse,
    callback=lambda: "clickeado",
    test=True,
    cooldown_seconds=1.0,
    element_id="mi_boton_especial"
)
```

Esta documentación cubre todos los aspectos del sistema de clicks en `print_card`, desde uso básico hasta implementaciones avanzadas con gestión de estado y cooldowns.
