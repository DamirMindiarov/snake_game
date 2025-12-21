# logic/world_map.py
import random


class WorldMapMixin:
    def init_world_map(self):
        self.tile_size = 60
        self.chunk_size = 20  # Чанк 20x20 клеток (1200x1200px)

        # ГЛАВНОЕ: Храним камни по чанкам для мгновенного доступа
        self.obstacles = {}  # {(cx, cy): set((tx, ty), ...)}
        self.generated_chunks = set()

    def generate_chunk_at(self, x, y):
        chunk_px = self.chunk_size * self.tile_size
        # ПРИНУДИТЕЛЬНО приводим к int, чтобы ключи были (1, 2), а не (1.0, 2.0)
        cx = int(x // chunk_px)
        cy = int(y // chunk_px)

        if (cx, cy) not in self.generated_chunks:
            stones = []
            if random.random() < 0.7:
                for _ in range(random.randint(5, 10)):
                    tx = random.randint(cx * self.chunk_size, (cx + 1) * self.chunk_size - 1)
                    ty = random.randint(cy * self.chunk_size, (cy + 1) * self.chunk_size - 1)
                    if abs(tx) > 3 or abs(ty) > 3:
                        stones.append((tx, ty))

            self.obstacles[(cx, cy)] = stones
            self.generated_chunks.add((cx, cy))

    def check_map_generation(self):
        """Генерируем мир только в 9 чанках вокруг головы"""
        chunk_px = self.chunk_size * self.tile_size
        for dx in [-chunk_px, 0, chunk_px]:
            for dy in [-chunk_px, 0, chunk_px]:
                self.generate_chunk_at(self.world_x + dx, self.world_y + dy)

    def is_tile_solid(self, x, y):
        """Мгновенная проверка коллизии O(1)"""
        tx, ty = int(x // self.tile_size), int(y // self.tile_size)
        cx, cy = int(tx // self.chunk_size), int(ty // self.chunk_size)

        if (cx, cy) in self.obstacles:
            return (tx, ty) in self.obstacles[(cx, cy)]
        return False
