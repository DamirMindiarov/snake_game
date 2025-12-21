# logic/world_map.py
import random

from kivy.graphics import InstructionGroup, Color, Rectangle


class WorldMapMixin:
    def init_world_map(self):
        self.tile_size = 60
        self.chunk_size = 20
        self.obstacles = {}  # {(cx, cy): {"stones": set(), "graphics": InstructionGroup}}
        self.generated_chunks = set()

    def generate_chunk_at(self, x, y):
        chunk_px = self.chunk_size * self.tile_size
        cx, cy = int(x // chunk_px), int(y // chunk_px)

        if (cx, cy) not in self.generated_chunks:
            stones = set()
            # Создаем "пакет" графики для чанка
            group = InstructionGroup()
            group.add(Color(0.4, 0.4, 0.4, 1))  # Цвет камней чанка

            if random.random() < 0.7:
                for _ in range(random.randint(5, 15)):
                    tx = random.randint(cx * self.chunk_size, (cx + 1) * self.chunk_size - 1)
                    ty = random.randint(cy * self.chunk_size, (cy + 1) * self.chunk_size - 1)
                    if abs(tx) > 3 or abs(ty) > 3:
                        stones.add((tx, ty))
                        # Добавляем камень в пакет графики ОДИН РАЗ
                        group.add(Rectangle(pos=(tx * 60 + 1, ty * 60 + 1), size=(58, 58)))

            self.obstacles[(cx, cy)] = {"stones": stones, "graphics": group}
            self.generated_chunks.add((cx, cy))

    def check_map_generation(self):
        """Генерируем мир только в 9 чанках вокруг головы"""
        chunk_px = self.chunk_size * self.tile_size
        for dx in [-chunk_px, 0, chunk_px]:
            for dy in [-chunk_px, 0, chunk_px]:
                self.generate_chunk_at(self.world_x + dx, self.world_y + dy)

    def is_tile_solid(self, x, y):
        """Мгновенная проверка коллизии с учетом новой структуры чанка"""
        tx, ty = int(x // self.tile_size), int(y // self.tile_size)
        cx, cy = int(tx // self.chunk_size), int(ty // self.chunk_size)

        # Раньше было: if (cx, cy) in self.obstacles: return (tx, ty) in self.obstacles[(cx, cy)]
        # Теперь данные лежат в ["stones"]
        if (cx, cy) in self.obstacles:
            return (tx, ty) in self.obstacles[(cx, cy)]["stones"]
        return False
