

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
        self.dash_power = 30.0
        self.game.dash_timer = 0.0
        self.dash_direction = [0, 0]
        self.last_spawn_time = 0

    def on_touch_down(self, touch):
        # Проверка: куплена ли мутация? (использует метод базового класса IMutationSystem) [17.1]
        if not self.is_active():
            return

        curr_time = time.time()
        # Детекция двойного клика
        if curr_time - self.last_click_time < 0.3:
            self._activate_dash(touch)

        self.last_click_time = curr_time

    def _activate_dash(self, touch):
        # 1. Расчет вектора ОТ ЦЕНТРА ЭКРАНА (где голова) к пальцу
        zoom = getattr(self.game, 'camera_zoom', 1.0)
        dx = (touch.x - Window.width / 2) / zoom
        dy = (touch.y - Window.height / 2) / zoom
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist > 10:
            self.dash_direction = [dx / dist, dy / dist]
            self.game.dash_timer = 0.25

            # Сбрасываем инерцию SnakeSystem для резкого старта
            self.game.vel_x, self.game.vel_y = 0, 0

            # СПАВН ПРИЗРАЧНОГО СЛЕДА (используем обновленный Flat Array) [12.1]
            fx_sys = self.game.manager.get_system('FXSystem')
            if fx_sys and hasattr(self.game, 'snake_data'):
                # Берем первые 20 элементов (10 сегментов) плоского массива
                snapshot = self.game.snake_data[:20]
                fx_sys.spawn(GhostTrailEffect(snapshot))

    def on_update(self, dt):
        if self.game.dash_timer > 0:
            self.game.dash_timer -= dt
            now = time.time()

            # 1. Создаем шлейф фантомов во время полета
            if now - self.last_spawn_time > 0.05:
                fx_sys = self.game.manager.get_system('FXSystem')
                if fx_sys and hasattr(self.game, 'snake_data'):
                    # Передаем копию текущего состояния хвоста
                    fx_sys.spawn(GhostTrailEffect(self.game.snake_data[:16]))
                self.last_spawn_time = now

            # 2. Перемещение головы (игнорируя физику SnakeSystem)
            move_x = self.dash_direction[0] * self.dash_power
            move_y = self.dash_direction[1] * self.dash_power

            # 3. Проверка коллизий через WorldSystem
            world = self.game.world
            if world:
                # Проверка по X и Y раздельно для скольжения вдоль стен [15.1]
                if not world.is_tile_solid(self.game.world_x + move_x, self.game.world_y):
                    self.game.world_x += move_x
                if not world.is_tile_solid(self.game.world_x, self.game.world_y + move_y):
                    self.game.world_y += move_y

            # 4. СИНХРОНИЗАЦИЯ ХВОСТА (Критично для Flat Data)
            snake_sys = self.game.manager.get_system('SnakeSystem')
            if snake_sys:
                snake_sys._update_tail()

    def on_render(self, canvas, t, zoom):
        pass

