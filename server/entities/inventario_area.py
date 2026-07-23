from utils.misc import db, get_uuid
from datetime import datetime, timezone

class InventarioArea(db.Model):
    __tablename__ = "inventario_area"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)

    area_id = db.Column(db.String(32), db.ForeignKey("areas.id"), nullable=False)
    material_id = db.Column(db.String(32), db.ForeignKey("materiales.id"), nullable=False)
    
    estado = db.Column(db.String(20))
    cantidad = db.Column(db.Integer, default=0)
    fecha_registro = db.Column(db.Text, default=lambda: datetime.now(timezone.utc).strftime("%d-%m-%Y"))
    hora_registro = db.Column(db.Text, default=lambda: datetime.now(timezone.utc).strftime("%H:%M:%S"))

    area = db.relationship("Area", back_populates="inventario")
    material = db.relationship("Material", back_populates="inventarios")