from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def delete(self, data):
        pass

    @abstractmethod
    def save(self, data):
        pass