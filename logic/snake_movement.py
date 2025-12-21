# logic/snake_movement.py
import math


class SnakeMovementMixin:
    def init_snake_data(self):
        self.num_segments = 25
        self.seg_dist = 18.0  # Жесткая дистанция между звеньями

        sx, sy = getattr(self, 'world_x', 0.0), getattr(self, 'world_y', 0.0)
        # Нам больше не нужна огромная история, только позиции сегментов
        self.segments = [[sx, sy] for _ in range(self.num_segments)]

    def move_tail(self):
        # Первый сегмент следует за головой
        leader_x, leader_y = float(self.world_x), float(self.world_y)

        for i in range(self.num_segments):
            seg = self.segments[i]

            # Вектор от текущего сегмента к лидеру (голове или предыдущему сегменту)
            dx = leader_x - seg[0]
            dy = leader_y - seg[1]
            dist = math.sqrt(dx ** 2 + dy ** 2)

            if dist > self.seg_dist:
                # Вычисляем, насколько нужно подвинуть сегмент, чтобы он
                # сохранил дистанцию seg_dist до лидера
                move_dist = dist - self.seg_dist
                # Плавное перемещение вдоль вектора
                seg[0] += (dx / dist) * move_dist
                seg[1] += (dy / dist) * move_dist

            # Следующий сегмент будет следовать за текущим
            leader_x, leader_y = seg[0], seg[1]
