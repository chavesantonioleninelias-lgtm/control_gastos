import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS gastos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha       TEXT    NOT NULL,              -- formato ISO: YYYY-MM-DD
            descripcion TEXT    NOT NULL,
            monto       REAL    NOT NULL CHECK (monto > 0),
            creado_en   TEXT    DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()


def crear_gasto(fecha, descripcion, monto):
    db = get_db()
    db.execute(
        "INSERT INTO gastos (fecha, descripcion, monto) VALUES (?, ?, ?)",
        (fecha, descripcion, monto),
    )
    db.commit()


def listar_gastos(desde=None, hasta=None, limite=None):
    query = "SELECT * FROM gastos WHERE 1=1"
    params = []
    if desde:
        query += " AND fecha >= ?"
        params.append(desde)
    if hasta:
        query += " AND fecha <= ?"
        params.append(hasta)
    query += " ORDER BY fecha DESC, id DESC"
    if limite:
        query += " LIMIT ?"
        params.append(limite)
    return get_db().execute(query, params).fetchall()


def resumen(desde=None, hasta=None):
    query = "SELECT COUNT(*) AS cantidad, COALESCE(SUM(monto), 0) AS total FROM gastos WHERE 1=1"
    params = []
    if desde:
        query += " AND fecha >= ?"
        params.append(desde)
    if hasta:
        query += " AND fecha <= ?"
        params.append(hasta)
    fila = get_db().execute(query, params).fetchone()
    promedio = fila["total"] / fila["cantidad"] if fila["cantidad"] else 0
    return {"cantidad": fila["cantidad"], "total": fila["total"], "promedio": promedio}


def eliminar_gasto(gasto_id):
    db = get_db()
    db.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
    db.commit()