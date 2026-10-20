import os
import sqlite3
from flask import Flask, g

def crear_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "agenda-flask-clave-local"
    app.config["DATABASE"] = os.path.join(app.root_path, "..", "agenda.db")

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
            g.db.execute("""
                CREATE TABLE IF NOT EXISTS actividades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT DEFAULT '',
                    fecha TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Pendiente'
                )
            """)
            g.db.commit()
        return g.db

    @app.teardown_appcontext
    def cerrar_db(error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    # Pone la función disponible para las rutas.
    app.get_db = get_db

    from .routes import bp
    app.register_blueprint(bp)
    return app
