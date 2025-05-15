from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from src.screens.inicio.TopBar.TopBar import TopBar
from src.screens.inicio.JuegoSeccion.JuegoSeccion import JuegoSeccion
from src.screens.inicio.BottomBar.BottomBar import BottomBar
from kivy.properties import StringProperty, ObjectProperty

Builder.load_file('src/screens/inicio/Inicio.kv')

class InicioScreen(Screen):
    pass