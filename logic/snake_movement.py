# logic/snake_movement.py
from collections import deque


class SnakeMovementMixin:
    def init_snake_data(self):
        self.num_segments = 30
        self.history_step = 5
        # Очередь на C — работает мгновенно O(1)
        # Заполняем сразу, чтобы не было пустых индексов
        self.history = deque([[0.0, 0.0]] * (self.num_segments * self.history_step + 1),
                             maxlen=1000)
        self.segments = [[0.0, 0.0] for _ in range(self.num_segments)]

    def move_tail(self):
        # appendleft в deque в десятки раз быстрее, чем list.insert(0)
        self.history.appendleft([self.world_x, self.world_y])

        for i in range(self.num_segments):
            # Доступ по индексу в deque в Python 3.12+ очень быстрый
            idx = (i + 1) * self.history_step
            if idx < len(self.history):
                # Обновляем координаты сегментов
                self.segments[i][0] = self.history[idx][0]
                self.segments[i][1] = self.history[idx][1]
