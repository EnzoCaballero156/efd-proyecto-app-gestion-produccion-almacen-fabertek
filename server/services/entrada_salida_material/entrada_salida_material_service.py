from .ientrada_salida_material_service import IEntradaSalidaMaterialService

from repositories.entrada_salida_material.ientrada_salida_material_repository import IEntradaSalidaMaterialRepository
from repositories.area.iarea_repository import IAreaRepository
from repositories.material.imaterial_repository import IMaterialRepository

from entities.entrada_salida_material import EntradaSalidaMaterial

from utils.misc import db
from datetime import datetime, timezone

class EntradaSalidaMaterialService(IEntradaSalidaMaterialService):
    def __init__(self, 
                 entrada_salida_material_repository: IEntradaSalidaMaterialRepository,
                 area_repository: IAreaRepository,
                 material_repository: IMaterialRepository):
        self.entrada_salida_material_repository = entrada_salida_material_repository
        self.area_repository = area_repository
        self.material_repository = material_repository

    def registrar_historial(self, area, tipo_material):
        registro_historial = EntradaSalidaMaterial(area=area, tipo_material=tipo_material)
        self.entrada_salida_material_repository.save(registro_historial)
        db.session.commit()
        return True
    
    def actualizar_historial(self, proceso_actual, siguiente_proceso, material_id):
        area_actual = self.area_repository.get_by_nombre(proceso_actual)
        area_siguiente = self.area_repository.get_by_nombre(siguiente_proceso)
        if not area_actual or not area_siguiente:
            return False
        
        material = self.material_repository.get_by_id(material_id)
        if not material:
            return False
        
        historial_actual = self.entrada_salida_material_repository.get_by_area_and_tipo_material(area_actual.nombre, material.tipo)
        historial_actual.salida_material = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
        self.entrada_salida_material_repository.save(historial_actual)

        nuevo_historial = EntradaSalidaMaterial(area=area_siguiente.nombre, tipo_material=material.tipo)
        self.entrada_salida_material_repository.save(nuevo_historial)
        db.session.commit()
        
        return True
