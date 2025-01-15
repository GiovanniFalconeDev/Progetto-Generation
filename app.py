from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import models
from sqlalchemy import text, update
import json
from shapely import wkb
from config import endpoint

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = endpoint

#collegamento tra database e app variabile alla riga 4
models.db.init_app(app)

#creare la tabella
with app.app_context():
   models.db.create_all()

@app.route("/", methods=['GET'])
def visualizzaedifici():
   return render_template('registrazione_edifici.html')

@app.route("/tfo", methods=['GET'])
def visualizzatfo():
   return render_template('tfo.html')


# @app.route("/send", methods=['POST'])
# def aggiungiedificio():
#     # edificio = models.Edificio(id=request.form["id"], posizione=request.form["posizione"], perimetro=request.form["perimetro"], codice_istat=request.form["codice_istat"])
#     data = request.get_json() 
#     print(data)
#     edificio = models.Edificio(
#         posizione = f"POINT ({data['latitudine']} {data['longitudine']})",
#         tipo_edificio = data["tipoEdificio"],
#         data_predisposizione=data["dataPredisposizione"]
#     )
#     print(edificio)
    
#     # models.db.session.add(edificio)
#     # models.db.session.commit()
#     return redirect(url_for("visualizzaedifici"))

@app.route("/send", methods=['POST'])
def aggiungiedificio():
    # Ottieni i dati JSON dalla richiesta
    edifici_data = request.get_json()
    # Aggiungi gli edifici al database
    for data in edifici_data:
        pos = f"POINT ({data['latitudine']} {data['longitudine']})"
        # edificio = models.Edificio(id=request.form["id"], posizione=request.form["posizione"], perimetro=request.form["perimetro"], codice_istat=request.form["codice_istat"])
        edificio = models.Edificio(
            tipo_edificio = data["tipoEdificio"],
            data_predisposizione=data["dataPredisposizione"]
        )
        print(edificio)
        print(pos)
    
        select = models.db.session.query(models.Edificio).filter(models.Edificio.id == data["id"]).all()
        if select:
            edificio = select[0]
            edificio.tipo_edificio = data["tipoEdificio"]
            edificio.data_predisposizione = data["dataPredisposizione"]
            models.db.session.commit()
        else:
            print("data non inserita")


    # upd = update()
    # val = upd.values({"column_name":"value"})
    # cond = val.where(tablename.c.column_name == value)

    #     models.db.session.add(edificio)
    # # Commit delle modifiche al database
    # models.db.session.commit()
    # # Redirect alla visualizzazione degli edifici
    return jsonify({"data":None, "status":200, "message": "successfully"})


@app.route("/delete", methods=['POST'])
def cancellaedificio():
    data = request.get_json()  # Accedi ai dati JSON inviati nella richiesta
    
    # Cerca l'edificio direttamente usando l'ID passato
    edificio = models.Edificio.query.get(data.get("id"))
    
    if edificio:
        # Se l'edificio esiste, cancellalo
        models.db.session.delete(edificio)
        models.db.session.commit()
        return "Edificio cancellato con successo"
    else:
        # Se l'edificio non esiste o l'ID non è valido
        return "Edificio non trovato"

@app.route("/query_bounding_box", methods=['GET'])
def query_bounding_box():
    # Ottieni i parametri dal frontend (se applicabile)
    latitude = request.args.get("latitudine")  # Default latitudine
    longitude = request.args.get("longitudine")  # Default longitudine
    print(latitude)

    query = text(f"""SELECT * FROM public.edificio
WHERE posizione::geometry && ST_MakeEnvelope(
{float(longitude)+0.001},
{float(latitude)+0.001},
{float(longitude)-0.001},
{float(latitude)-0.001},
4326
)""")
    result = models.db.session.execute(query)

    # edifici_json = [{
    #     "id":row[0],
    #     "posizione": {
    #         "type" : "Point",
    #         "coordinates": [wkb.loads(bytes.fromhex(row[1])).x, wkb.loads(bytes.fromhex(row[1])).y]},
    #     "perimetro": {
    #         "type": "Polygon", 
    #         "coordinates": [[x,y] for x, y in wkb.loads(bytes.fromhex(row[2])).exterior.coords]},
    #     "disponibilita": (True if row[4] is not None else False), 
    #     "codice_istat": row[3]} for row in result]
    edifici_json = [{
        "type": "Feature",
        "properties": {
            "id": row[0],
            "centroide": [wkb.loads(bytes.fromhex(row[1])).x, wkb.loads(bytes.fromhex(row[1])).y],
            "disponibilita": (True if row[4] is not None else False)
        },
        "geometry": {
            "type": "Polygon", 
            "coordinates": [[[(x if isinstance (x,float) else 0),(y if isinstance (y,float) else 0)] for x, y in wkb.loads(bytes.fromhex(row[2])).exterior.coords]]}
        
        } for row in result]

    result2 = {"type": "FeatureCollection", "features": edifici_json}
    # geometry = wkb.loads(bytes.fromhex(wkb_value)) # Estrarre latitudine e longitudine longitude, latitude = geometry.x, geometry.y print(f"Longitudine: {longitude}, Latitudine: {latitude}")
    # names = [f"POINT({}); ".join(str(e) for e in row ) for row in result]

    # Converti i risultati in formato JSON
    # edifici_json = [
    #     {
    #         "id": edificio.id,
    #         "posizione": {
    #             "type": "Point",
    #             "coordinates": [edificio.posizione.x, edificio.posizione.y]
    #         },
    #         "codice_istat": edificio.codice_istat
    #     }
    #     for edificio in results
    # ]

    json_response = json.dumps(result2, indent=4)
    return json_response  # Restituisce al browser

@app.route("/add_tfo", methods=['POST'])
def aggiungiTFO():
    # Ottieni i dati JSON dalla richiesta
    TFO_data = request.get_json()
    # Aggiungi gli edifici al database
    for data in TFO_data:
        # edificio = models.Edificio(id=request.form["id"], posizione=request.form["posizione"], perimetro=request.form["perimetro"], codice_istat=request.form["codice_istat"])
        TFO = models.TerminazioneOttica(
            id_edificio = data['id'],
            piano = data['piano'],
            scala = data['scala'],
            interno = data['interno'],
            posizione_dettagliata = data['posizioned']
        )
    
        models.db.session.add(TFO)
        models.db.session.commit()
        return jsonify({"message": "TFO aggiunto con successo."}), 201


    # upd = update()
    # val = upd.values({"column_name":"value"})
    # cond = val.where(tablename.c.column_name == value)

    #     models.db.session.add(edificio)
    # # Commit delle modifiche al database
    # models.db.session.commit()
    # # Redirect alla visualizzazione degli edifici
    


#flask --app app run --debug