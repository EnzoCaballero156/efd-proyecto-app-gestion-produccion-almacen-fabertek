from flask import Blueprint, request, jsonify
from repositories.material.material_repository import MaterialRepository
from repositories.entrada_salida_material.entrada_salida_material_repository import EntradaSalidaMaterialRepository
from repositories.empleado.empleado_repository import EmpleadoRepository
from repositories.inventario.inventario_area_repository import InventarioAreaRepository
from repositories.area.area_repository import AreaRepository

from services.empleado.empleado_service import EmpleadoService
from services.material.material_service import MaterialService
from services.entrada_salida_material.entrada_salida_material_service import EntradaSalidaMaterialService
from services.area.area_service import AreaService

material_bp = Blueprint('material_bp', __name__)

material_repository = MaterialRepository()
entrada_salida_material_repository = EntradaSalidaMaterialRepository()
empleado_repository = EmpleadoRepository()
inventario_area_repository = InventarioAreaRepository()
area_repository = AreaRepository()

empleado_service = EmpleadoService(empleado_repository)
material_service = MaterialService(material_repository, empleado_repository, inventario_area_repository, area_repository)
entrada_salida_material_service = EntradaSalidaMaterialService(
    entrada_salida_material_repository, area_repository, material_repository
)
area_service = AreaService(area_repository)

@material_bp.post('/registrar')
def registrar_material():
    area = request.json['area']
    tipo_material = request.json['tipoMaterial']
    cantidad = request.json['cantidad']
    estado = request.json['estado']
    
    if not area or not tipo_material or not cantidad or not estado:
        return jsonify({"error": "No autorizado."}), 401
    
    area_actual = area_service.obtener_area_por_nombre(area)
    if not area_actual:
        return jsonify({"error": "Area no existe."}), 404

    nuevo_material = material_service.registrar_material(area_actual, tipo_material, cantidad, estado)
    if not nuevo_material:
        return jsonify({"error": "No se pudo realizar la operación."}), 401
    
    entrada_salida_material_service.registrar_historial(area_actual.nombre, nuevo_material.tipo)

    return jsonify({
        "id": nuevo_material.id,
        "tipoMaterial": nuevo_material.tipo,
        "cantidad": cantidad,
        "estado": estado,
        "area": area_actual.nombre
    })

@material_bp.post('/enviar-a/<siguiente_proceso>')
def enviar_material(siguiente_proceso):
    proceso_actual = request.json['procesoActual']
    if not proceso_actual:
        return jsonify({"error": "No autorizado."}), 401
    
    material_id = request.json['materialID']
    cantidad = request.json['cantidad']

    material_a_enviar = material_service.obtener_material_por_id(material_id)
    if not material_a_enviar:
        return jsonify({"error": "Material no existe."}), 404
    
    inventario_actual = material_service.enviar_material(proceso_actual, siguiente_proceso, material_a_enviar, cantidad)
    if not inventario_actual:
        return jsonify({"error": "No se pudo realizar la operación."}), 401
    
    entrada_salida_material_service.actualizar_historial(proceso_actual, siguiente_proceso, material_id)

    return jsonify({
        "tipoMaterial": inventario_actual.material.tipo,
        "estadoActual": inventario_actual.estado,
        "cantidadActual": inventario_actual.cantidad,
    })

@material_bp.put('/actualizar-estado/<material_id>')
def actualizar_estado_material(material_id):
    area = request.json['area']
    estado = request.json['estado']

    area_actual = area_service.obtener_area_por_nombre(area)
    if not area_actual:
        return jsonify({"error": "Área no existe."}), 404
    
    material = material_service.obtener_material_por_id(material_id)
    if not material:
        return jsonify({"error": "Material no existe."}), 404

    inventario_actualizado = material_service.actualizar_estado_material(area_actual, material, estado)

    return jsonify({
        "nuevoEstado": inventario_actualizado.estado
    })