from .imaterial_repository import IMaterialRepository
from entities.material import Material
from utils.misc import db

class MaterialRepository(IMaterialRepository):
    def get_all(self):
        return Material.query.all()

    def get_by_id(self, id):
        return Material.query.filter_by(id=id).first()

    def delete(self, data):
        db.session.delete(data)
        return True

    def save(self, data):
        db.session.add(data)
        return data