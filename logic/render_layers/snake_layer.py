import math
from kivy.graphics import Color, Ellipse

class SnakeRenderLayer:
    def _draw_snake(self, t):
        with self.canvas:
            if hasattr(self, 'segments'):
                for i, seg in enumerate(self.segments):
                    size = 28 - (i * 0.4)
                    Color(0.2, 0.8, 0.5, 1 - (i / len(self.segments)) * 0.6)
                    Ellipse(pos=(seg[0] - size/2, seg[1] - size/2), size=(size, size))

            h_size = 38 + math.sin(t * 3) * 2
            # В методе _draw_snake
            h_color = (1, 0, 0, 1) if getattr(self, 'damage_timer', 0) > 0 else (1, 0.6, 0, 1)
            Color(*h_color)
            Ellipse(pos=(self.world_x - h_size / 2, self.world_y - h_size / 2), size=(h_size, h_size))

