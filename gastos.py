from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from flask import Blueprint, flash, redirect, render_template, request, url_for

import models
from auth import login_required

bp = Blueprint("gastos", __name__)


def validar_gasto(fecha, descripcion, monto_txt):
    """Validación del lado servidor (nunca confiar solo en el navegador)."""
    errores = []

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        errores.append("La fecha no es válida.")

    if not (3 <= len(descripcion) <= 120):
        errores.append("La descripción debe tener entre 3 y 120 caracteres.")

    monto = None
    try:
        monto = Decimal(monto_txt.replace(",", "."))
        if monto <= 0 or monto > Decimal("1000000000"):
            errores.append("El monto debe ser mayor que 0.")
    except (InvalidOperation, AttributeError):
        errores.append("El monto debe ser un número válido.")

    return errores, (round(float(monto), 2) if monto is not None and not errores else None)


@bp.route("/", methods=["GET", "POST"])
@login_required
def registro():
    if request.method == "POST":
        fecha = request.form.get("fecha", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        monto_txt = request.form.get("monto", "").strip()

        errores, monto = validar_gasto(fecha, descripcion, monto_txt)
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            models.crear_gasto(fecha, descripcion, monto)
            flash("Gasto registrado correctamente.", "success")
            return redirect(url_for("gastos.registro"))

    return render_template(
        "registro.html",
        hoy=date.today().isoformat(),
        recientes=models.listar_gastos(limite=5),
        resumen=models.resumen(),
    )


@bp.route("/reportes")
@login_required
def reportes():
    desde = request.args.get("desde", "").strip() or None
    hasta = request.args.get("hasta", "").strip() or None
    return render_template(
        "reportes.html",
        gastos=models.listar_gastos(desde, hasta),
        resumen=models.resumen(desde, hasta),
        desde=desde or "",
        hasta=hasta or "",
    )


@bp.route("/gastos/<int:gasto_id>/eliminar", methods=["POST"])
@login_required
def eliminar(gasto_id):
    models.eliminar_gasto(gasto_id)
    flash("Gasto eliminado.", "success")
    return redirect(url_for("gastos.reportes"))