# logic/systems/stone_system.py
import random
from kivy.graphics import Color, Rectangle
from logic.core.interfaces import IGameSystem
from logic.core.world_objects import IWorldPopulator, WORLD_OBJECTS


class StoneSystem(IGameSystem, IWorldPopulator):
    def on_init(self):
        # Регистрируемся в мире как наполнитель
        if hasattr(self.game, 'world'):
            self.game.world.register_populator(self)

    def populate_chunk(self, cx, cy, chunk_map):
        """Логика расстановки камней"""
        cs = self.game.chunk_size
        # Генерируем 5-15 камней на чанк
        if random.random() < 0.7:  # Шанс, что чанк не пустой
            for _ in range(random.randint(5, 15)):
                tx = random.randint(cx * cs, (cx + 1) * cs - 1)
                ty = random.randint(cy * cs, (cy + 1) * cs - 1)

                if (tx, ty) not in chunk_map:
                    if abs(tx) > 3 or abs(ty) > 3:
                        chunk_map[(tx, ty)] = 1  # ID Камня

    def draw_object(self, obj_id, tx, ty, layers, ts):
        """Отрисовка камня"""
        if obj_id == 1:
            px, py = tx * ts, ty * ts
            conf = WORLD_OBJECTS[obj_id]

            # Камни рисуем только на нижнем слое (0)
            layers["layer_0"].add(Color(*conf["color"]))
            layers["layer_0"].add(Rectangle(
                pos=(px + 1, py + 1),
                size=(ts - 2, ts - 2)
            ))

    def on_update(self, dt):
        pass

    def on_render(self, canvas, t, zoom):
        pass
