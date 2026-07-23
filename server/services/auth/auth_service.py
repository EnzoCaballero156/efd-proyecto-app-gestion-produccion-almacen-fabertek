from .iauth_service import IAuthService
from repositories.empleado.iempleado_repository import IEmpleadoRepository

class AuthService(IAuthService):
    def __init__(self, empleado_repository: IEmpleadoRepository):
        self.empleado_repository = empleado_repository

    def empleado_existe_por_email(self, email):
        return self.empleado_repository.exists_by_email(email)

    def cargar_sesion_actual(self, id):
        data = self.empleado_repository.get_by_id(id)
        return data
    
    def es_admin(self, email, password):
        if email == "admin@admin.xyz" and password == "admin":
            return True
        return False

    def iniciar_sesion(self, email):
        data = self.empleado_repository.get_by_email(email)
        return data