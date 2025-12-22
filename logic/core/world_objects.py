# logic/core/world_objects.py
from abc import ABC, abstractmethod

# Свойства объектов мира (ID -> Характеристики)
WORLD_OBJECTS = {
    0: {"name": "empty", "solid": False, "movable": False, "layer": 0},
    1: {
        "name": "stone",
        "solid": True, "movable": True, "layer": 0,
        "texture": "assets/stone.png"
    },
    2: {
        "name": "tree",
        "solid": True, "movable": False, "layer": 0,
        "texture": "assets/tree.png"
    }
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