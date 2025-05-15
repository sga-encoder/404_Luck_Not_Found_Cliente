from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_file('src/screens/inicio/TopBar/Saldo.kv')
Builder.load_file('src/screens/inicio/TopBar/UserInicio.kv')
Builder.load_file('src/screens/inicio/TopBar/UserImage.kv')
Builder.load_file('src/screens/inicio/TopBar/TopBar.kv')

class Saldo(AnchorLayout):
    pass

class UserInicio(AnchorLayout):
    pass

class UserImage(Image):
    pass

class TopBar(AnchorLayout):
    pass