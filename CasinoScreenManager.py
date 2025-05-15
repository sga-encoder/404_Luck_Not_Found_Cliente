from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from src.screens.inicio.Inicio import InicioScreen
from src.screens.portada.Portada import PortadaScreen

# Crear el administrador de pantallas
class CasinoScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        Window.size = (1280, 832)
        # Centrar la ventana en la pantalla
        screen_width, screen_height = Window.system_size
        Window.left = (screen_width - Window.size[0]) // 2
        Window.top = (screen_height - Window.size[1]) // 2
        # Cargar los archivos kv en orden correcto
        Builder.load_file('src/CasinoScreenManager.kv')
        return CasinoScreenManager()
    
class MyAppDev(App):
    def build(self):
        Window.size = (1280, 832)
        
        # Centrar la ventana en la pantalla
        screen_width, screen_height = Window.system_size
        Window.left = (screen_width - Window.size[0]) // 2
        Window.top = (screen_height - Window.size[1]) // 2
        # Cargar el archivo kv de la pantalla específica
        Builder.load_string('''
<CasinoScreenManager>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'src/assets/imagen/fondo.jpg'
    InicioScreen:
        name: 'inicio'
        ''')
        return CasinoScreenManager()

if __name__ == '__main__':
    MyApp().run()
    # MyAppDev().run()
