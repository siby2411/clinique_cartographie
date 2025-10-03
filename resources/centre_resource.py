from flask_restful import Resource, reqparse
# CORRECTION: Importez 'db' depuis 'extensions'
from extensions import db 
from models.centre_sante import CentreSante
from geoalchemy2.functions import ST_GeomFromText 
from geoalchemy2.functions import ST_AsGeoJSON # Pour le GeoJSON

centre_parser = reqparse.RequestParser()
centre_parser.add_argument('nom', type=str, required=True, help="Nom du centre requis", location='json')
centre_parser.add_argument('adresse', type=str, location='json')
centre_parser.add_argument('telephone', type=str, location='json')
centre_parser.add_argument('capacite_lits', type=int, location='json')
centre_parser.add_argument('coords', type=str, required=True, help="Coordonnées (lat,lon) sont requises", location='json')


class CentreListResource(Resource):
    def get(self):
        centres = CentreSante.query.all()
        return [{'id': c.id, 'nom': c.nom, 'coords': c.coords} for c in centres]

    def post(self):
        args = centre_parser.parse_args()
        
        # --- LOGIQUE POSTGIS : Conversion des coordonnées en géométrie ---
        try:
            lat, lon = map(float, args['coords'].split(',')) 
            wkt_point = f"POINT({lon} {lat})" 
            location_geom = ST_GeomFromText(wkt_point, 4326) 
            
        except ValueError:
            return {'message': 'Format de coordonnées invalide. Utilisez "latitude,longitude"'}, 400
        
        new_centre = CentreSante(
            nom=args['nom'],
            adresse=args['adresse'],
            telephone=args['telephone'],
            capacite_lits=args['capacite_lits'],
            location=location_geom
        )
        
        db.session.add(new_centre)
        db.session.commit()
        return {'message': 'Centre créé', 'id': new_centre.id}, 201

class CentreResource(Resource):
    def get(self, centre_id):
        centre = CentreSante.query.get_or_404(centre_id)
        return {'id': centre.id, 'nom': centre.nom, 'coords': centre.coords}

class CentreGeoJSONResource(Resource):
    def get(self):
        # Utilise la fonction ST_AsGeoJSON de PostGIS pour générer la sortie
        # Query pour obtenir l'ID et la géométrie convertie en GeoJSON
        centres_data = db.session.query(
            CentreSante.id, 
            CentreSante.nom, 
            ST_AsGeoJSON(CentreSante.location).label('geojson')
        ).all()
        
        features = []
        for id, nom, geojson in centres_data:
            features.append({
                "type": "Feature",
                "geometry": json.loads(geojson),
                "properties": {"id": id, "nom": nom}
            })
            
        return jsonify({
            "type": "FeatureCollection",
            "features": features
        })