# logic/core/mutations.py
from abc import abstractmethod

from logic.core.config import MUTATIONS_CONFIG
from logic.core.interfaces import IGameSystem



class IMutationSystem(IGameSystem):
    @property
    @abstractmethod
    def mutation_id(self):
        """Должен совпадать с ключом в MUTATIONS_CONFIG"""
        pass

    # def is_active(self):
    #     """Проверяет состояние напрямую в конфиге"""
    #     return MUTATIONS_CONFIG.get(self.mutation_id, {}).get("active", False)

    def is_active(self):
        return self.game.mutations.get(self.mutation_id, False)

