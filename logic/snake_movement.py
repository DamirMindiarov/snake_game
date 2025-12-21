# logic/snake_movement.py

class SnakeMovementMixin:
    def init_snake_data(self):
        # Количество сегментов
        self.num_segments = 30
        # Создаем сегменты сразу в начальной точке
        self.segments = [[0.0, 0.0] for _ in range(self.num_segments)]
        # История: заполняем её сразу начальными точками, чтобы хвост не "висел"
        self.history = [[0.0, 0.0] for _ in range(500)]
        self.history_step = 5

    def move_tail(self):
        # 1. Записываем текущую позицию головы в историю
        # Важно: записываем всегда, даже если стоим, чтобы хвост не дергался
        self.history.insert(0, [self.world_x, self.world_y])

        # 2. Ограничиваем историю (с запасом)
        if len(self.history) > 600:
            self.history.pop()

        # 3. Прямая привязка сегментов к истории
        for i in range(self.num_segments):
            index = (i + 1) * self.history_step
            if index < len(self.history):
                # Обновляем координаты сегмента напрямую из истории
                self.segments[i][0] = self.history[index][0]
                self.segments[i][1] = self.history[index][1]
