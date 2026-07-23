from abc import ABC, abstractmethod

class IMaterialService(ABC):
    @abstractmethod
    def obtener_material_por_id(self, id):
        pass
    
    @abstractmethod
    def registrar_material(self, area, tipo, cantidad, estado):
        pass

    @abstractmethod
    def enviar_material(self, proceso_actual, siguiente_proceso, material_a_enviar, cantidad):
        pass

    @abstractmethod
    def actualizar_estado_material(self, area, material, estado):
        pass