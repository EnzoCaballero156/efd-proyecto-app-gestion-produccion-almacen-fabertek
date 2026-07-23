from .imaterial_service import IMaterialService

from repositories.material.imaterial_repository import IMaterialRepository
from repositories.empleado.iempleado_repository import IEmpleadoRepository
from repositories.inventario.iinventario_empleado_repository import IInventarioEmpleadoRepository

from entities.material import Material
from entities.inventario_empleado import InventarioEmpleado

from utils.misc import db

class MaterialService(IMaterialService):
    def __init__(
            self, material_repository: IMaterialRepository, 
            empleado_repository: IEmpleadoRepository,
            inventario_empleado_repository: IInventarioEmpleadoRepository
            ):
        self.material_repository = material_repository
        self.empleado_repository = empleado_repository
        self.inventario_empleado_repository = inventario_empleado_repository

    def __obtener_empleados(self, proceso_actual, siguiente_proceso):
        empleado_actual = self.empleado_repository.get_by_area(proceso_actual)
        empleado_receptor = self.empleado_repository.get_by_area(siguiente_proceso)
        return empleado_actual, empleado_receptor
    
    def __obtener_inventarios(self, empleado_actual_id, empleado_receptor_id, material_id):
        inventario_actual = self.inventario_empleado_repository.get_by_empleado_id_and_material_id(empleado_actual_id, material_id)
        inventario_receptor = self.inventario_empleado_repository.get_by_empleado_id_and_material_id(empleado_receptor_id, material_id)
        return inventario_actual, inventario_receptor

    def __actualizar_stock(self, inventario_actual, inventario_receptor, cantidad):
        inventario_actual.cantidad -= cantidad
        inventario_receptor.cantidad += cantidad
        self.inventario_empleado_repository.save(inventario_actual)
        self.inventario_empleado_repository.save(inventario_receptor)
        return True

    def obtener_material_por_id(self, id):
        return self.material_repository.get_by_id(id)

    def registrar_material(self, empleado, tipo, cantidad, estado):
        nuevo_material = Material(tipo=tipo)
        self.material_repository.save(nuevo_material)
        registro_inventario = InventarioEmpleado(empleado=empleado.detalle, estado=estado, cantidad=cantidad, material=nuevo_material)
        self.inventario_empleado_repository.save(registro_inventario)
        db.session.commit()

        return nuevo_material

    def enviar_material(self, proceso_actual, siguiente_proceso, material_a_enviar, cantidad):
        empleado_actual, empleado_receptor = self.__obtener_empleados(proceso_actual, siguiente_proceso)
        if not empleado_actual or not empleado_receptor:
            return None

        inventario_actual, inventario_receptor = self.__obtener_inventarios(empleado_actual.detalle.id, empleado_receptor.detalle.id, material_a_enviar.id)
        if not inventario_actual or inventario_actual.cantidad < cantidad: 
            return None
        
        if not inventario_receptor:
            inventario_receptor = InventarioEmpleado(empleado=empleado_receptor.detalle, estado=inventario_actual.estado, material=material_a_enviar, cantidad=0)
            self.inventario_empleado_repository.save(inventario_receptor)

        self.__actualizar_stock(inventario_actual, inventario_receptor, cantidad)
        db.session.commit()

        return inventario_actual

    def actualizar_estado_material(self, empleado, material, estado):
        inventario = self.inventario_empleado_repository.get_by_empleado_id_and_material_id(empleado.detalle.id, material.id)
        inventario.estado = estado
        self.inventario_empleado_repository.save(inventario)
        db.session.commit()
        return inventario