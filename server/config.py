from dotenv import load_dotenv
import os
import redis

load_dotenv()

# ruta base de config.py
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "wafu981r98147y45hf91")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = fr"sqlite:///{os.path.join(base_dir, "db.sqlite")}"
    SQLALCHEMY_ECHO = True

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379?protocol=2")
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = False

    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_SECURE = True