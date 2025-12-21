import time
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate, Scale
from kivy.core.window import Window
from logic.render_layers.world_layer import WorldRenderLayer
from logic.render_layers.snake_layer import SnakeRenderLayer

# logic/renderer.py
class GameRendererMixin(WorldRenderLayer, SnakeRenderLayer):
    def draw_canvas(self):
        self.canvas.clear() # Очищаем главный холст
        t = time.time()
        zoom = getattr(self, 'camera_zoom', 0.6)

        # Рисуем фон (прямо здесь)
        with self.canvas:
            Color(0.18, 0.28, 0.18, 1)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))

        # Трансформации камеры
        # ВАЖНО: Матрица трансформаций (PushMatrix)
        # все равно должна быть в with self.canvas
        with self.canvas:
            PushMatrix()
            Translate(Window.width / 2, Window.height / 2, 0)
            Scale(zoom, zoom, 1)
            Translate(-self.world_x, -self.world_y, 0)

        # Вызываем слои (они сами зайдут в with self.canvas)
        self._draw_obstacles(zoom)
        self._draw_snake(t)

        with self.canvas:
            PopMatrix()

