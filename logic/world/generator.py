# logic/world/generator.py
from kivy.graphics import InstructionGroup, Color, Rectangle, Ellipse
import random


class WorldGenerator:
    def generate_chunk_at(self, x, y):
        chunk_px = self.chunk_size * self.tile_size
        cx, cy = int(x // chunk_px), int(y // chunk_px)

        if (cx, cy) not in self.generated_chunks:
            # 1. ГРАФИКА КАМНЕЙ
            stones = set()
            s_group = InstructionGroup()
            s_group.add(Color(0.4, 0.4, 0.4, 1))

            if random.random() < 0.7:
                for _ in range(random.randint(5, 15)):
                    tx = random.randint(cx * self.chunk_size, (cx + 1) * self.chunk_size - 1)
                    ty = random.randint(cy * self.chunk_size, (cy + 1) * self.chunk_size - 1)
                    if abs(tx) > 3 or abs(ty) > 3:
                        stones.add((tx, ty))
                        s_group.add(Rectangle(pos=(tx * self.tile_size + 1, ty * self.tile_size + 1), size=(58, 58)))

            # 2. ГРАФИКА ЕДЫ (Запекаем статично)
            f_group = InstructionGroup()
            f_list = []
            if hasattr(self, 'spawn_food_in_chunk'):
                f_list = self.spawn_food_in_chunk(cx, cy)
                f_group.add(Color(0, 0.8, 1, 0.8))  # Голубой неон
                for food in f_list:
                    f_group.add(Ellipse(pos=(food["x"] - 8, food["y"] - 8), size=(16, 16)))

            # Сохраняем всё в структуру чанка
            self.obstacles[(cx, cy)] = {
                "stones": stones,
                "graphics": s_group,
                "food_graphics": f_group
            }
            self.generated_chunks.add((cx, cy))
