from ..base.irepository import IRepository
from abc import abstractmethod

class IInventarioAreaRepository(IRepository):
    @abstractmethod
    def get_by_area_id_and_material_id(self, area_id, material_id):
        pass