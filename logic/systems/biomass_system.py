import random
import math
from kivy.graphics import Color, Ellipse
from logic.core.interfaces import IGameSystem


class BiomassSystem(IGameSystem):
    def on_init(self):
        # Храним данные о еде в самой системе
        self.game.food_items = {}  # {(cx, cy): [{"x":, "y":}, ...]}
        self.food_color = (0, 0.8, 1, 0.8)  # Голубой неон
        self.snap_dist = 100  # Дистанция броска (мутация)
        self.eat_dist = 35  # Дистанция поедания

    def on_chunk_generated(self, cx, cy, chunk_data):
        """Слушаем событие от WorldSystem и наполняем чанк едой"""
        ts = self.game.tile_size
        cs = self.game.chunk_size
        chunk_px = cs * ts

        food_list = []
        # Наполняем графическую группу чанка, которую нам передал WorldSystem
        f_group = chunk_data["food_graphics"]
        f_group.add(Color(*self.food_color))

        for _ in range(random.randint(3, 6)):
            fx = random.randint(cx * chunk_px, (cx + 1) * chunk_px)
            fy = random.randint(cy * chunk_px, (cy + 1) * chunk_px)

            # Проверяем наложение на камни через WorldSystem
            if not self.game.world.is_tile_solid(fx, fy):
                food_list.append({"x": fx, "y": fy})
                f_group.add(Ellipse(pos=(fx - 8, fy - 8), size=(16, 16)))

        self.game.food_items[(cx, cy)] = food_list

    def on_update(self, dt):
        """Логика магнита и поедания (бывший FoodSystemMixin)"""
        if not self.game.food_items: return

        chunk_px = self.game.chunk_size * self.game.tile_size
        ccx = int(self.game.world_x // chunk_px)
        ccy = int(self.game.world_y // chunk_px)

        is_mutated = self.game.mutations.get("predatory_snap", False)
        current_snap = self.snap_dist if is_mutated else self.eat_dist

        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.game.food_items:
                    for food in self.game.food_items[(cx, cy)][:]:
                        dx = food["x"] - self.game.world_x
                        dy = food["y"] - self.game.world_y
                        dist_sq = dx ** 2 + dy ** 2

                        if dist_sq < current_snap ** 2:
                            # Эффект рывка
                            if is_mutated:
                                dist = dist_sq ** 0.5
                                if dist > 1:
                                    snap_power = 40.0
                                    self.game.vel_x = (dx / dist) * snap_power
                                    self.game.vel_y = (dy / dist) * snap_power

                            # Условие поедания
                            if dist_sq < self.eat_dist ** 2:
                                self.game.food_items[(cx, cy)].remove(food)
                                self.game.biomass_points += 1
                                self.game.damage_timer = -0.1  # Мини-вспышка (условно)
                                self._refresh_food_graphics(cx, cy)
                                return

    def on_render(self, canvas, t, zoom):
        """Отрисовка пакетов еды (аналогично камням)"""
        chunk_px = self.game.chunk_size * self.game.tile_size
        ccx = int(self.game.world_x // chunk_px)
        ccy = int(self.game.world_y // chunk_px)

        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.game.obstacles:
                    group = self.game.obstacles[(cx, cy)].get("food_graphics")
                    if group:
                        canvas.add(group)

    def _refresh_food_graphics(self, cx, cy):
        """Пересборка пакета графики чанка при поедании"""
        if (cx, cy) in self.game.obstacles:
            group = self.game.obstacles[(cx, cy)]["food_graphics"]
            group.clear()
            group.add(Color(*self.food_color))
            for food in self.game.food_items.get((cx, cy), []):
                group.add(Ellipse(pos=(food["x"] - 8, food["y"] - 8), size=(16, 16)))
