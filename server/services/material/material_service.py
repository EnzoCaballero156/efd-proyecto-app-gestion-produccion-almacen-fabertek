from .imaterial_service import IMaterialService

from repositories.material.imaterial_repository import IMaterialRepository
from repositories.empleado.iempleado_repository import IEmpleadoRepository
from repositories.inventario.iinventario_area_repository import IInventarioAreaRepository
from repositories.area.iarea_repository import IAreaRepository

from entities.material import Material
from entities.inventario_area import InventarioArea

from utils.misc import db

class MaterialService(IMaterialService):
    def __init__(
            self, material_repository: IMaterialRepository, 
            empleado_repository: IEmpleadoRepository,
            inventario_area_repository: IInventarioAreaRepository,
            area_repository: IAreaRepository
            ):
        self.material_repository = material_repository
        self.empleado_repository = empleado_repository
        self.inventario_area_repository = inventario_area_repository
        self.area_repository = area_repository
 
    def __obtener_areas(self, proceso_actual, siguiente_proceso):
        area_actual = self.area_repository.get_by_nombre(proceso_actual)
        area_siguiente = self.area_repository.get_by_nombre(siguiente_proceso)
        return area_actual, area_siguiente
    
    def __obtener_inventarios(self, area_actual_id, area_siguiente_id, material_id):
        inventario_actual = self.inventario_area_repository.get_by_area_id_and_material_id(area_actual_id, material_id)
        inventario_siguiente = self.inventario_area_repository.get_by_area_id_and_material_id(area_siguiente_id, material_id)
        return inventario_actual, inventario_siguiente

    def __actualizar_stock(self, inventario_actual, inventario_siguiente, cantidad):
        inventario_actual.cantidad -= cantidad
        inventario_siguiente.cantidad += cantidad
        self.inventario_area_repository.save(inventario_actual)
        self.inventario_area_repository.save(inventario_siguiente)
        return True

    def obtener_material_por_id(self, id):
        return self.material_repository.get_by_id(id)

    def registrar_material(self, area, tipo, cantidad, estado):
        try:
            nuevo_material = Material(tipo=tipo)
            self.material_repository.save(nuevo_material)
            registro_inventario = InventarioArea(area=area, estado=estado, cantidad=cantidad, material=nuevo_material)
            self.inventario_area_repository.save(registro_inventario)
            db.session.commit()
            return nuevo_material
        except Exception as e:
            db.session.rollback()
            return None

    def enviar_material(self, proceso_actual, siguiente_proceso, material_a_enviar, cantidad):
        try:
            area_actual, area_siguiente = self.__obtener_areas(proceso_actual, siguiente_proceso)
            if not area_actual or not area_siguiente:
                return None
            
            inventario_actual, inventario_siguiente = self.__obtener_inventarios(area_actual.id, area_siguiente.id, material_a_enviar.id)
            if not inventario_actual or inventario_actual.cantidad < cantidad: 
                return None
            if not inventario_siguiente:
                inventario_siguiente = InventarioArea(area=area_siguiente, estado=inventario_actual.estado, material=material_a_enviar, cantidad=0)
                self.inventario_area_repository.save(inventario_siguiente)

            self.__actualizar_stock(inventario_actual, inventario_siguiente, cantidad)
            db.session.commit()
            return inventario_actual
        except Exception as e:
            db.session.rollback()
            return None

    def actualizar_estado_material(self, area, material, estado):
        try:
            inventario = self.inventario_area_repository.get_by_area_id_and_material_id(area.id, material.id)
            inventario.estado = estado
            self.inventario_area_repository.save(inventario)
            db.session.commit()
            return inventario
        except Exception as e:
            db.session.rollback()
            return None