import hmac
from functools import wraps
from flask import (Blueprint, current_app, flash, redirect,
                   render_template, request, session, url_for)

bp = Blueprint("auth", __name__)


def login_required(vista):
    """Protege rutas: sin sesión activa, redirige al login."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            flash("Inicia sesión para continuar.", "error")
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)
    return envoltura


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("gastos.registro"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "")
        cfg = current_app.config

        # Comparación en tiempo constante
        ok_user = hmac.compare_digest(usuario, cfg["ADMIN_USER"])
        ok_pass = hmac.compare_digest(clave, cfg["ADMIN_PASSWORD"])

        if ok_user and ok_pass:
            session.clear()
            session["usuario"] = usuario
            flash("Bienvenido de nuevo.", "success")
            return redirect(url_for("gastos.registro"))
        flash("Usuario o clave incorrectos.", "error")

    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))