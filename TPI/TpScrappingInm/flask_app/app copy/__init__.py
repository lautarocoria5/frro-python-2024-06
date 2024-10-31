# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Asegúrate de importar Migrate
import spacy

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()  # Crear la instancia de Migrate

def create_app():
    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)
    
    # Cargar configuraciones
    app.config.from_object('config.Config')
    
    # Inicializar SQLAlchemy y Flask-Migrate con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)  # Inicializa Migrate aquí
    
    # Importar y registrar las rutas
    with app.app_context():
        from app.routes import setup_routes
        setup_routes(app)
    
    # Cargar el modelo de lenguaje en español
    global nlp
    nlp = spacy.load("es_core_news_sm")

    return app

