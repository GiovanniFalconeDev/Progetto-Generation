from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography, Geometry

db = SQLAlchemy()

class Edificio(db.Model):
    __tablename__ = 'edificio'
    id = db.Column(db.Integer, primary_key=True)
    posizione = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=False, unique=True)
    perimetro = db.Column(Geometry(geometry_type='POLIGON', srid=4326), nullable=True)
    codice_istat = db.Column(db.String(6), nullable=False)
    data_predisposizione = db.Column(db.Date, nullable=True)
    tipo_edificio = db.Column(db.String(50), nullable= True)
    

class TerminazioneOttica(db.Model):
    __tablename__ = 'terminazione_ottica'
    id = db.Column(db.Integer, primary_key=True)
    id_edificio = db.Column(db.Integer, db.ForeignKey('edificio.id'), nullable=False)
    piano = db.Column(db.String(50), nullable=True)
    scala = db.Column(db.String(50), nullable=True)
    interno = db.Column(db.String(50), nullable=True)
    posizione_dettagliata = db.Column(db.Text, nullable=True)

class Istat(db.Model):
    __tablename__ = 'istat'
    codice_istat = db.Column(db.String(8), primary_key=True, nullable=False)
    denominazione = db.Column(db.String(100), nullable=False)