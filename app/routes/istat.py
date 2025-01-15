from app import db

class Istat(db.Model):
    __tablename__ = 'istat'
    codice_istat = db.Column(db.String(6), primary_key=True, nullable=False)
    denominazione = db.Column(db.String(100), nullable=False)
