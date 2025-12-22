# logic/systems/interaction_system.py
from kivy.graphics import Color, Rectangle
from logic.core.interfaces import IGameSystem
from logic.core.world_objects import WORLD_OBJECTS


class InteractionSystem(IGameSystem):
    def on_init(self):
        self.active_blocks = []  # [{"id": 1, "pos": [x,y], "target": [tx, ty], "speed": 5}]

    def push_block(self, tx, ty, direction):
        """Пытается толкнуть блок в указанном направлении [dx, dy]"""
        target_tx, target_ty = tx + direction[0], ty + direction[1]

        # 1. Сначала узнаем, КТО стоит в этой клетке
        cx, cy = tx // self.game.chunk_size, ty // self.game.chunk_size
        chunk_map = self.game.world_map.get((cx, cy), {})
        obj_id = chunk_map.get((tx, ty))

        # 2. ПРОВЕРКА: Если объекта нет или его НЕЛЬЗЯ толкать по конфигу (как дерево)
        if obj_id is None or not WORLD_OBJECTS.get(obj_id, {}).get("movable", False):
            return False

        # 3. Проверяем, свободна ли целевая клетка (куда толкаем)
        if not self.game.world.is_tile_solid(target_tx * self.game.tile_size, target_ty * self.game.tile_size):

            # 4. Проверка на хвост (чтобы не задвинуть камень в себя)
            if self._is_tail_at(target_tx, target_ty):
                return False

            # Вырезаем объект (он точно movable, мы проверили выше)
            removed_id = self.game.world.pop_object(tx, ty)
            if removed_id:
                # Получаем систему, которая владеет текстурой этого объекта
                # (Для камня это StoneSystem)
                tex = None
                if removed_id == 1:
                    tex = getattr(self.game.stones, 'stone_tex', None)

                self.active_blocks.append({
                    "id": removed_id,
                    "curr_pos": [tx * self.game.tile_size, ty * self.game.tile_size],
                    "target_tile": (target_tx, target_ty),
                    "texture": tex,  # Сохраняем текстуру вместо цвета
                })
                return True
        return False

    def _is_tail_at(self, tx, ty):
        # Простая проверка: нет ли сегментов змеи в радиусе тайла
        ts = self.game.tile_size
        for i in range(0, len(self.game.snake_data), 2):
            sx, sy = self.game.snake_data[i], self.game.snake_data[i + 1]
            if abs(sx - (tx * ts + ts / 2)) < ts / 2 and abs(sy - (ty * ts + ts / 2)) < ts / 2:
                return True
        return False

    def on_update(self, dt):
        ts = self.game.tile_size
        for b in self.active_blocks[:]:
            target_x = b["target_tile"][0] * ts
            target_y = b["target_tile"][1] * ts

            # Двигаем камень к цели
            dx = target_x - b["curr_pos"][0]
            dy = target_y - b["curr_pos"][1]
            dist = (dx ** 2 + dy ** 2) ** 0.5

            speed = 10  # Скорость полета камня
            if dist > speed:
                b["curr_pos"][0] += (dx / dist) * speed
                b["curr_pos"][1] += (dy / dist) * speed
            else:
                # Прибыл в точку: вмораживаем обратно
                self.game.world.place_object(b["target_tile"][0], b["target_tile"][1], b["id"])
                self.active_blocks.remove(b)

    def on_render(self, canvas, t, zoom):
        ts = self.game.tile_size
        for b in self.active_blocks:
            canvas.add(Color(1, 1, 1, 1)) # Сброс цвета для текстуры
            if b["texture"]:
                canvas.add(Rectangle(
                    texture=b["texture"],
                    pos=(b["curr_pos"][0], b["curr_pos"][1]),
                    size=(ts, ts)
                ))
            else:
                # Фоллбэк, если текстуры нет
                canvas.add(Color(0.5, 0.5, 0.5, 1))
                canvas.add(Rectangle(
                    pos=(b["curr_pos"][0], b["curr_pos"][1]),
                    size=(ts, ts)
                ))
