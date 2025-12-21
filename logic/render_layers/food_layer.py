# logic/render_layers/food_layer.py
class FoodRenderLayer:
    def _draw_food(self, zoom):
        chunk_px = self.chunk_size * self.tile_size
        ccx, ccy = int(self.world_x // chunk_px), int(self.world_y // chunk_px)

        # Отрисовка пакетов еды из 9 чанков
        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.obstacles:
                    group = self.obstacles[(cx, cy)].get("food_graphics")
                    if group:
                        self.canvas.add(group)
