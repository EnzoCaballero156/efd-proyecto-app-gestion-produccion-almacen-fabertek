from .ientrada_salida_material_service import IEntradaSalidaMaterialService

from repositories.entrada_salida_material.ientrada_salida_material_repository import IEntradaSalidaMaterialRepository
from repositories.empleado.iempleado_repository import IEmpleadoRepository
from repositories.material.imaterial_repository import IMaterialRepository

from entities.entrada_salida_material import EntradaSalidaMaterial

from utils.misc import db
from datetime import datetime, timezone

class EntradaSalidaMaterialService(IEntradaSalidaMaterialService):
    def __init__(self, 
                 entrada_salida_material_repository: IEntradaSalidaMaterialRepository,
                 empleado_repository: IEmpleadoRepository,
                 material_repository: IMaterialRepository):
        self.entrada_salida_material_repository = entrada_salida_material_repository
        self.empleado_repository = empleado_repository
        self.material_repository = material_repository

    def registrar_historial(self, area, tipo_material):
        registro_historial = EntradaSalidaMaterial(area=area, tipo_material=tipo_material)
        self.entrada_salida_material_repository.save(registro_historial)
        db.session.commit()
        return True
    
    def actualizar_historial(self, proceso_actual, siguiente_proceso, material_id):
        empleado_actual = self.empleado_repository.get_by_area(proceso_actual)
        empleado_receptor = self.empleado_repository.get_by_area(siguiente_proceso)
        if not empleado_actual or not empleado_receptor:
            return False
        
        material = self.material_repository.get_by_id(material_id)
        if not material:
            return False
        
        historial_actual = self.entrada_salida_material_repository.get_by_area_and_tipo_material(empleado_actual.detalle.area, material.tipo)
        historial_actual.salida_material = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S")
        self.entrada_salida_material_repository.save(historial_actual)

        nuevo_historial = EntradaSalidaMaterial(area=empleado_receptor.detalle.area, tipo_material=material.tipo)
        self.entrada_salida_material_repository.save(nuevo_historial)

        db.session.commit()

        return True
