from app import db, create_app
from sqlalchemy import text  # Importar text() para manejar expresiones SQL textuales

# Crear la aplicación y empujar el contexto de aplicación
app = create_app()

# Usar el contexto de la aplicación para las operaciones de base de datos
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("La conexión con la base de datos es exitosa.")
    except Exception as e:
        print(f"Error en la conexión con la base de datos: {e}")