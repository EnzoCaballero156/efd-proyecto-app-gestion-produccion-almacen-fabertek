from flask import Blueprint, request, jsonify
from repositories.material.material_repository import MaterialRepository
from repositories.entrada_salida_material.entrada_salida_material_repository import EntradaSalidaMaterialRepository
from repositories.empleado.empleado_repository import EmpleadoRepository
from repositories.inventario.inventario_repository import InventarioRepository

from services.empleado.empleado_service import EmpleadoService
from services.material.material_service import MaterialService
from services.entrada_salida_material.entrada_salida_material_service import EntradaSalidaMaterialService

material_bp = Blueprint('material_bp', __name__)

material_repository = MaterialRepository()
entrada_salida_material_repository = EntradaSalidaMaterialRepository()
empleado_repository = EmpleadoRepository()
inventario_repository = InventarioRepository()

empleado_service = EmpleadoService(empleado_repository)
material_service = MaterialService(material_repository, empleado_repository, inventario_repository)
entrada_salida_material_service = EntradaSalidaMaterialService(
    entrada_salida_material_repository, empleado_repository, material_repository
)

@material_bp.post('/registrar')
def registrar_material():
    empleado_id = request.json['empleadoID']
    tipo_material = request.json['tipoMaterial']
    cantidad = request.json['cantidad']
    estado = request.json['estado']
    
    if not empleado_id or not tipo_material or not cantidad or not estado:
        return jsonify({"error": "No autorizado."}), 401
    
    empleado = empleado_service.obtener_empleado_por_id(empleado_id)
    if not empleado:
        return jsonify({"error": "Empleado no existe."}), 404

    nuevo_material = material_service.registrar_material(empleado, tipo_material, cantidad, estado)
    entrada_salida_material_service.registrar_historial(empleado.detalle.area, tipo_material)

    return jsonify({
        "id": nuevo_material.id,
        "tipoMaterial": nuevo_material.tipo,
        "cantidad": cantidad,
        "estado": estado,
        "area": empleado.detalle.area
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

    return jsonify({
        "tipoMaterial": inventario_actual.material.tipo,
        "estadoActual": inventario_actual.estado,
        "cantidadActual": inventario_actual.cantidad,
    })

@material_bp.put('/actualizar-estado/<material_id>')
def actualizar_estado_material(material_id):
    empleado_id = request.json['empleadoID']
    estado = request.json['estado']

    empleado = empleado_service.obtener_empleado_por_id(empleado_id)
    if not empleado:
        return jsonify({"error": "Empleado no existe."}), 404
    
    material = material_service.obtener_material_por_id(material_id)
    if not material:
        return jsonify({"error": "Material no existe."}), 404

    inventario_actualizado = material_service.actualizar_estado_material(empleado, material, estado)

    return jsonify({
        "nuevoEstado": inventario_actualizado.estado
    })