from .iinventario_material_repository import IInventarioMaterialRepository
from entities.inventario_material import InventarioMaterial
from utils.misc import db

class InventarioMaterialRepository(IInventarioMaterialRepository):
    def get_all(self):
        return InventarioMaterial.query.all()

    def get_by_id(self, id):
        return InventarioMaterial.query.filter_by(id=id).first()

    def get_by_empleado_id_and_material_id(self, empleado_id, material_id):
        return InventarioMaterial.query.filter_by(empleado_id=empleado_id, material_id=material_id).first()

    def delete(self, data):
        db.session.delete(data)
        return True

    def save(self, data):
        db.session.add(data)
        return data