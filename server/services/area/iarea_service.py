from abc import ABC, abstractmethod

class IAreaService(ABC):
    @abstractmethod
    def obtener_areas(self):
        pass

    @abstractmethod
    def obtener_area_por_id(self):
        pass

    def obtener_area_por_nombre(self, nombre):
        pass