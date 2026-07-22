from abc import ABC, abstractmethod

class IEmpleadoService(ABC):
    @abstractmethod
    def obtener_empleados(self):
        pass

    @abstractmethod
    def obtener_empleado_por_id(self, id):
        pass

    @abstractmethod
    def obtener_empleado_por_area(self, area):
        pass