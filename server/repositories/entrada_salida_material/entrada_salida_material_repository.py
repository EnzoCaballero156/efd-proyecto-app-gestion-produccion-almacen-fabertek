from .ientrada_salida_material_repository import IEntradaSalidaMaterialRepository
from entities.entrada_salida_material import EntradaSalidaMaterial
from utils.misc import db

class EntradaSalidaMaterialRepository(IEntradaSalidaMaterialRepository):
    def get_all(self):
        return EntradaSalidaMaterial.query.all()

    def get_by_id(self, id):
        return EntradaSalidaMaterial.query.filter_by(id=id).first()

    def get_by_area_and_tipo_material(self, area, tipo_material):
        return EntradaSalidaMaterial.query.filter_by(area=area, tipo_material=tipo_material).first()

    def delete(self, data):
        db.session.delete(data)
        return True

    def save(self, data):
        db.session.add(data)
        return data