from datetime import date
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

bp = Blueprint("agenda", __name__)

def db():
    return current_app.get_db()

@bp.route("/")
def inicio():
    busqueda = request.args.get("q", "").strip()
    estado = request.args.get("estado", "").strip()
    sql = "SELECT * FROM actividades WHERE 1=1"
    params = []
    if busqueda:
        sql += " AND (titulo LIKE ? OR descripcion LIKE ?)"
        params.extend([f"%{busqueda}%", f"%{busqueda}%"])
    if estado in ("Pendiente", "Completada"):
        sql += " AND estado = ?"
        params.append(estado)
    sql += " ORDER BY fecha ASC, id DESC"
    actividades = db().execute(sql, params).fetchall()
    total = db().execute("SELECT COUNT(*) FROM actividades").fetchone()[0]
    completadas = db().execute(
        "SELECT COUNT(*) FROM actividades WHERE estado = 'Completada'"
    ).fetchone()[0]
    return render_template(
        "index.html", actividades=actividades, hoy=date.today().isoformat(),
        q=busqueda, estado=estado, total=total, completadas=completadas
    )

@bp.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    fecha = request.form.get("fecha", "").strip()
    if not titulo or not fecha:
        flash("El título y la fecha son obligatorios.", "error")
        return redirect(url_for("agenda.inicio"))
    db().execute(
        "INSERT INTO actividades (titulo, descripcion, fecha) VALUES (?, ?, ?)",
        (titulo, descripcion, fecha)
    )
    db().commit()
    flash("Actividad agregada correctamente.", "success")
    return redirect(url_for("agenda.inicio"))

@bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    actividad = db().execute("SELECT * FROM actividades WHERE id = ?", (id,)).fetchone()
    if actividad is None:
        flash("No se encontró esa actividad.", "error")
        return redirect(url_for("agenda.inicio"))
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        fecha = request.form.get("fecha", "").strip()
        estado = request.form.get("estado", "Pendiente")
        if not titulo or not fecha:
            flash("El título y la fecha son obligatorios.", "error")
            return render_template("edit.html", actividad=actividad)
        if estado not in ("Pendiente", "Completada"):
            estado = "Pendiente"
        db().execute(
            """UPDATE actividades
               SET titulo = ?, descripcion = ?, fecha = ?, estado = ?
               WHERE id = ?""",
            (titulo, descripcion, fecha, estado, id)
        )
        db().commit()
        flash("Cambios guardados.", "success")
        return redirect(url_for("agenda.inicio"))
    return render_template("edit.html", actividad=actividad)

@bp.route("/completar/<int:id>", methods=["POST"])
def completar(id):
    actividad = db().execute("SELECT estado FROM actividades WHERE id = ?", (id,)).fetchone()
    if actividad:
        nuevo = "Pendiente" if actividad["estado"] == "Completada" else "Completada"
        db().execute("UPDATE actividades SET estado = ? WHERE id = ?", (nuevo, id))
        db().commit()
        flash("Estado actualizado.", "success")
    return redirect(url_for("agenda.inicio"))

@bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    db().execute("DELETE FROM actividades WHERE id = ?", (id,))
    db().commit()
    flash("Actividad eliminada.", "success")
    return redirect(url_for("agenda.inicio"))
