from utils.misc import db, get_uuid

class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    nombre = db.Column(db.String(70), nullable=False)
    apellido = db.Column(db.String(70), nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    detalle = db.relationship("EmpleadoDetalle", back_populates="empleado", uselist=False, cascade="all, delete-orphan")

class EmpleadoDetalle(db.Model):
    __tablename__ = "empleado_detalle"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    empleado_id = db.Column(db.String(32), db.ForeignKey('empleados.id'), unique=True, nullable=False)
    area = db.Column(db.String(15), nullable=False)

    inventario = db.relationship("InventarioEmpleado", back_populates="empleado", cascade="all, delete-orphan")
    empleado = db.relationship("Empleado", back_populates="detalle")
