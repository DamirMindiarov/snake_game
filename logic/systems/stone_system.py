# logic/systems/stone_system.py
import random
import os
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage  # Для загрузки текстур
from logic.core.interfaces import IGameSystem
from logic.core.world_objects import IWorldPopulator, WORLD_OBJECTS


class StoneSystem(IGameSystem, IWorldPopulator):
    def on_init(self):
        # 1. Загрузка текстуры камня
        path = "assets/stone.png"
        if os.path.exists(path):
            try:
                self.stone_tex = CoreImage(path).texture
                # 'nearest' для четкости мультяшных границ из Paint
                self.stone_tex.mag_filter = 'nearest'
            except Exception as e:
                print(f"Ошибка загрузки текстуры камня: {e}")
                self.stone_tex = None
        else:
            print(f"Файл {path} не найден!")
            self.stone_tex = None

        # 2. Регистрируемся в мире как наполнитель
        if hasattr(self.game, 'world'):
            self.game.world.register_populator(self)

    def populate_chunk(self, cx, cy, chunk_map):
        """Логика расстановки камней (остается без изменений)"""
        cs = self.game.chunk_size
        if random.random() < 0.7:
            for _ in range(random.randint(5, 15)):
                tx = random.randint(cx * cs, (cx + 1) * cs - 1)
                ty = random.randint(cy * cs, (cy + 1) * cs - 1)

                if (tx, ty) not in chunk_map:
                    if abs(tx) > 3 or abs(ty) > 3:
                        chunk_map[(tx, ty)] = 1

    def draw_object(self, obj_id, tx, ty, layers, ts):
        """Отрисовка камня с использованием текстуры"""
        if obj_id == 1:
            px, py = tx * ts, ty * ts

            # Устанавливаем белый цвет (Color 1,1,1,1), чтобы текстура отображалась без искажений
            layers["layer_0"].add(Color(1, 1, 1, 1))

            if self.stone_tex:
                # Рисуем прямоугольник с текстурой
                layers["layer_0"].add(Rectangle(
                    texture=self.stone_tex,
                    pos=(px, py),
                    size=(ts, ts)
                ))
            else:
                # Резервный вариант (заглушка), если текстура не загрузилась
                conf = WORLD_OBJECTS[obj_id]
                layers["layer_0"].add(Color(*conf.get("color", (0.5, 0.5, 0.5, 1))))
                layers["layer_0"].add(Rectangle(pos=(px + 1, py + 1), size=(ts - 2, ts - 2)))

    def on_update(self, dt):
        pass

    def on_render(self, canvas, t, zoom):
        pass
