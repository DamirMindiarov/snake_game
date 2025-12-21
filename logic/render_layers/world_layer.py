from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window

class WorldRenderLayer:
    def _draw_obstacles(self, zoom):
        with self.canvas:
            Color(0.4, 0.4, 0.4, 1)
            step = self.tile_size
            chunk_px = self.chunk_size * step
            vw, vh = (Window.width / zoom) / 2 + step, (Window.height / zoom) / 2 + step
            ccx, ccy = int(self.world_x // chunk_px), int(self.world_y // chunk_px)

            for cx in range(ccx - 1, ccx + 2):
                for cy in range(ccy - 1, ccy + 2):
                    if (cx, cy) in self.obstacles:
                        for tx, ty in self.obstacles[(cx, cy)]:
                            ox, oy = tx * step, ty * step
                            if abs(ox - self.world_x) < vw and abs(oy - self.world_y) < vh:
                                Rectangle(pos=(ox + 1, oy + 1), size=(step - 2, step - 2))
