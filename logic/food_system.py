# logic/food_system.py
import random


class FoodSystemMixin:
    def init_food(self):
        # {(cx, cy): [ {"x": 100, "y": 100}, ... ]}
        self.food_items = {}
        self.biomass_points = 0
        self.eat_timer = 0.0

    def spawn_food_in_chunk(self, cx, cy):
        """Возвращает список координат еды для запекания в чанк"""
        chunk_px = self.chunk_size * self.tile_size
        food_list = []
        for _ in range(random.randint(3, 6)):
            fx = random.randint(cx * chunk_px, (cx + 1) * chunk_px)
            fy = random.randint(cy * chunk_px, (cy + 1) * chunk_px)
            if not self.is_tile_solid(fx, fy):
                food_list.append({"x": fx, "y": fy})

        self.food_items[(cx, cy)] = food_list
        return food_list
