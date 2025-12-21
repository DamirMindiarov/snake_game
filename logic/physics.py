# logic/physics.py

class SnakePhysicsMixin:
    def init_physics(self):
        self.vel_x = 0
        self.vel_y = 0
        self.max_v = 9  # Максимальная скорость
        self.accel = 0.4  # Ускорение
        self.friction = 0.95  # Трение (замедление)

    def apply_inertia(self):
        # СТРАХОВКА: если переменные еще не созданы, создаем их на лету
        if not hasattr(self, 'vel_x'):
            self.init_physics()
        # Если палец прижат, тянем змею к цели
        if getattr(self, 'is_touching', False):
            dx = self.target_x - self.world_x
            dy = self.target_y - self.world_y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist > 5:
                # Плавное ускорение в сторону цели
                self.vel_x += (dx / dist) * self.accel
                self.vel_y += (dy / dist) * self.accel

        # Применяем трение, чтобы не лететь вечно
        self.vel_x *= self.friction
        self.vel_y *= self.friction

        # Ограничение скорости
        v_current = (self.vel_x ** 2 + self.vel_y ** 2) ** 0.5
        if v_current > self.max_v:
            scale = self.max_v / v_current
            self.vel_x *= scale
            self.vel_y *= scale

        # Обновляем координаты мира
        self.world_x += self.vel_x
        self.world_y += self.vel_y
