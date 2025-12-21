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

            # --- ВСЁ, ЧТО НИЖЕ, ПРИВЯЗАНО К МИРУ ---
            self._draw_grid(zoom)  # Слой 1: Сетка
            self._draw_obstacles(zoom)  # Слой 2: Камни
            self._draw_snake(t)  # Слой 3: Змея (голова и хвост)


            PopMatrix()

    def _draw_obstacles(self, zoom):
        step = self.tile_size  # Должно быть 60
        chunk_px = self.chunk_size * step  # Должно быть 20 * 60 = 1200

        # Текущий чанк (целые числа)
        ccx = int(self.world_x // chunk_px)
        ccy = int(self.world_y // chunk_px)

        # Перебираем 9 чанков вокруг
        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.obstacles:
                    Color(0.4, 0.4, 0.4, 1)  # Серый цвет
                    for tx, ty in self.obstacles[(cx, cy)]:
                        # ВАЖНО: Координаты Rectangle должны быть мировыми!
                        # Если tx=5, а step=60, то pos_x = 300
                        pos_x = tx * step
                        pos_y = ty * step

                        Rectangle(pos=(pos_x + 1, pos_y + 1),
                                  size=(step - 2, step - 2))

    def _draw_grid(self, zoom):
        step = self.tile_size  # Убедись, что это 60
        # Цвет: очень тусклый зеленый, чтобы не рябило
        Color(0.2, 0.3, 0.2, 0.4)

        # 1. Считаем, сколько мира видно в камеру (в пикселях)
        vw = (Window.width / zoom) / 2 + step
        vh = (Window.height / zoom) / 2 + step

        # 2. Находим ближайшие к краям экрана линии сетки
        start_x = int((self.world_x - vw) // step) * step
        end_x = int((self.world_x + vw) // step) * step
        start_y = int((self.world_y - vh) // step) * step
        end_y = int((self.world_y + vh) // step) * step

        # 3. Рисуем вертикальные линии
        for x in range(start_x, end_x + step, step):
            Line(points=[x, start_y, x, end_y], width=1)

        # 4. Рисуем горизонтальные линии
        for y in range(start_y, end_y + step, step):
            Line(points=[start_x, y, end_x, y], width=1)

    def _draw_snake(self, t):
        # ОТРИСОВКА ХВОСТА
        if hasattr(self, 'segments'):
            for i, seg in enumerate(self.segments):
                size = 28 - (i * 0.4)
                # Цвет затухает к хвосту
                Color(0.2, 0.8, 0.5, 1 - (i / len(self.segments)) * 0.6)
                Ellipse(pos=(seg[0] - size / 2, seg[1] - size / 2), size=(size, size))

        # ОТРИСОВКА ГОЛОВЫ
        # Добавим легкое "дыхание" голове через math.sin
        h_size = 38 + math.sin(t * 3) * 2
        Color(1, 0.6, 0, 1)
        Ellipse(pos=(self.world_x - h_size / 2, self.world_y - h_size / 2), size=(h_size, h_size))

