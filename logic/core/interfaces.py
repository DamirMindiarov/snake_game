from abc import ABC, abstractmethod

class IGameSystem(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def on_init(self): pass

    @abstractmethod
    def on_update(self, dt): pass

    @abstractmethod
    def on_render(self, canvas, t, zoom): pass

    def on_chunk_generated(self, cx, cy, chunk_data):
        """Событие создания чанка (опционально для систем)"""
        pass

class IVisualEffect:
    """Интерфейс для любого визуального эффекта"""
    def update(self, dt): pass
    def draw(self, canvas): pass
    @property
    def is_alive(self): return True


class IEntity(ABC):
    def __init__(self, game, pos):
        self.game = game
        self.pos = list(pos)  # [x, y]
        self.vel = [0.0, 0.0]
        self.alive = True
        self.size = 32

    @abstractmethod
    def update(self, dt):
        """Логика ИИ и перемещения"""
        pass

    @abstractmethod
    def draw(self, canvas):
        """Отрисовка (обычно Rectangle с текстурой)"""
        pass

    @abstractmethod
    def on_catch(self):
        """Событие поедания змеей"""
        pass