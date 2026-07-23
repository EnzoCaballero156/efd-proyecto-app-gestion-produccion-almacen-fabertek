from utils.misc import db, get_uuid

class Material(db.Model):
    __tablename__ = "materiales"

    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    tipo = db.Column(db.String(150))

    inventarios = db.relationship("InventarioArea", back_populates="material", cascade="all, delete-orphan")