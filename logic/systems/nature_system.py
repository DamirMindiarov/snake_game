# logic/systems/nature_system.py
import random
from kivy.graphics import Color, Rectangle, Ellipse
from logic.core.interfaces import IGameSystem
from logic.core.world_objects import IWorldPopulator, WORLD_OBJECTS


class NatureSystem(IGameSystem, IWorldPopulator):
    def on_init(self):
        # Регистрируем себя как наполнитель в системе мира
        if hasattr(self.game, 'world'):
            self.game.world.register_populator(self)

    def populate_chunk(self, cx, cy, chunk_map):
        """Логика расстановки деревьев в сетку"""
        cs = self.game.chunk_size
        # Генерируем 3-7 деревьев на чанк
        for _ in range(random.randint(3, 7)):
            tx = random.randint(cx * cs, (cx + 1) * cs - 1)
            ty = random.randint(cy * cs, (cy + 1) * cs - 1)

            # Проверяем, не занято ли место (например, камнем от другой системы)
            if (tx, ty) not in chunk_map:
                if abs(tx) > 3 or abs(ty) > 3:
                    chunk_map[(tx, ty)] = 2  # ID ствола дерева

    def draw_object(self, obj_id, tx, ty, layers, ts):
        """Отрисовка дерева на два слоя"""
        if obj_id == 2:
            px, py = tx * ts, ty * ts
            conf = WORLD_OBJECTS[obj_id]

            # 1. Ствол (Слой 0 - под змеей)
            layers["layer_0"].add(Color(*conf["color"]))
            layers["layer_0"].add(Rectangle(
                pos=(px + ts * 0.3, py + ts * 0.3),
                size=(ts * 0.4, ts * 0.4)
            ))

            # 2. Крона (Слой 1 - НАД змеей)
            layers["layer_1"].add(Color(0.1, 0.6, 0.1, 0.6))  # Полупрозрачный зеленый
            layers["layer_1"].add(Ellipse(
                pos=(px - ts * 0.5, py - ts * 0.5),
                size=(ts * 2, ts * 2)
            ))

    def on_update(self, dt):
        pass

    def on_render(self, canvas, t, zoom):
        pass
