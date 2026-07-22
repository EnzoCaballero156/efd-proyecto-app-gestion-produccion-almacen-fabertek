from abc import ABC, abstractmethod

class IGerenteService(ABC):
    @abstractmethod
    def registrar_empleado(self, nombre, apellido, email, password, area):
        pass

    @abstractmethod
    def editar_empleado_por_id(self, id, nombre, apellido, password):
        pass

    @abstractmethod
    def eliminar_empleado_por_id(self, id):
        pass