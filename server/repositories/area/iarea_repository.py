from ..base.irepository import IRepository
from abc import abstractmethod

class IAreaRepository(IRepository):
    @abstractmethod
    def get_by_nombre(self, nombre):
        pass