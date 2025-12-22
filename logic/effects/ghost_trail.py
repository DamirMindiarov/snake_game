# logic/effects/ghost_trail.py
from kivy.graphics import Color, Ellipse, InstructionGroup
import time


class GhostTrailEffect:
    def __init__(self, flat_data, color=(0, 0.8, 1)):
        self.start_time = time.time()
        self.lifetime = 0.3
        self.alive = True
        self.alpha = 0.4

        # 1. Создаем графический контейнер
        self.group = InstructionGroup()
        self.color_instr = Color(*color, self.alpha)
        self.group.add(self.color_instr)

        # 2. Итерируемся по плоскому массиву [x0, y0, x1, y1...]
        # Шаг 2, так как на каждый сегмент приходится два числа
        for i in range(0, len(flat_data), 2):
            x = flat_data[i]
            y = flat_data[i + 1]

            # Рассчитываем размер (i // 2, чтобы получить индекс сегмента)
            segment_idx = i // 2
            size = 28 - (segment_idx * 1.5)

            if size > 1:
                # Используем x и y напрямую (без индексов [0] и [1])
                self.group.add(Ellipse(
                    pos=(x - size / 2, y - size / 2),
                    size=(size, size)
                ))

    def update(self, dt):
        elapsed = time.time() - self.start_time
        if elapsed > self.lifetime:
            self.alive = False
        else:
            # Плавно гасим альфу
            self.alpha = (1.0 - (elapsed / self.lifetime)) * 0.4
            self.color_instr.a = self.alpha

    def draw(self, canvas):
        if self.alive:
            canvas.add(self.group)

    @property
    def is_alive(self):
        return self.alive
