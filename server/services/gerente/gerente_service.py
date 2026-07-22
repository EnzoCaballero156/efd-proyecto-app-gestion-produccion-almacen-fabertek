from .igerente_service import IGerenteService
from repositories.empleado.iempleado_repository import IEmpleadoRepository
from entities.empleado import Empleado, EmpleadoDetalle
from utils.misc import db

class GerenteService(IGerenteService):
    def __init__(self, empleado_repository: IEmpleadoRepository):
        self.empleado_repository = empleado_repository

    def registrar_empleado(self, nombre, apellido, email, password, area):
        nuevo_empleado = Empleado(nombre=nombre, apellido=apellido, email=email, password=password)
        nuevo_empleado.detalle = EmpleadoDetalle(area=area)
        self.empleado_repository.save(nuevo_empleado)
        db.session.commit()
        return nuevo_empleado

    def editar_empleado_por_id(self, id, nombre, apellido, password):
        empleado = self.empleado_repository.get_by_id(id)
        empleado.nombre = nombre
        empleado.apellido = apellido
        empleado.password = password
        self.empleado_repository.save(empleado)
        db.session.commit()
        return empleado

    def eliminar_empleado_por_id(self, id):
        empleado = self.empleado_repository.get_by_id(id)
        self.empleado_repository.delete(empleado)
        db.session.commit()
        return True