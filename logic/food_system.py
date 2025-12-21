# logic/food_system.py
import random

from kivy.graphics import Color, Ellipse


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

    def check_food_snapping(self):
        if not self.food_items: return

        chunk_px = self.chunk_size * self.tile_size
        ccx, ccy = int(self.world_x // chunk_px), int(self.world_y // chunk_px)

        # Дистанция броска
        is_mutated = self.mutations.get("predatory_snap", False)
        snap_dist = 120 if is_mutated else 35

        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.food_items:
                    for food in self.food_items[(cx, cy)][:]:
                        dx = food["x"] - self.world_x
                        dy = food["y"] - self.world_y
                        dist_sq = dx ** 2 + dy ** 2

                        if dist_sq < snap_dist ** 2:
                            # ЕСЛИ МУТАЦИЯ — ДЕЛАЕМ РЫВОК
                            if is_mutated:
                                dist = dist_sq ** 0.5
                                if dist > 1:
                                    # Придаем огромную скорость в сторону еды
                                    snap_power = 40.0
                                    self.vel_x = (dx / dist) * snap_power
                                    self.vel_y = (dy / dist) * snap_power

                            # Условие поедания (вплотную)
                            if dist_sq < 30 ** 2:
                                self.food_items[(cx, cy)].remove(food)
                                self.biomass_points += 1
                                self.eat_timer = 0.3
                                self._refresh_food_chunk_graphics(cx, cy)
                                return True
        return False


    def _refresh_food_chunk_graphics(self, cx, cy):
        """Перерисовка запеченной графики еды"""
        # В нашей структуре Step 11 графика лежит в self.obstacles
        if (cx, cy) in self.obstacles:
            group = self.obstacles[(cx, cy)].get("food_graphics")
            if group:
                group.clear()
                group.add(Color(0, 0.8, 1, 0.8))
                for food in self.food_items.get((cx, cy), []):
                    group.add(Ellipse(pos=(food["x"] - 8, food["y"] - 8), size=(16, 16)))
