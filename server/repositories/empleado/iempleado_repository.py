from ..base.irepository import IRepository
from abc import abstractmethod

class IEmpleadoRepository(IRepository):
    @abstractmethod
    def get_all_activo(self):
        pass

    @abstractmethod
    def get_by_area_id(self, area_id):
        pass
    
    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def exists_by_email(self, email):
        pass