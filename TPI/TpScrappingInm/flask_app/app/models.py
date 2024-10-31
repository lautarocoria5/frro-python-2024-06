from app import db

class Inmueble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True, default=0)  # Cambiado de String a Float
    location = db.Column(db.String(255), nullable=True)
    ambientes = db.Column(db.Integer, nullable=True)
    banos = db.Column(db.Integer, nullable=True)
    metros_cuadrados = db.Column(db.Float, nullable=True)
    link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Inmueble {self.title}>'
