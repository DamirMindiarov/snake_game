# logic/systems/mutation_snap.py
import math
from logic.core.mutations import IMutationSystem


class MutationSnapSystem(IMutationSystem):
    @property
    def mutation_id(self):
        return "predatory_snap"

    def on_init(self):
        # Настройки дистанции выпада
        self.snap_dist = 120.0
        self.eat_dist = 30.0

    def on_update(self, dt):
        # Если мутация не куплена — ничего не делаем
        if not self.is_active():
            return

        if not hasattr(self.game, 'food_items') or not self.game.food_items:
            return

        # Логика поиска ближайшей еды для прыжка
        chunk_px = self.game.chunk_size * self.game.tile_size
        ccx = int(self.game.world_x // chunk_px)
        ccy = int(self.game.world_y // chunk_px)

        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.game.food_items:
                    for food in self.game.food_items[(cx, cy)][:]:
                        dx = food["x"] - self.game.world_x
                        dy = food["y"] - self.game.world_y
                        dist_sq = dx ** 2 + dy ** 2

                        # Если еда в радиусе броска — придаем импульс (как мы делали раньше)
                        if dist_sq < self.snap_dist ** 2:
                            dist = math.sqrt(dist_sq)
                            if dist > 1:
                                snap_power = 40.0
                                self.game.vel_x = (dx / dist) * snap_power
                                self.game.vel_y = (dy / dist) * snap_power

                            # Условие поедания обрабатывается в BiomassSystem или здесь
                            # В модульной схеме лучше оставить физику броска тут,
                            # а факт "поедания" — в BiomassSystem для разделения ответственности.
                            return

    def on_render(self, canvas, t, zoom):
        pass  # Визуальные эффекты прыжка можно добавить сюда
