from .iinventario_area_repository import IInventarioAreaRepository
from entities.inventario_area import InventarioArea
from utils.misc import db

class InventarioAreaRepository(IInventarioAreaRepository):
    def get_all(self):
        return InventarioArea.query.all()

    def get_by_id(self, id):
        return InventarioArea.query.filter_by(id=id).first()

    def get_by_area_id_and_material_id(self, area_id, material_id):
        return InventarioArea.query.filter_by(area_id=area_id, material_id=material_id).first()

    def delete(self, data):
        db.session.delete(data)
        return True

    def save(self, data):
        db.session.add(data)
        return data