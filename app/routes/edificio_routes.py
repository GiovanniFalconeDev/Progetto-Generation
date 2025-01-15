from flask import Blueprint, request, render_template, jsonify,json
from models.edificio import Edificio
from app import db
from sqlalchemy import text
from shapely import wkb

edificio_blueprint = Blueprint('edificio', __name__)

@edificio_blueprint.route("/", methods=['GET'])
def visualizzaedifici():
    return render_template('registrazione_edifici.html')

@edificio_blueprint.route("/send", methods=['POST'])
def aggiungiedificio():
    edifici_data = request.get_json()
    for data in edifici_data:
        pos = f"POINT ({data['latitudine']} {data['longitudine']})"
        edificio = Edificio(
            tipo_edificio=data["tipoEdificio"],
            data_predisposizione=data["dataPredisposizione"]
        )
        select = db.session.query(Edificio).filter(Edificio.id == data["id"]).all()
        if select:
            edificio = select[0]
            edificio.tipo_edificio = data["tipoEdificio"]
            edificio.data_predisposizione = data["dataPredisposizione"]
            db.session.commit()
        else:
            print("data non inserita")
    return jsonify({"data": None, "status": 200, "message": "successfully"})


@edificio_blueprint.route("/query_bounding_box", methods=['GET'])
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
    result = Edificio.db.session.execute(query)

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