# logic/render_layers/snake_layer.py
from kivy.graphics import Color, Ellipse


class SnakeRenderLayer:
    # logic/render_layers/snake_layer.py
    def _draw_snake(self, t):
        if not hasattr(self, 'segments'): return

        # Рисуем хвост (с конца, чтобы голова была сверху)
        for i in range(len(self.segments) - 1, -1, -1):
            s = self.segments[i]
            # Размер (30) больше дистанции (18) — это дает плотное тело без щелей
            size = 30 - (i * 0.4)
            Color(0.2, 0.8, 0.5, 1)
            Ellipse(pos=(s[0] - size / 2, s[1] - size / 2), size=(size, size))

        # Голова
        Color(1, 0.6, 0, 1) if getattr(self, 'damage_timer', 0) <= 0 else Color(1, 0, 0, 1)
        Ellipse(pos=(self.world_x - 20, self.world_y - 20), size=(40, 40))

