from flask import Blueprint, request, jsonify
from models.terminazione_ottica import TerminazioneOttica
from app import db
from flask import render_template

terminazione_ottica_blueprint = Blueprint('terminazione_ottica', __name__)

@terminazione_ottica_blueprint.route("/", methods=['GET'])
def visualizzatfo():
    return render_template('tfo.html')


@terminazione_ottica_blueprint.route("/add_tfo", methods=['POST'])
def aggiungiTFO():
    TFO_data = request.get_json()
    for data in TFO_data:
        TFO = TerminazioneOttica(
            id_edificio=data['id'],
            piano=data['piano'],
            scala=data['scala'],
            interno=data['interno'],
            posizione_dettagliata=data['posizioned']
        )
        db.session.add(TFO)
        db.session.commit()
    return jsonify({"message": "TFO aggiunto con successo."}), 201
