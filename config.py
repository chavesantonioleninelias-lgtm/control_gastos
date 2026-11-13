import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-dev-cambiar-en-produccion")
    DATABASE = os.path.join(BASE_DIR, "gastos.db")

    # Credenciales fijas exigidas por la práctica
    ADMIN_USER = "admin"
    ADMIN_PASSWORD = "123"

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"