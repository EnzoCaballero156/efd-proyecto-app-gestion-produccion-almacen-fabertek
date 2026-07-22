from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    def empleado_existe_por_email(self, email):
        pass

    @abstractmethod
    def cargar_sesion_actual(self, id):
        pass

    @abstractmethod
    def es_admin(self, email, password):
        pass

    @abstractmethod
    def iniciar_sesion(self, email):
        pass