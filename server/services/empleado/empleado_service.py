from .iempleado_service import IEmpleadoService
from repositories.empleado.iempleado_repository import IEmpleadoRepository

class EmpleadoService(IEmpleadoService):
    def __init__(self, empleado_repository: IEmpleadoRepository):
        self.empleado_repository = empleado_repository

    def obtener_empleados(self):
        return self.empleado_repository.get_all()

    def obtener_empleado_por_id(self, id):
        return self.empleado_repository.get_by_id(id)

    def obtener_empleado_por_area_id(self, area_id):
        return self.empleado_repository.get_by_area_id(area_id)
    
    def empleado_existe_por_email(self, email):
        return self.empleado_repository.exists_by_email(email)