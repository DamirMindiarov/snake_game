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
