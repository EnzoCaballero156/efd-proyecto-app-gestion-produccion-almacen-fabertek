from utils.misc import db, get_uuid

class Area(db.Model):
    __tablename__ = "areas"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    nombre = db.Column(db.String(15), nullable=False)

    empleado = db.relationship("EmpleadoDetalle", back_populates="area", cascade="all, delete-orphan")
    inventario = db.relationship("InventarioArea", back_populates="area", cascade="all, delete-orphan")

    def __iter__(self):
        yield 'id', self.id,
        yield 'nombre', self.nombre