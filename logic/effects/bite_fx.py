# logic/effects/bite_fx.py
import random
import math
from kivy.graphics import Color, Ellipse


class BiteEffect:
    def __init__(self, game, color=(0.9, 0.9, 0.9, 1)):
        self.game = game
        self.alive = True
        self.duration = 0.6  # Чуть дольше, чтобы глаз успел заметить
        self.elapsed = 0.0
        self.particles = []

        # Увеличиваем до 15-20 частиц для "густоты" [15.1]
        for _ in range(18):
            angle = random.uniform(0, 6.283)
            # Делаем разлет более резким (взрывным)
            speed = random.uniform(4, 12)
            self.particles.append({
                'p': [0.0, 0.0],
                'v': [math.cos(angle) * speed, math.sin(angle) * speed],
                # Увеличиваем размер (было 3-7, стало 6-12)
                's': random.uniform(6, 12)
            })
        self.color = color

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed > self.duration:
            self.alive = False
            return

        for p in self.particles:
            # Двигаем частицы
            p['p'][0] += p['v'][0]
            p['p'][1] += p['v'][1]

            # Трение воздуха (теперь затухание чуть слабее, чтобы летели дальше)
            p['v'][0] *= 0.93
            p['v'][1] *= 0.93

            # Частицы постепенно уменьшаются в размере к концу жизни [12.1]
            p['s'] *= 0.95

    @property
    def is_alive(self):
        return self.alive

    def draw(self, canvas):
        # Рассчитываем прозрачность
        alpha = 1.0 - (self.elapsed / self.duration)

        # Получаем актуальные координаты головы змеи ПРЯМО СЕЙЧАС
        hx, hy = self.game.world_x, self.game.world_y

        # Используем яркий цвет (почти белый), чтобы выделялся на фоне
        canvas.add(Color(self.color[0], self.color[1], self.color[2], alpha))

        for p in self.particles:
            # Рисуем частицы со смещением от текущего положения головы
            canvas.add(Ellipse(
                pos=(hx + p['p'][0] - p['s'] / 2,
                     hy + p['p'][1] - p['s'] / 2),
                size=(p['s'], p['s'])
            ))
