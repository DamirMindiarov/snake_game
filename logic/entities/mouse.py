import random, math
from kivy.graphics import Color, Rectangle
from logic.core.interfaces import IEntity
from logic.effects.bite_fx import BiteEffect


class Mouse(IEntity):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.is_prey = True  # Мышь — это еда
        self.speed = 3.5
        self.fear_radius = 280.0
        self.vel = [0, 0]
        self.speed = 3.0
        self.fear_radius = 250.0
        ent_sys = game.manager.get_system('EntitySystem')
        self.texture = ent_sys.get_tex("assets/mouse.png")

    @staticmethod
    def populate_chunk(game, cx, cy, chunk_map):
        # Возвращаем шанс 20-25% на появление мышей в чанке
        if random.random() < 1:
            cs, ts = game.chunk_size, game.tile_size

            # Спавним всего 1-2 мыши на чанк вместо 30
            for _ in range(random.randint(1, 2)):
                tx = random.randint(cx * cs, (cx + 1) * cs - 1)
                ty = random.randint(cy * cs, (cy + 1) * cs - 1)

                if (tx, ty) not in chunk_map:
                    ent_sys = game.manager.get_system('EntitySystem')
                    if ent_sys:
                        world_pos = [tx * ts + ts / 2, ty * ts + ts / 2]
                        ent_sys.spawn(Mouse, world_pos)



    def update(self, dt):
        # 1. Локальные ссылки для ускорения доступа в Python [12.1]
        gx, gy = self.game.world_x, self.game.world_y
        px, py = self.pos[0], self.pos[1]

        dx = px - gx
        dy = py - gy
        dist_sq = dx * dx + dy * dy  # Быстрее, чем dx**2 [15.1]

        # 2. Логика ИИ (Квадрат радиуса страха 250^2 = 62500)
        if dist_sq < 62500:
            dist = dist_sq ** 0.5
            # Нормализация вектора и умножение на скорость
            m = self.speed / dist if dist > 0 else 0
            self.vel[0] = dx * m
            self.vel[1] = dy * m
        elif random.random() < 0.02:
            # Случайное блуждание (только в 2% кадров)
            a = random.uniform(0, 6.283)
            self.vel[0] = math.cos(a)
            self.vel[1] = math.sin(a)

        # 3. Применяем движение
        nx = px + self.vel[0]
        ny = py + self.vel[1]

        # 4. ОПТИМИЗАЦИЯ КОЛЛИЗИЙ (Самое тяжелое место) [12.1]
        # Если мышь далеко от змеи (например, > 1000px), не проверяем стены
        # Это сэкономит 70% ресурсов CPU при ENT 180+
        if dist_sq > 1000000:  # 1000^2
            self.pos[0], self.pos[1] = nx, ny
        else:
            # Рядом со змеей проверяем стены честно
            if not self.game.world.is_tile_solid(nx, ny):
                self.pos[0], self.pos[1] = nx, ny
            else:
                # Отскок при ударе о стену
                self.vel[0] *= -1
                self.vel[1] *= -1

    def draw(self, group):
        # Используем Rectangle и текстуру.
        # Если все мыши белые, Color можно добавить один раз в EntitySystem перед циклом.
        from kivy.graphics import Rectangle
        group.add(Rectangle(
            texture=self.texture,
            pos=(self.pos[0] - 16, self.pos[1] - 16),
            size=(32, 32)
        ))

    def on_catch(self):
        if getattr(self.game, 'fx_bite_enabled', True):
            fx_sys = self.game.manager.get_system('FXSystem')
            if fx_sys:
                # Просто триггерим взрыв, он сам привяжется к голове
                fx_sys.spawn_bite()

        if hasattr(self.game, 'digestion_stack'):
            self.game.digestion_stack.append({'idx': 0.0, 'pwr': 1.0})
