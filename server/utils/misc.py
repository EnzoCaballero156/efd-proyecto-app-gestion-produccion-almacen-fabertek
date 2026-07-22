from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from uuid import uuid4

db = SQLAlchemy()
bcrypt = Bcrypt()

def get_uuid():
    return uuid4().hex