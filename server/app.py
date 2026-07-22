from flask_session import Session
from flask_cors import CORS

from utils.builder import AppBuilder
from utils.misc import db, bcrypt
from config import DevelopmentConfig

from controllers.auth_controller import auth_bp
from controllers.gerente_controller import gerente_bp
from controllers.empleado_controller import empleado_bp
from controllers.material_controller import material_bp

app = (
    AppBuilder()
        .create_app(file=__name__)
        .configure(object=DevelopmentConfig)
        .register_bp(auth_bp, url_prefix='/api/auth')
        .register_bp(gerente_bp, url_prefix='/api/gerente')
        .register_bp(empleado_bp, url_prefix='/api/empleado')
        .register_bp(material_bp, url_prefix='/api/material')
        .build()
)

bcrypt.init_app(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)