
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy_garden.frostedglass import FrostedGlass


# Primero definimos las clases y luego cargamos los archivos kv
class JuegoSeccionItem(FrostedGlass):
    background_id = ObjectProperty(None)
    imagen = StringProperty()
    titulo = StringProperty()

class JuegoSeccion(FloatLayout):
    pass

# Cargamos los archivos kv después de definir las clases
Builder.load_file("src/screens/inicio/JuegoSeccion/JuegoSeccionItem.kv")
Builder.load_file("src/screens/inicio/JuegoSeccion/JuegoSeccion.kv")