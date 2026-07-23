from ..base.irepository import IRepository
from abc import abstractmethod

class IInventarioMaterialRepository(IRepository):
    @abstractmethod
    def get_by_empleado_id_and_material_id(self, empleado_id, material_id):
        pass