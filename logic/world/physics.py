class WorldPhysics:
    def is_tile_solid(self, x, y):
        """O(1) проверка коллизии через хэш-таблицу чанков"""
        tx, ty = int(x // self.tile_size), int(y // self.tile_size)
        cx, cy = int(tx // self.chunk_size), int(ty // self.chunk_size)

        if (cx, cy) in self.obstacles:
            return (tx, ty) in self.obstacles[(cx, cy)]["stones"]
        return False
