from utils.misc import db, get_uuid
from datetime import datetime, timezone

class InventarioMaterial(db.Model):
    __tablename__ = "inventario_material"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)

    empleado_id = db.Column(db.String(32), db.ForeignKey("empleado_detalle.id"), nullable=False)
    material_id = db.Column(db.String(32), db.ForeignKey("materiales.id"), nullable=False)
    
    estado = db.Column(db.String(20))
    cantidad = db.Column(db.Integer, default=0)
    fecha_registro = db.Column(db.Text, default=lambda: datetime.now(timezone.utc).strftime("%d-%m-%Y"))
    hora_registro = db.Column(db.Text, default=lambda: datetime.now(timezone.utc).strftime("%H:%M:%S"))

    empleado = db.relationship("EmpleadoDetalle", back_populates="inventario")
    material = db.relationship("Material", back_populates="inventarios")