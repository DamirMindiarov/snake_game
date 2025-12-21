from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window

class WorldRenderLayer:
    def _draw_obstacles(self, zoom):
        chunk_px = self.chunk_size * self.tile_size
        ccx = int(self.world_x // chunk_px)
        ccy = int(self.world_y // chunk_px)

        # Мы просто добавляем группу инструкций чанка на холст.
        # Kivy сам поймет, что их нужно отрисовать.
        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.obstacles:
                    # Добавляем графический пакет чанка в текущий контекст отрисовки
                    self.canvas.add(self.obstacles[(cx, cy)]["graphics"])
