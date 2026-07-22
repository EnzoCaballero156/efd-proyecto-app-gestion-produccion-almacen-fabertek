from .iempleado_repository import IEmpleadoRepository
from entities.empleado import Empleado, EmpleadoDetalle
from utils.misc import db

class EmpleadoRepository(IEmpleadoRepository):
    def get_all(self):
        return Empleado.query.all()

    def get_by_id(self, id):
        return Empleado.query.filter_by(id=id).first()

    def get_by_area(self, area):
        data = EmpleadoDetalle.query.filter_by(area=area).first()
        return data.empleado if data else None

    def get_by_email(self, email):
        return Empleado.query.filter_by(email=email).first()
    
    def exists_by_email(self, email):
        return Empleado.query.filter_by(email=email).first() is not None

    def delete(self, data):
        db.session.delete(data)
        return True

    def save(self, data):
        db.session.add(data)
        return data