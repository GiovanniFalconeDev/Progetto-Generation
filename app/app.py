from flask import Flask, redirect, request,json
from __init__ import db
from routes.edificio_routes import edificio_blueprint
from routes.terminazione_ottica_routes import terminazione_ottica_blueprint
from sqlalchemy import text
from shapely import wkb


def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    # Registrazione dei Blueprint
    app.register_blueprint(edificio_blueprint, url_prefix='/edifici')
    app.register_blueprint(terminazione_ottica_blueprint, url_prefix='/tfo')


    @app.route("/", methods=['GET'])
    def visualizzaedifici():
        return redirect('/edifici')
    


    
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
        result = db.session.execute(query)
 
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
        #     "codice_istat": row[3]} for row in result]

        result2 = {"type": "FeatureCollection", "features": edifici_json}  
        json_response = json.dumps(result2, indent=4)
        return json_response  # Restituisce al browser

    return app
