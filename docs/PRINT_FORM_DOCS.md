# Documentación de print_form

## Descripción

La función `print_form` es una función avanzada para crear formularios dinámicos con inputs, botones y navegación automática. Encapsula toda la funcionalidad de formularios en una sola función reutilizable.

## Características

- ✅ **Inputs dinámicos**: Texto y contraseña con validación
- ✅ **Botones configurables**: Simples o en grid usando print_card
- ✅ **Contenedores opcionales**: Usando print_card para marco visual
- ✅ **Navegación automática**: TAB, ENTER, ESC
- ✅ **Validación de campos**: Requeridos, longitud mínima/máxima, validadores personalizados
- ✅ **Manejo de eventos**: Teclado y mouse automático
- ✅ **Posicionamiento flexible**: Absoluto y relativo

## Estructura de Configuración

```python
form_config = {
    # Configuración general
    'title': 'TÍTULO DEL FORMULARIO',           # Opcional
    'title_config': {                           # Opcional - configuración del título
        'font': 'slant',
        'color': Screen.COLOUR_CYAN,
        'x-center': 0,
        'y': 2
    },

    # Contenedor opcional
    'container': {                              # Opcional - usa print_card
        'width': 50,
        'height': 18,
        'x-center': 0,
        'y-center': 0,
        'corner': ['╭', '╮', '╰', '╯'],
        'ascii_x': '─',
        'ascii_y': '│'
    },

    # Inputs (obligatorio si hay inputs)
    'inputs': {
        'campo_id': {                           # ID único del campo
            'label': 'Etiqueta:',              # Obligatorio
            'width': 30,                       # Obligatorio
            'height': 4,                       # Obligatorio
            'x-center': 0,                     # Posicionamiento
            'y-center': -2,
            'placeholder': 'Texto placeholder', # Opcional
            'is_password': False,              # Opcional - para campos de contraseña
            'max_length': 20,                  # Opcional
            'color_focused': Screen.COLOUR_YELLOW,  # Opcional
            'color_normal': Screen.COLOUR_WHITE     # Opcional
        }
    },

    # Botones
    'buttons': {
        # Opción 1: Botones simples
        'btn_id': {
            'text': 'TEXTO BOTÓN',
            'x-center': 0,
            'y-center': 5,
            'action': 'submit',  # 'submit', 'cancel', o personalizada
            'color': Screen.COLOUR_GREEN
        },

        # Opción 2: Botones en grid (usa print_card)
        'grid': True,
        'width': 40,
        'height': 3,
        'grid_divider_x': 2,
        'grid_divider_y': 1,
        'content': {
            '0': {
                'text': 'ACEPTAR',
                'button': True,
                'action': 'submit'
            },
            '1': {
                'text': 'CANCELAR',
                'button': True,
                'action': 'cancel'
            }
        }
    },

    # Validación
    'validation': {                             # Opcional
        'campo_id': {
            'required': True,                   # Campo obligatorio
            'min_length': 3,                   # Longitud mínima
            'max_length': 20,                  # Longitud máxima
            'custom': lambda value: '@' in value  # Validador personalizado
        }
    },

    # Navegación
    'navigation_order': ['campo1', 'campo2', 'btn_0', 'btn_1'],  # Opcional
    'initial_focus': 'campo1',                  # Opcional

    # Eventos personalizados
    'key_handlers': {                           # Opcional
        102: lambda: print("F pressed")        # Código de tecla: función
    }
}
```

## Valor de Retorno

```python
{
    'form_state': {
        'current_field': 'campo_actual',        # Campo con focus actual
        'form_data': {                          # Datos de todos los inputs
            'campo1': 'valor1',
            'campo2': 'valor2'
        },
        'result': {                             # Resultado si se completó
            'action': 'submit',                 # 'submit', 'cancel', etc.
            'data': {                           # Datos del formulario
                'campo1': 'valor1',
                'campo2': 'valor2'
            }
        },
        'show_error': False,                    # Si hay error visible
        'error_message': ''                     # Mensaje de error
    },
    'position': {                               # Información de posición
        'x': 10,                               # Posición X del formulario
        'y': 5,                                # Posición Y del formulario
        'width': 50,                           # Ancho total
        'height': 18                           # Alto total
    },
    'inputs_data': {                           # Estados detallados de inputs
        'campo1': {
            'input_state': {...},              # Estado del input
            'width': 30,
            'height': 4,
            'x_position': 15,
            'y_position': 8
        }
    }
}
```

## Ejemplos de Uso

### Ejemplo 1: Formulario de Login Completo

```python
def login_form(screen):
    form_config = {
        'title': 'INICIAR SESIÓN',
        'title_config': {
            'font': 'slant',
            'x-center': 0,
            'y': 2,
            'color': Screen.COLOUR_CYAN
        },
        'container': {
            'width': 50,
            'height': 18,
            'x-center': 0,
            'y-center': 0
        },
        'inputs': {
            'usuario': {
                'label': 'Usuario:',
                'width': 44,
                'height': 4,
                'x-center': 0,
                'y-center': -4,
                'placeholder': 'Ingresa tu usuario'
            },
            'password': {
                'label': 'Contraseña:',
                'width': 44,
                'height': 4,
                'x-center': 0,
                'y-center': 0,
                'placeholder': 'Ingresa tu contraseña',
                'is_password': True
            }
        },
        'buttons': {
            'grid': True,
            'width': 40,
            'height': 3,
            'x-center': 0,
            'y-center': 5,
            'grid_divider_x': 2,
            'content': {
                '0': {'text': 'INICIAR', 'action': 'submit'},
                '1': {'text': 'CANCELAR', 'action': 'cancel'}
            }
        },
        'validation': {
            'usuario': {'required': True, 'min_length': 3},
            'password': {'required': True, 'min_length': 4}
        }
    }

    while True:
        event = screen.get_event()
        result = print_form(screen, form_config, event)

        if result['form_state']['result']:
            return result['form_state']['result']

        screen.refresh()
```

### Ejemplo 2: Formulario Simple sin Contenedor

```python
def simple_form(screen):
    form_config = {
        'inputs': {
            'nombre': {
                'label': 'Nombre:',
                'width': 30,
                'height': 3,
                'x-center': 0,
                'y-center': -2
            }
        },
        'buttons': {
            'enviar': {
                'text': 'ENVIAR',
                'x-center': 0,
                'y-center': 2,
                'action': 'submit'
            }
        }
    }

    while True:
        event = screen.get_event()
        result = print_form(screen, form_config, event)

        if result['form_state']['result']:
            return result

        screen.refresh()
```

### Ejemplo 3: Formulario con Validación Personalizada

```python
def registration_form(screen):
    def validate_email(email):
        return '@' in email and '.' in email

    form_config = {
        'inputs': {
            'email': {
                'label': 'Email:',
                'width': 40,
                'height': 3,
                'x-center': 0,
                'y-center': 0
            }
        },
        'buttons': {
            'registrar': {
                'text': 'REGISTRAR',
                'x-center': 0,
                'y-center': 4,
                'action': 'submit'
            }
        },
        'validation': {
            'email': {
                'required': True,
                'min_length': 5,
                'custom': validate_email
            }
        }
    }

    # ... resto del código
```

## Acciones de Botones

### Acciones Predefinidas

- `'submit'`: Envía el formulario con validación
- `'cancel'`: Cancela el formulario

### Acciones Personalizadas

```python
'buttons': {
    'mi_boton': {
        'text': 'ACCIÓN PERSONALIZADA',
        'action': 'mi_accion_custom'
    }
}
```

El resultado será:

```python
{
    'action': 'mi_accion_custom',
    'data': {...}  # Datos del formulario
}
```

## Navegación

### Teclas Automáticas

- **TAB**: Siguiente campo
- **ENTER**: Confirmar/siguiente campo o ejecutar botón
- **ESC**: Cancelar formulario

### Orden de Navegación

Por defecto: inputs (alfabético) + botones (alfabético)

Personalizado:

```python
'navigation_order': ['campo1', 'campo2', 'btn_0', 'btn_1']
```

## Validación

### Tipos de Validación

```python
'validation': {
    'campo': {
        'required': True,                      # Campo obligatorio
        'min_length': 3,                      # Mínimo 3 caracteres
        'max_length': 20,                     # Máximo 20 caracteres
        'custom': lambda x: x.isdigit()       # Solo números
    }
}
```

### Mensajes de Error

Los errores se muestran automáticamente:

- "El campo X es requerido"
- "El campo X debe tener al menos N caracteres"
- "El campo X no puede tener más de N caracteres"
- "El campo X no es válido" (validación personalizada)

## Integración

Para usar en tu proyecto:

```python
from utils.printers import print_form
from asciimatics.screen import Screen

def mi_formulario(screen):
    screen.mouse = True  # Habilitar mouse

    # Configurar formulario
    form_config = { ... }

    # Bucle principal
    while True:
        screen.clear()
        event = screen.get_event()

        result = print_form(screen, form_config, event)

        if result['form_state']['result']:
            # Formulario completado
            return result['form_state']['result']

        screen.refresh()

# Ejecutar
Screen.wrapper(mi_formulario)
```

## Notas Importantes

1. **Estado Interno**: La función mantiene estado interno automáticamente
2. **Limpieza**: El estado se limpia automáticamente al finalizar
3. **Mouse**: Recuerda activar `screen.mouse = True`
4. **Eventos**: Siempre pasar el evento a la función
5. **Refresh**: Llamar `screen.refresh()` después de print_form
