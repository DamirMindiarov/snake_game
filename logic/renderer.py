# logic/renderer.py
import math
import time
from kivy.graphics import Color, Ellipse, Rectangle, PushMatrix, PopMatrix, Translate, Scale, Line
from kivy.core.window import Window


# logic/renderer.py
class GameRendererMixin:
    def draw_canvas(self):
        self.canvas.clear()
        t = time.time()
        zoom = getattr(self, 'camera_zoom', 1.0)

        with self.canvas:
            # 1. СТАТИЧНЫЙ ФОН (не двигается)
            Color(0.1, 0.15, 0.1, 1)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))

            PushMatrix()
            # 2. КАМЕРА (Центрирует змею)
            Translate(Window.width / 2, Window.height / 2, 0)
            Scale(zoom, zoom, 1)
            Translate(-self.world_x, -self.world_y, 0)

            # 3. СЕТКА (статичная в мире)
            Color(0.2, 0.3, 0.2, 1)
            step = 100  # Размер клетки

            # Рисуем сетку от -2000 до 2000 пикселей мира
            for x in range(-2000, 2001, step):
                Line(points=[x, -2000, x, 2000], width=1)
            for y in range(-2000, 2001, step):
                Line(points=[-2000, y, 2000, y], width=1)

            # 4. ГОЛОВА ЗМЕИ
            Color(1, 0.6, 0, 1)
            Ellipse(pos=(self.world_x - 20, self.world_y - 20), size=(40, 40))

            PopMatrix()

