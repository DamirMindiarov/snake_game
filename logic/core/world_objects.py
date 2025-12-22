# logic/core/world_objects.py
from abc import ABC, abstractmethod

# Свойства объектов мира (ID -> Характеристики)
WORLD_OBJECTS = {
    0: {"name": "empty", "solid": False, "movable": False, "layer": 0},
    1: {"name": "stone", "solid": True, "movable": True, "layer": 0, "color": (0.4, 0.4, 0.4, 1)},

    # Ствол дерева (ID 2): блокирует путь, слой 0 (под змеей)
    2: {"name": "tree_trunk", "solid": True, "movable": False, "layer": 0, "color": (0.4, 0.2, 0.1, 1)},

    # Крона (ID 3): не блокирует путь, слой 1 (НАД змеей)
    3: {"name": "tree_crown", "solid": False, "movable": False, "layer": 1, "color": (0.1, 0.6, 0.1, 0.7)}
}

class IWorldObject(ABC):
    @property
    @abstractmethod
    def is_solid(self):
        """Блокирует ли объект движение?"""
        pass

    @property
    @abstractmethod
    def layer(self):
        """На каком слое рисовать (0 - под змеей, 1 - над змеей)"""
        pass


class IWorldPopulator(ABC):
    @abstractmethod
    def populate_chunk(self, cx, cy, chunk_map):
        """Метод для расстановки ID объектов в сетку чанка"""
        pass

    @abstractmethod
    def draw_object(self, obj_id, tx, ty, layers, ts):
        """Метод для отрисовки конкретного ID"""
        pass