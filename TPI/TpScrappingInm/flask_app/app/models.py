from app import db

class Inmueble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Cambiado de String a Float
    location = db.Column(db.String(100), nullable=False)
    ambientes = db.Column(db.Integer, nullable=False)
    banos = db.Column(db.Integer, nullable=False)
    metros_cuadrados = db.Column(db.Float, nullable=False)
    link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Inmueble {self.title}>'
