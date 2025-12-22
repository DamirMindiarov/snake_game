# logic/systems/mutation_dash.py
import time
import math
from kivy.core.window import Window
from logic.core.mutations import IMutationSystem
from logic.effects.ghost_trail import GhostTrailEffect


class MutationDashSystem(IMutationSystem):
    @property
    def mutation_id(self):
        return "dash"

    def on_init(self):
        self.last_click_time = 0
        self.dash_power = 30.0  # Сила рывка (настрой под себя)
        self.game.dash_timer = 0.0
        self.dash_direction = [0, 0]
        self.last_spawn_time = 0

    def on_touch_down(self, touch):
        if not self.is_active():
            return

        curr_time = time.time()
        # Детекция двойного клика
        if curr_time - self.last_click_time < 0.3:
            self._activate_dash(touch)

        self.last_click_time = curr_time

    def _activate_dash(self, touch):
        # 1. Расчет вектора ОТ ЦЕНТРА ЭКРАНА (где голова) к пальцу
        dx = touch.x - Window.width / 2
        dy = touch.y - Window.height / 2
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist > 10:
            self.dash_direction = [dx / dist, dy / dist]
            self.game.dash_timer = 0.25
            self.game.vel_x, self.game.vel_y = 0, 0

            # ИСПРАВЛЕНИЕ ТУТ:
            fx_sys = getattr(self.game, 'fx', None)
            # Проверяем наличие нового массива snake_data
            if fx_sys and hasattr(self.game, 'snake_data'):
                # Берем срез (плоский список координат)
                snapshot = self.game.snake_data[:20]
                fx_sys.spawn(GhostTrailEffect(snapshot))

    def on_update(self, dt):
        now = time.time()

        if self.game.dash_timer > 0:
            self.game.dash_timer -= dt

            # 1. Добавляем фантомов во время полета (раз в 0.06 сек)
            if now - self.last_spawn_time > 0.06:
                fx_sys = getattr(self.game, 'fx', None)
                if fx_sys and hasattr(self.game, 'segments'):
                    snapshot = [list(pos) for pos in self.game.segments[:8]]
                    fx_sys.spawn(GhostTrailEffect(snapshot))
                self.last_spawn_time = now

            # 2. Принудительное перемещение головы (игнорируя трение SnakeSystem)
            move_x = self.dash_direction[0] * self.dash_power
            move_y = self.dash_direction[1] * self.dash_power

            # 3. Проверка коллизий через WorldSystem
            world = getattr(self.game, 'world', None)
            if world:
                if not world.is_tile_solid(self.game.world_x + move_x, self.game.world_y):
                    self.game.world_x += move_x
                if not world.is_tile_solid(self.game.world_x, self.game.world_y + move_y):
                    self.game.world_y += move_y

            # СИНХРОНИЗАЦИЯ ХВОСТА
            snake_sys = getattr(self.game, 'snake', None)
            if snake_sys:
                # ВЫЗЫВАЕМ МЕТОД, КОТОРЫЙ ТЕПЕРЬ РАБОТАЕТ С ПЛОСКИМ МАССИВОМ
                snake_sys._update_tail()

    def on_render(self, canvas, t, zoom):
        pass
