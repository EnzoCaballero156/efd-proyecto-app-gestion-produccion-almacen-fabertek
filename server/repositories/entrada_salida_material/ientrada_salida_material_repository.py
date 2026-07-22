from ..base.irepository import IRepository
from abc import abstractmethod

class IEntradaSalidaMaterialRepository(IRepository):
    @abstractmethod
    def get_by_area_and_tipo_material(self, area, tipo_material):
        pass