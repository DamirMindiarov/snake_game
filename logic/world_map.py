from logic.world.generator import WorldGenerator
from logic.world.physics import WorldPhysics

class WorldMapMixin(WorldGenerator, WorldPhysics):
    def init_world_map(self):
        self.tile_size = 60
        self.chunk_size = 20
        self.obstacles = {}  # {(cx, cy): {"stones": set(), "graphics": InstructionGroup}}
        self.generated_chunks = set()

    def check_map_generation(self):
        """Менеджер чанков: создает мир в радиусе видимости"""
        chunk_px = self.chunk_size * self.tile_size
        # Генерируем 9 чанков вокруг игрока
        for dx in [-chunk_px, 0, chunk_px]:
            for dy in [-chunk_px, 0, chunk_px]:
                self.generate_chunk_at(self.world_x + dx, self.world_y + dy)
