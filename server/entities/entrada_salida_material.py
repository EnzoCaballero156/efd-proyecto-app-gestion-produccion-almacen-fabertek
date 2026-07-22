from utils.misc import db, get_uuid
from datetime import datetime, timezone

class EntradaSalidaMaterial(db.Model):
    __tablename__ = "entrada_salida_material"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    area = db.Column(db.String(15))
    tipo_material = db.Column(db.String(150))
    entrada_material = db.Column(db.Text, default=lambda: datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"))
    salida_material = db.Column(db.Text, default="")