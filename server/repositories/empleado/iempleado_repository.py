from ..base.irepository import IRepository
from abc import abstractmethod

class IEmpleadoRepository(IRepository):
    @abstractmethod
    def get_by_area(self, area):
        pass
    
    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def exists_by_email(self, email):
        pass