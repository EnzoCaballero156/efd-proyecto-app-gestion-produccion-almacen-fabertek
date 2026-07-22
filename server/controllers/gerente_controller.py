from flask import Blueprint, request, jsonify
from repositories.empleado.empleado_repository import EmpleadoRepository
from services.gerente.gerente_service import GerenteService
from services.empleado.empleado_service import EmpleadoService
from utils.misc import bcrypt

gerente_bp = Blueprint('gerente_bp', __name__)

empleado_repository = EmpleadoRepository()
gerente_service = GerenteService(empleado_repository)
empleado_service = EmpleadoService(empleado_repository)

@gerente_bp.post('/registrar-empleado')
def registrar_empleado():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    email = request.json['email']
    password = request.json['password']
    area = request.json['area']

    if not nombre or not apellido or not email or not password or not area:
        return jsonify({"error": "No autorizado."}), 401
    
    if empleado_repository.exists_by_email(email):
        return jsonify({"error": "El email ya está en uso."}), 401
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    nuevo_empleado = gerente_service.registrar_empleado(nombre, apellido, email, hashed_password, area)

    return jsonify({
        'id': nuevo_empleado.id,
        'nombre': nuevo_empleado.nombre,
        'apellido': nuevo_empleado.apellido,
        'area': nuevo_empleado.detalle.area,
        'email': nuevo_empleado.email,
        'password': password
    }) 

@gerente_bp.put('/empleado/editar/<id>')
def editar_empleado_por_id(id):
    empleado = empleado_service.obtener_empleado_por_id(id)
    if empleado is None:
        return jsonify({"error": "Empleado no existe."}), 404
    
    nombre = request.json['nombre'] or empleado.nombre
    apellido = request.json['apellido'] or empleado.apellido
    password = request.json['password']

    if not password:
        empleado_editado = gerente_service.editar_empleado_por_id(id, nombre, apellido, empleado.password)
    else:
        new_hashed_password = bcrypt.generate_password_hash(password)
        empleado_editado = gerente_service.editar_empleado_por_id(id, nombre, apellido, new_hashed_password)

    return jsonify({
        'id': empleado_editado.id,
        'nombre': empleado_editado.nombre,
        'apellido': empleado_editado.apellido,
        'area': empleado_editado.detalle.area,
        'email': empleado_editado.email,
        'password': empleado_editado.password
    })

@gerente_bp.delete('/empleado/eliminar/<id>')
def eliminar_empleado_por_id(id):
    empleado_existe = empleado_service.obtener_empleado_por_id(id) is not None
    if not empleado_existe:
        return jsonify({"error": "Empleado no existe."}), 404
    
    gerente_service.eliminar_empleado_por_id(id)

    return jsonify({"mensaje": "Usuario eliminado."}), 200