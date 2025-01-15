from app import db

class TerminazioneOttica(db.Model):
    __tablename__ = 'terminazione_ottica'
    id = db.Column(db.Integer, primary_key=True)
    id_edificio = db.Column(db.Integer, db.ForeignKey('edificio.id'), nullable=False)
    piano = db.Column(db.String(50), nullable=True)
    scala = db.Column(db.String(50), nullable=True)
    interno = db.Column(db.String(50), nullable=True)
    posizione_dettagliata = db.Column(db.Text, nullable=True)
