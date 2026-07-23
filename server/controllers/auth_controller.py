from flask import Blueprint, request, jsonify, session
from repositories.empleado.empleado_repository import EmpleadoRepository
from services.auth.auth_service import AuthService
from utils.misc import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

empleado_repository = EmpleadoRepository()
auth_service = AuthService(empleado_repository)

@auth_bp.get('/@me')
def get_current_session():
    user_id = session.get("user_id")

    if user_id == "admin":
        return jsonify({
            "id": "admin",
            "email": "admin@admin.xyz"
        })

    if user_id is None:
        return jsonify({"error": "No autorizado."}), 401
    
    user = auth_service.cargar_sesion_actual(user_id)

    return jsonify({
        'id': user.id,
        'nombre': user.nombre,
        'apellido': user.apellido,
        'area': user.detalle.area,
        'email': user.email
    })

def create_session(user_id):
    session['user_id'] = user_id
    session.permanent = True
    session.modified = True

@auth_bp.post('/login')
def iniciar_sesion():
    email = request.json['email']
    password = request.json['password']

    if auth_service.es_admin(email, password):
        create_session("admin")
        return jsonify({
            "id": "admin",
            "email": "admin@admin.xyz"
        })

    usuario = auth_service.iniciar_sesion(email)

    if usuario is None or not bcrypt.check_password_hash(usuario.password, password):
        return jsonify({"error": "No autorizado."}), 401

    create_session(usuario.id)

    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "area": usuario.detalle.area,
        "email": usuario.email
    })

@auth_bp.post('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'mensaje': 'Sesión cerrada.'})