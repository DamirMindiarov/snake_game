import math

from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from logic.core.interfaces import IGameSystem


class SnakeSystem(IGameSystem):
    def on_init(self):
        # Параметры физики
        self.game.vel_x = 0.0
        self.game.vel_y = 0.0
        self.max_v = 9.0
        self.accel = 0.4
        self.friction = 0.95

        # ПАРАМЕТРЫ ТЕЛА (Flat Array)
        self.game.num_segments = 25
        self.seg_dist = 18.0

        # Храним координаты как [x0, y0, x1, y1, x2, y2 ...]
        # Это один непрерывный блок памяти. Никаких вложенных списков.
        self.game.snake_data = [0.0] * (self.game.num_segments * 2)

        # Инициализируем стартовой позицией
        sx, sy = float(self.game.world_x), float(self.game.world_y)
        for i in range(self.game.num_segments):
            self.game.snake_data[i * 2] = sx
            self.game.snake_data[i * 2 + 1] = sy

    def on_update(self, dt):
        # 1. ОБРАБОТКА ВВОДА (Input Phase)
        # Переносим логику из GameLoop сюда, чтобы змея знала, куда ползти
        if self.game.is_touching:
            zoom = getattr(self.game, 'camera_zoom', 1.0)

            # Центрируем экранные координаты относительно центра окна
            rel_x = self.game.touch_screen_pos[0] - Window.width / 2
            rel_y = self.game.touch_screen_pos[1] - Window.height / 2

            # Устанавливаем цель в мировых координатах
            self.game.target_x = self.game.world_x + (rel_x / zoom)
            self.game.target_y = self.game.world_y + (rel_y / zoom)

        # 2. ФИЗИКА (Inertia Phase)
        if self.game.is_touching:
            dx = self.game.target_x - self.game.world_x
            dy = self.game.target_y - self.game.world_y
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > 5:
                self.game.vel_x += (dx / dist) * self.accel
                self.game.vel_y += (dy / dist) * self.accel

        # Адаптивное трение
        v_sq = self.game.vel_x ** 2 + self.game.vel_y ** 2
        current_friction = 0.85 if v_sq > 100 else self.friction
        self.game.vel_x *= current_friction
        self.game.vel_y *= current_friction

        # Ограничение скорости
        v_current = math.sqrt(v_sq)
        if v_current > self.max_v:
            scale = self.max_v / v_current
            self.game.vel_x *= scale
            self.game.vel_y *= scale

        # 2. КОЛЛИЗИИ СО СКОЛЬЖЕНИЕМ (Бывший CollisionMixin)
        self._apply_movement_with_collisions(self.game.vel_x, self.game.vel_y)

        # 3. ХВОСТ (Бывший SnakeMovementMixin - Векторная модель)
        self._update_tail()

    def on_render(self, canvas, t, zoom):
        """Отрисовка из плоского массива"""
        # Рисуем с конца к началу
        for i in range(self.game.num_segments - 1, -1, -1):
            idx = i * 2
            x = self.game.snake_data[idx]
            y = self.game.snake_data[idx + 1]

            size = 30 - (i * 0.4)
            if i == 0:  # Голова
                Color(1, 0.6, 0, 1) if self.game.damage_timer <= 0 else Color(1, 0, 0, 1)
                size = 40
            else:  # Тело
                Color(0.2, 0.8, 0.5, 1)

            Ellipse(pos=(x - size / 2, y - size / 2), size=(size, size))

    def _apply_movement_with_collisions(self, vx, vy):
        world = getattr(self.game, 'world', None)
        interact = getattr(self.game, 'interaction', None)
        if not world: return

        ts = self.game.tile_size

        # --- Проверка по X ---
        future_x = self.game.world_x + vx
        if not world.is_tile_solid(future_x, self.game.world_y):
            self.game.world_x = future_x
        else:
            # Если уперлись в стену по X — пробуем толкнуть
            tx = int((future_x + (ts / 2 if vx > 0 else -ts / 2)) // ts)
            ty = int(self.game.world_y // ts)

            direction = [1 if vx > 0 else -1, 0]

            # Если InteractionSystem смогла толкнуть блок
            if interact and interact.push_block(tx, ty, direction):
                # Разрешаем змее немного продвинуться, пока камень отлетает
                self.game.world_x += vx * 0.3
            else:
                self.game.vel_x = 0
                self.game.damage_timer = 0.5

        # --- Проверка по Y ---
        future_y = self.game.world_y + vy
        if not world.is_tile_solid(self.game.world_x, future_y):
            self.game.world_y = future_y
        else:
            # Если уперлись в стену по Y — пробуем толкнуть
            tx = int(self.game.world_x // ts)
            ty = int((future_y + (ts / 2 if vy > 0 else -ts / 2)) // ts)

            direction = [0, 1 if vy > 0 else -1]

            if interact and interact.push_block(tx, ty, direction):
                self.game.world_y += vy * 0.3
            else:
                self.game.vel_y = 0
                self.game.damage_timer = 0.5

    def _update_tail(self):
        # Важно: используем snake_data[0] и [1] для головы
        self.game.snake_data[0] = float(self.game.world_x)
        self.game.snake_data[1] = float(self.game.world_y)

        for i in range(1, self.game.num_segments):
            idx = i * 2
            prev_idx = (i - 1) * 2

            lx, ly = self.game.snake_data[prev_idx], self.game.snake_data[prev_idx + 1]
            sx, sy = self.game.snake_data[idx], self.game.snake_data[idx + 1]

            dx = lx - sx
            dy = ly - sy
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > self.seg_dist:
                move_dist = dist - self.seg_dist
                self.game.snake_data[idx] += (dx / dist) * move_dist
                self.game.snake_data[idx + 1] += (dy / dist) * move_dist
