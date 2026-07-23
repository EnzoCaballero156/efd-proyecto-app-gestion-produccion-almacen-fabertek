from .iarea_repository import IAreaRepository
from entities.area import Area
from utils.misc import db

class AreaRepository(IAreaRepository):
    def get_all(self):
        return Area.query.all()
    
    def get_by_id(self, id):
        return Area.query.filter_by(id=id).first()

    def get_by_nombre(self, nombre):
        return Area.query.filter_by(nombre=nombre).first()

    def delete(self, data):
        db.session.delete(data)
        return True

    def save(self, data):
        db.session.add(data)
        return data