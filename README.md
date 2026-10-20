# Agenda de Actividades — Flask + SQLite

Aplicación escolar para registrar, consultar, editar y eliminar actividades.

## 1. Requisitos
- Python 3.10 o superior
- pip

## 2. Instalar
Abre una terminal dentro de esta carpeta y ejecuta:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Instala Flask:
```bash
pip install -r requirements.txt
```

## 3. Ejecutar
```bash
python run.py
```

Abre en el navegador: http://127.0.0.1:5000

La base de datos `agenda.db` se crea automáticamente al iniciar la aplicación por primera vez.

## Funciones
- Agregar actividades con título, descripción y fecha.
- Ver todas las actividades en una tabla.
- Editar título, descripción, fecha y estado.
- Marcar actividades como pendientes o completadas.
- Eliminar actividades con confirmación.
- Filtrar por estado y buscar por título o descripción.

## Estructura
```text
Agenda_Flask/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── edit.html
│   └── static/
│       └── style.css
├── run.py
├── requirements.txt
└── README.md
```
