# Tipos de Layouts en Kivy

## BoxLayout
- **Propósito principal**: Organizar widgets en una fila (horizontal) o columna (vertical).
- **Características clave**:
  - Distribuye el espacio disponible entre sus hijos.
  - La propiedad `orientation` puede ser 'horizontal' (default) o 'vertical'.
  - Los widgets se colocan uno tras otro en la dirección especificada.
  - Controla la distribución del espacio con `size_hint` y `pos_hint`.
  - Usa `spacing` para definir el espacio entre widgets.
  - Utiliza `padding` para agregar margen interno.
- **Uso ideal**: Para disponer elementos secuencialmente (menús, barras de herramientas, formularios).

```kivy
BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)
    Button:
        text: 'Botón 1'
    Button:
        text: 'Botón 2'
```

## GridLayout
- **Propósito principal**: Organizar widgets en una cuadrícula.
- **Características clave**:
  - Requiere definir `cols` (columnas) o `rows` (filas).
  - Los widgets se colocan de izquierda a derecha, fila por fila.
  - Admite `col_default_width`, `row_default_height`, `col_force_default` y `row_force_default`.
  - Soporta `minimum_width` y `minimum_height`.
  - Puede configurar `spacing` para filas y columnas.
  - Puede tener tamaños de columnas/filas no uniformes.
- **Uso ideal**: Para diseños tipo tabla, teclados, calculadoras, galerías de imágenes.

```kivy
GridLayout:
    cols: 2
    spacing: dp(5)
    Button:
        text: 'A'
    Button:
        text: 'B'
    Button:
        text: 'C'
    Button:
        text: 'D'
```

## AnchorLayout
- **Propósito principal**: Anclar widgets a una posición específica.
- **Características clave**:
  - Permite posicionar widgets en 9 posiciones (combinaciones de top/center/bottom y left/center/right).
  - Propiedades principales: `anchor_x` ('left', 'center', 'right') y `anchor_y` ('top', 'center', 'bottom').
  - Todos los widgets se anclan a la misma posición.
  - No gestiona tamaños, solo posiciones.
- **Uso ideal**: Para colocar un widget en una esquina o centro de la pantalla.

```kivy
AnchorLayout:
    anchor_x: 'center'
    anchor_y: 'top'
    Button:
        text: 'Centrado arriba'
        size_hint: None, None
        size: dp(200), dp(50)
```

## FloatLayout
- **Propósito principal**: Posicionar widgets usando coordenadas relativas.
- **Características clave**:
  - Los widgets "flotan" en posiciones relativas dentro del layout.
  - Usa `pos_hint` para definir la posición relativa (valores de 0 a 1).
  - Extremadamente flexible pero puede ser más difícil de manejar.
  - Los widgets pueden superponerse.
- **Uso ideal**: Para interfaces donde la posición exacta es importante, o para diseños complejos.

```kivy
FloatLayout:
    Button:
        text: 'Centro'
        size_hint: .2, .1
        pos_hint: {'center_x': .5, 'center_y': .5}
    Button:
        text: 'Esquina'
        size_hint: .2, .1
        pos_hint: {'right': 1, 'top': 1}
```

## RelativeLayout
- **Propósito principal**: Similar a FloatLayout, pero las posiciones son relativas al layout, no a la ventana.
- **Características clave**:
  - Cuando el layout se mueve, todos sus hijos se mueven con él.
  - El punto (0,0) es la esquina inferior izquierda del layout.
  - Ideal para componentes que necesitan moverse juntos.
- **Uso ideal**: Para crear componentes UI móviles o grupos de widgets que deben moverse juntos.

```kivy
RelativeLayout:
    pos: dp(100), dp(100)
    Button:
        text: 'Relativo al layout'
        size_hint: None, None
        size: dp(200), dp(50)
        pos: dp(10), dp(10)  # 10dp desde la esquina inferior izquierda del layout
```

## StackLayout
- **Propósito principal**: Colocar elementos uno tras otro, con ajuste automático cuando se acaba el espacio.
- **Características clave**:
  - Similar a BoxLayout pero con ajuste automático (wrapping).
  - Útil para contenido de longitud variable.
  - Propiedades: `orientation` y `padding`.
  - El ajuste ocurre cuando los widgets no caben en la dirección principal.
- **Uso ideal**: Para colecciones de elementos de tamaño similar que deben ajustarse, como galerías de fotos o tags.

```kivy
StackLayout:
    orientation: 'lr-tb'  # left-to-right, top-to-bottom
    spacing: dp(5)
    # Los elementos se colocarán de izquierda a derecha y luego
    # pasarán a la siguiente fila cuando se acabe el espacio
    Button:
        text: '1'
        size_hint: None, None
        size: dp(100), dp(50)
    # Más botones...
```

## PageLayout
- **Propósito principal**: Crear un efecto de "libro" o páginas deslizables.
- **Características clave**:
  - Cada widget hijo se convierte en una página distinta.
  - Permite deslizar horizontalmente entre páginas.
  - Soporta efecto de página con sombra y doblado.
- **Uso ideal**: Para tutoriales, wizards, visualizadores de documentos.

```kivy
PageLayout:
    Button:
        text: 'Página 1'
    Button:
        text: 'Página 2'
    Button:
        text: 'Página 3'
```

## ScatterLayout
- **Propósito principal**: Permitir transformaciones multitouch (rotar, escalar, mover).
- **Características clave**:
  - Hereda de Scatter y Layout.
  - Los widgets hijos pueden ser manipulados con gestos táctiles.
  - Soporta transformaciones 2D (rotación, escala, translación).
- **Uso ideal**: Para interfaces que requieren manipulación directa como visores de fotos, mapas, etc.

```kivy
ScatterLayout:
    Button:
        text: 'Puedes moverme, rotarme y escalarme'
        size_hint: None, None
        size: dp(200), dp(100)
```

## Tabla Comparativa de Layouts

| Layout | Propósito | Fortaleza | Debilidad |
|--------|-----------|-----------|-----------|
| BoxLayout | Organización secuencial | Simple, predecible | Limitado a una dimensión |
| GridLayout | Estructura tipo tabla | Ordenado, simétrico | Menos flexible para widgets de diferentes tamaños |
| AnchorLayout | Posicionamiento fijo | Simple para alineaciones básicas | Sólo 9 posiciones posibles |
| FloatLayout | Posicionamiento libre | Muy flexible | Puede ser complejo de manejar |
| RelativeLayout | Grupo móvil | Bueno para componentes compuestos | Similar a FloatLayout |
| StackLayout | Contenido con ajuste automático | Bueno para colecciones | Menos control sobre posicionamiento |
| PageLayout | Navegación tipo libro | Intuitivo para secuencias | Limitado a transición horizontal |
| ScatterLayout | Manipulación multitáctil | Interactivo | Mayor complejidad |
