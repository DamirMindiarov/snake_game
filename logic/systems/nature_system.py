# logic/systems/nature_system.py
import random

from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle, Ellipse
from logic.core.interfaces import IGameSystem
from logic.core.world_objects import IWorldPopulator, WORLD_OBJECTS


class NatureSystem(IGameSystem, IWorldPopulator):
    def on_init(self):
        # Загружаем текстуру заранее для оптимизации 2025
        self.tree_tex = CoreImage("assets/tree.png").texture
        self.tree_tex.mag_filter = 'nearest'
        self.game.world.register_populator(self)
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
        if obj_id == 2:
            px, py = tx * ts, ty * ts

            # 1. Устанавливаем желаемую ширину (2 тайла)
            w = ts * 4

            # 2. Считаем высоту по пропорции картинки (289 / 243 ≈ 1.19)
            # Высота будет: ширина * (высота_ориг / ширина_ориг)
            h = w * (289 / 243)

            layers["layer_1"].add(Color(1, 1, 1, 0.7))
            layers["layer_1"].add(Rectangle(
                texture=self.tree_tex,
                # Смещение:
                # По X: центрируем относительно тайла
                # По Y: корень дерева (низ картинки) в центре тайла + небольшой зазор
                pos=(px - (w - ts) / 2, py + ts * 0.1),
                size=(w, h)
            ))

    def on_update(self, dt):
        pass

    def on_render(self, canvas, t, zoom):
        pass
