# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import spacy

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Crear la instancia de la aplicación Flask
    app = Flask(__name__)
    
    # Cargar configuraciones
    app.config.from_object('config.Config')
    
    # Inicializar SQLAlchemy con la aplicación
    db.init_app(app)
    
    # Importar y registrar las rutas
    with app.app_context():
        from app.routes import setup_routes
        setup_routes(app)
    
    # Cargar el modelo de lenguaje en español
    global nlp
    nlp = spacy.load("es_core_news_sm")

    return app


