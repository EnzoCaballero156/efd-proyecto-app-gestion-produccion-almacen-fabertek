from abc import ABC, abstractmethod
class IEntradaSalidaMaterialService(ABC):
    @abstractmethod
    def registrar_historial(self, area, tipo_material):
        pass
    
    @abstractmethod
    def actualizar_historial(self, empleado_id, material_id, estado):
        pass
