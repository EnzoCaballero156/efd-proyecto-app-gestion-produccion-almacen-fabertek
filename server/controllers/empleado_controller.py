from flask import Blueprint, jsonify
from repositories.empleado.empleado_repository import EmpleadoRepository
from services.empleado.empleado_service import EmpleadoService

empleado_bp = Blueprint('empleado_bp', __name__)

empleado_repository = EmpleadoRepository()
empleado_service = EmpleadoService(empleado_repository)

@empleado_bp.get('/')
def obtener_empleados():
    empleados = empleado_service.obtener_empleados()
    return jsonify([{
        "id": empleado.id,
        "nombre": empleado.nombre,
        "apellido": empleado.apellido,
        "email": empleado.email,
        "password": empleado.password,
        "area": empleado.detalle.area
    } for empleado in empleados])

@empleado_bp.get('/id/<id>')
def obtener_empleado_por_id(id):
    empleado = empleado_service.obtener_empleado_por_id(id)

    if empleado is None:
        return jsonify({"error": "Empleado no existe."}), 404
    
    return jsonify({
        "id": empleado.id,
        "nombre": empleado.nombre,
        "apellido": empleado.apellido,
        "email": empleado.email,
        "password": empleado.password,
        "area": empleado.detalle.area
    })

@empleado_bp.get('/area/<area>')
def obtener_empleado_por_area(area):
    empleado = empleado_service.obtener_empleado_por_area(area)

    if empleado is None:
        return jsonify({"error": "Empleado no existe."}), 404
    
    return jsonify({
        "id": empleado.id,
        "nombre": empleado.nombre,
        "apellido": empleado.apellido,
        "email": empleado.email,
        "password": empleado.password,
        "area": empleado.detalle.area
    })