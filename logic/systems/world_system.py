# logic/systems/world_system.py
import random
from kivy.graphics import InstructionGroup
from logic.core.interfaces import IGameSystem


class WorldSystem(IGameSystem):
    def on_init(self):
        self.game.tile_size = 60
        self.game.chunk_size = 20
        # Логика: {(cx, cy): {(tx, ty): object_id}}
        self.game.world_map = {}
        # Графика: {(cx, cy): {"layer_0": IG, "layer_1": IG, "food": IG}}
        self.game.obstacles = {}
        self.game.generated_chunks = set()
        self.populators = []  # Список систем-наполнителей (NatureSystem и т.д.)

    def register_populator(self, populator):
        self.populators.append(populator)

    def is_tile_solid(self, x, y):
        ts, cs = self.game.tile_size, self.game.chunk_size
        tx, ty = int(x // ts), int(y // ts)
        cx, cy = int(tx // cs), int(ty // cs)

        chunk_data = self.game.world_map.get((cx, cy))
        if chunk_data:
            obj_id = chunk_data.get((tx, ty), 0)
            # Импортируем конфиг внутри, чтобы избежать циклической зависимости
            from logic.core.world_objects import WORLD_OBJECTS
            return WORLD_OBJECTS.get(obj_id, {}).get("solid", False)
        return False

    def _generate_chunk_at(self, x, y):
        ts, cs = self.game.tile_size, self.game.chunk_size
        px = cs * ts
        cx, cy = int(x // px), int(y // px)

        if (cx, cy) not in self.game.generated_chunks:
            chunk_map = {}
            for p in self.populators:
                p.populate_chunk(cx, cy, chunk_map)

            self.game.world_map[(cx, cy)] = chunk_map

            # 3. УДАЛИЛИ "food_graphics" отсюда
            layers = {
                "layer_0": InstructionGroup(),
                "layer_1": InstructionGroup()
            }
            self.game.obstacles[(cx, cy)] = layers

            self.redraw_chunk(cx, cy)
            self.game.generated_chunks.add((cx, cy))

            # 4. ИСПРАВИЛИ: теперь просто уведомляем о новом чанке без специфики еды
            self.game.manager.broadcast_chunk(cx, cy, layers)

    def redraw_chunk(self, cx, cy):
        layers = self.game.obstacles.get((cx, cy))
        chunk_map = self.game.world_map.get((cx, cy), {})
        if not layers: return

        layers["layer_0"].clear()
        layers["layer_1"].clear()
        # Слой еды здесь больше не очищаем, так как его нет в словаре layers

        for (tx, ty), obj_id in chunk_map.items():
            for p in self.populators:
                p.draw_object(obj_id, tx, ty, layers, self.game.tile_size)

    def on_update(self, dt):
        # Стандартный обход 9 чанков вокруг игрока
        px = self.game.chunk_size * self.game.tile_size
        for dx in [-px, 0, px]:
            for dy in [-px, 0, px]:
                self._generate_chunk_at(self.game.world_x + dx, self.game.world_y + dy)

    def on_render(self, canvas, t, zoom):
        """Отрисовка НИЖНЕГО слоя (камни, стволы)"""
        ts = self.game.tile_size
        cs = self.game.chunk_size
        chunk_px = cs * ts

        ccx = int(self.game.world_x // chunk_px)
        ccy = int(self.game.world_y // chunk_px)

        # Рисуем 9 чанков вокруг игрока
        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.game.obstacles:
                    # Добавляем на холст слой 0 (камни и стволы)
                    canvas.add(self.game.obstacles[(cx, cy)]["layer_0"])

    def draw_upper_layer(self, canvas):
        """Отрисовка крон деревьев поверх змеи"""
        # Берем настройки из общего стейта игры
        ts = self.game.tile_size
        cs = self.game.chunk_size
        chunk_px = cs * ts

        # Определяем текущий чанк игрока
        ccx = int(self.game.world_x // chunk_px)
        ccy = int(self.game.world_y // chunk_px)

        # Отрисовываем 9 ближайших чанков
        for cx in range(ccx - 1, ccx + 2):
            for cy in range(ccy - 1, ccy + 2):
                if (cx, cy) in self.game.obstacles:
                    # Извлекаем слой крон (layer_1)
                    layer_1 = self.game.obstacles[(cx, cy)].get("layer_1")
                    if layer_1:
                        canvas.add(layer_1)

    def pop_object(self, tx, ty):
        """Вырезает объект из мира и возвращает его ID"""
        cx, cy = tx // self.game.chunk_size, ty // self.game.chunk_size
        chunk_map = self.game.world_map.get((cx, cy))
        if chunk_map and (tx, ty) in chunk_map:
            obj_id = chunk_map.pop((tx, ty))
            self.redraw_chunk(cx, cy)
            return obj_id
        return None

    def place_object(self, tx, ty, obj_id):
        """Вмораживает объект обратно в статику"""
        cx, cy = tx // self.game.chunk_size, ty // self.game.chunk_size
        if (cx, cy) not in self.game.world_map:
            self.game.world_map[(cx, cy)] = {}
        self.game.world_map[(cx, cy)][(tx, ty)] = obj_id
        self.redraw_chunk(cx, cy)
