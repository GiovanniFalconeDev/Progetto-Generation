from app import db
from geoalchemy2 import Geography, Geometry

class Edificio(db.Model):
    __tablename__ = 'edificio'
    id = db.Column(db.Integer, primary_key=True)
    posizione = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=False, unique=True)
    perimetro = db.Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=True)
    codice_istat = db.Column(db.String(6), nullable=False)
    data_predisposizione = db.Column(db.Date, nullable=True)
    tipo_edificio = db.Column(db.String(50), nullable=True)
