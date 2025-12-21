import random
from kivy.graphics import InstructionGroup, Color, Rectangle


class WorldGenerator:
    def generate_chunk_at(self, x, y):
        chunk_px = self.chunk_size * self.tile_size
        cx, cy = int(x // chunk_px), int(y // chunk_px)

        if (cx, cy) not in self.generated_chunks:
            stones = set()
            group = InstructionGroup()
            group.add(Color(0.4, 0.4, 0.4, 1))

            if random.random() < 0.7:
                for _ in range(random.randint(5, 15)):
                    tx = random.randint(cx * self.chunk_size, (cx + 1) * self.chunk_size - 1)
                    ty = random.randint(cy * self.chunk_size, (cy + 1) * self.chunk_size - 1)
                    if abs(tx) > 3 or abs(ty) > 3:
                        stones.add((tx, ty))
                        group.add(Rectangle(pos=(tx * self.tile_size + 1, ty * self.tile_size + 1),
                                            size=(self.tile_size - 2, self.tile_size - 2)))

            self.obstacles[(cx, cy)] = {"stones": stones, "graphics": group}
            self.generated_chunks.add((cx, cy))

            if hasattr(self, 'spawn_food_in_chunk'):
                self.spawn_food_in_chunk(cx, cy)

    def redraw_chunk(self, cx, cy):
        """Полная переборка графики чанка (например, при разрушении)"""
        if (cx, cy) in self.obstacles:
            data = self.obstacles[(cx, cy)]
            data["graphics"].clear()
            data["graphics"].add(Color(0.4, 0.4, 0.4, 1))
            for tx, ty in data["stones"]:
                data["graphics"].add(Rectangle(pos=(tx * self.tile_size + 1, ty * self.tile_size + 1),
                                               size=(self.tile_size - 2, self.tile_size - 2)))
