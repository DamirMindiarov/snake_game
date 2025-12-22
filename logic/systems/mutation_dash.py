# logic/systems/mutation_dash.py
import time
import math
from logic.core.mutations import IMutationSystem


class MutationDashSystem(IMutationSystem):
    @property
    def mutation_id(self): return "dash"

    def on_init(self):
        """Реализация обязательного метода интерфейса"""
        self.last_click_time = 0
        self.dash_power = 20.0
        self.game.dash_timer = 0.0
        self.dash_direction = [0, 0]

    def on_touch_down(self, touch):
        if not self.is_active(): return  # Используем встроенную проверку


        curr_time = time.time()
        # Двойной клик
        if curr_time - self.last_click_time < 0.3:
            self._activate_dash()
        self.last_click_time = curr_time

    def _activate_dash(self):
        # Считаем направление рывка
        dx = self.game.target_x - self.game.world_x
        dy = self.game.target_y - self.game.world_y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist > 1:
            self.dash_direction = [dx / dist, dy / dist]
            self.game.dash_timer = 0.3  # Длительность рывка в секундах
            # Обнуляем текущую скорость, чтобы рывок был чистым
            self.game.vel_x, self.game.vel_y = 0, 0
            print(f"ULTRA DASH: {self.dash_power}")

    def on_update(self, dt):
        if self.game.dash_timer > 0:
            self.game.dash_timer -= dt

            # 1. Рассчитываем мощный сдвиг
            move_x = self.dash_direction[0] * self.dash_power
            move_y = self.dash_direction[1] * self.dash_power

            # 2. Двигаем голову с проверкой коллизий
            if hasattr(self.game.world, 'is_tile_solid'):
                if not self.game.world.is_tile_solid(self.game.world_x + move_x, self.game.world_y):
                    self.game.world_x += move_x
                if not self.game.world.is_tile_solid(self.game.world_x, self.game.world_y + move_y):
                    self.game.world_y += move_y
            else:
                self.game.world_x += move_x
                self.game.world_y += move_y

            # 3. КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Синхронизируем хвост
            # Находим систему змеи в списке систем менеджера
            snake_sys = getattr(self.game, 'snake', None)
            if snake_sys and hasattr(snake_sys, '_update_tail'):
                # Принудительно заставляем хвост "подтянуться" к новым координатам головы
                # Прямо в этом же кадре!
                snake_sys._update_tail()

    def on_render(self, canvas, t, zoom):
        pass
