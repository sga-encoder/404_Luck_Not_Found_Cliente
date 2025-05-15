# from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.graphics import RenderContext, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import os
import sys
from src.utils.utils import leer_archivo

glassmorphism_shader = leer_archivo('glassmorphism.glsl')

class GlassmorphismWidget(Widget):
    # Propiedades ajustables desde Python o KV
    blur_radius = NumericProperty(5.0)
    opacity = NumericProperty(0.7)
    tint_color = ListProperty([0.9, 0.95, 1.0, 0.15])  # RGBA: Azul claro con transparencia
    time = NumericProperty(0)

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.fs = glassmorphism_shader
        super(GlassmorphismWidget, self).__init__(**kwargs)
        
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)
            
        self.bind(pos=self._update_rect, size=self._update_rect)
        Clock.schedule_interval(self._update_glsl, 1/60.)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def _update_glsl(self, *args):
        self.time += 0.01
        self.canvas['time'] = self.time
        self.canvas['resolution'] = [float(Window.width), float(Window.height)]
        self.canvas['blur_radius'] = self.blur_radius
        self.canvas['opacity'] = self.opacity
        # Convertir ListProperty a lista normal para que GLSL pueda manejarla
        self.canvas['tint_color'] = list(self.tint_color)
        self.canvas.ask_update()