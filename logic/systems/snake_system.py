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

        # Параметры тела
        self.game.num_segments = 25
        self.seg_dist = 18.0
        # Инициализируем сегменты мировыми координатами головы
        self.game.segments = [[self.game.world_x, self.game.world_y] for _ in range(self.game.num_segments)]

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
        # Хвост (SnakeRenderLayer)
        for i in range(len(self.game.segments) - 1, -1, -1):
            s = self.game.segments[i]
            size = 30 - (i * 0.4)
            Color(0.2, 0.8, 0.5, 1)
            Ellipse(pos=(s[0] - size / 2, s[1] - size / 2), size=(size, size))

        # Голова
        h_size = 40
        Color(1, 0, 0, 1) if self.game.damage_timer > 0 else Color(1, 0.6, 0, 1)
        Ellipse(pos=(self.game.world_x - 20, self.game.world_y - 20), size=(h_size, h_size))

    def _apply_movement_with_collisions(self, vx, vy):
        # Обращаемся к WorldSystem через основной класс игры
        world = getattr(self.game, 'world', None)
        if not world: return

        # Проверка по X
        if not world.is_tile_solid(self.game.world_x + vx, self.game.world_y):
            self.game.world_x += vx
        else:
            self.game.vel_x = 0
            self.game.damage_timer = 0.5

        # Проверка по Y
        if not world.is_tile_solid(self.game.world_x, self.game.world_y + vy):
            self.game.world_y += vy
        else:
            self.game.vel_y = 0
            self.game.damage_timer = 0.5

    def _update_tail(self):
        leader_x, leader_y = float(self.game.world_x), float(self.game.world_y)
        for i in range(self.game.num_segments):
            seg = self.game.segments[i]
            dx = leader_x - seg[0]
            dy = leader_y - seg[1]
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > self.seg_dist:
                move_dist = dist - self.seg_dist
                seg[0] += (dx / dist) * move_dist
                seg[1] += (dy / dist) * move_dist

            leader_x, leader_y = seg[0], seg[1]
