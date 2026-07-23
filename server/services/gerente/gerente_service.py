from .igerente_service import IGerenteService
from repositories.empleado.iempleado_repository import IEmpleadoRepository
from repositories.area.iarea_repository import IAreaRepository
from entities.empleado import Empleado, EmpleadoDetalle
from entities.area import Area
from utils.misc import db

class GerenteService(IGerenteService):
    def __init__(self, empleado_repository: IEmpleadoRepository, area_repository: IAreaRepository):
        self.empleado_repository = empleado_repository
        self.area_repository = area_repository

    def registrar_empleado(self, nombre, apellido, email, password, area):
        try:
            area_a_asignar = self.area_repository.get_by_nombre(area)
            if not area_a_asignar:
                area_a_asignar = Area(nombre=area)
                self.area_repository.save(area_a_asignar)
            nuevo_empleado = Empleado(nombre=nombre, apellido=apellido, email=email, password=password)
            nuevo_empleado.detalle = EmpleadoDetalle(area=area_a_asignar)
            self.empleado_repository.save(nuevo_empleado)
            db.session.commit()
            return nuevo_empleado
        except Exception as e:
            db.session.rollback()
            return None

    def editar_empleado_por_id(self, id, nombre, apellido, password):
        try:
            empleado = self.empleado_repository.get_by_id(id)
            empleado.nombre = nombre
            empleado.apellido = apellido
            empleado.password = password
            self.empleado_repository.save(empleado)
            db.session.commit()
            return empleado
        except Exception as e:
            db.session.rollback()
            return None

    def eliminar_empleado_por_id(self, id):
        try:
            empleado = self.empleado_repository.get_by_id(id)
            self.empleado_repository.delete(empleado)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False