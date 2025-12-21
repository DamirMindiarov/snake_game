import random
from kivy.graphics import Color, Rectangle, InstructionGroup
from logic.core.interfaces import IGameSystem


class WorldSystem(IGameSystem):
    def on_init(self):
        # Переносим настройки из старого WorldMapMixin
        self.game.tile_size = 60
        self.game.chunk_size = 20
        self.game.obstacles = {}  # {(cx, cy): {"stones": set(), "graphics": InstructionGroup}}
        self.game.generated_chunks = set()

    def on_update(self, dt):
        """Менеджер чанков: создает мир в радиусе видимости"""
        chunk_px = self.game.chunk_size * self.game.tile_size
        # Генерируем чанки вокруг world_x/y игрока
        for dx in [-chunk_px, 0, chunk_px]:
            for dy in [-chunk_px, 0, chunk_px]:
                self._generate_chunk_at(self.game.world_x + dx, self.game.world_y + dy)

    def on_render(self, canvas, t, zoom):
        """Отрисовка пакетов камней (world_layer)"""
        chunk_px = self.game.chunk_size * self.game.tile_size
        ccx = int(self.game.world_x // chunk_px)
        ccy = int(self.game.world_y // chunk_px)

        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.game.obstacles:
                    canvas.add(self.game.obstacles[(cx, cy)]["graphics"])

    def _generate_chunk_at(self, x, y):
        """Бывшая логика WorldGenerator"""
        chunk_px = self.game.chunk_size * self.game.tile_size
        cx, cy = int(x // chunk_px), int(y // chunk_px)

        if (cx, cy) not in self.game.generated_chunks:
            stones = set()
            group = InstructionGroup()
            group.add(Color(0.4, 0.4, 0.4, 1))

            if random.random() < 0.7:
                for _ in range(random.randint(5, 15)):
                    tx = random.randint(cx * self.game.chunk_size, (cx + 1) * self.game.chunk_size - 1)
                    ty = random.randint(cy * self.game.chunk_size, (cy + 1) * self.game.chunk_size - 1)
                    # Зона спавна игрока пустая
                    if abs(tx) > 3 or abs(ty) > 3:
                        stones.add((tx, ty))
                        group.add(Rectangle(
                            pos=(tx * self.game.tile_size + 1, ty * self.game.tile_size + 1),
                            size=(self.game.tile_size - 2, self.game.tile_size - 2)
                        ))

            # Создаем пустой контейнер данных для чанка
            chunk_data = {
                "stones": stones,
                "graphics": group,
                "food_graphics": InstructionGroup(),  # Будущая еда
                "food_data": []
            }

            self.game.obstacles[(cx, cy)] = chunk_data
            self.game.generated_chunks.add((cx, cy))

            # ВНИМАНИЕ: Оповещаем другие системы (например, Еду), что чанк создан
            self.game.manager.broadcast_chunk(cx, cy, chunk_data)

    def is_tile_solid(self, x, y):
        """Бывшая логика WorldPhysics"""
        ts = self.game.tile_size
        cs = self.game.chunk_size
        tx, ty = int(x // ts), int(y // ts)
        cx, cy = int(tx // cs), int(ty // cs)

        if (cx, cy) in self.game.obstacles:
            return (tx, ty) in self.game.obstacles[(cx, cy)]["stones"]
        return False
