# resources/stats_resource.py

from flask_restful import Resource, reqparse
from sqlalchemy import func
# CORRECTION: Importez 'db' depuis 'extensions'
from extensions import db 
from models.centre_sante import CentreSante
from models.departement import Departement
from geoalchemy2.functions import ST_DWithin, ST_GeomFromText, ST_Intersects, ST_AsText


# ==========================================================
# 1. ProximityStatsResource : Chercher les entités proches (ST_DWithin)
# ==========================================================
proximity_parser = reqparse.RequestParser()
proximity_parser.add_argument('lat', type=float, required=True, help="Latitude requise", location='args')
proximity_parser.add_argument('lon', type=float, required=True, help="Longitude requise", location='args')
proximity_parser.add_argument('distance_km', type=int, default=5, help="Distance maximale en km", location='args')

class ProximityStatsResource(Resource):
    """
    Trouve les centres de santé dans une certaine distance (en kilomètres) 
    d'un point donné (latitude, longitude).
    """
    def get(self):
        args = proximity_parser.parse_args()
        
        # 1. Créer le point de référence (le point utilisateur)
        user_point = func.ST_SetSRID(
            func.ST_MakePoint(args['lon'], args['lat']), 
            4326
        )
        
        # 2. Utiliser ST_DWithin: 
        #    ST_DWithin(geometry1, geometry2, distance_meters)
        #    Note: Nous multiplions la distance_km par 1000 pour avoir des mètres
        distance_meters = args['distance_km'] * 1000
        
        # Le champ location dans CentreSante est de type Geography, donc ST_DWithin
        # fonctionne nativement en mètres.
        centres_proches = db.session.query(CentreSante).filter(
            func.ST_DWithin(CentreSante.location, user_point, distance_meters)
        ).all()
        
        results = [{
            'id': c.id, 
            'nom': c.nom, 
            'distance_km': round(db.session.scalar(func.ST_Distance(c.location, user_point)) / 1000, 2)
        } for c in centres_proches]
        
        return {
            'point_reference': f"{args['lat']}, {args['lon']}",
            'distance_max_km': args['distance_km'],
            'centres_trouves': len(results),
            'data': results
        }


# ==========================================================
# 2. DepartmentStatsResource : Statistiques par zone (ST_Contains/ST_Intersects)
# ==========================================================

class DepartmentStatsResource(Resource):
    """
    Retourne le nombre de centres de santé par département.
    Utilise ST_Intersects (ou ST_Contains) pour trouver dans quelle zone (géométrie) se trouve le point.
    """
    def get(self):
        # Jointure implicite: Grouper les centres par le département qui les contient
        # On projette le point (location) en géométrie (ST_GeomFromWKB) pour le comparer avec la géométrie du département.
        
        results = db.session.query(
            Departement.nom,
            func.count(CentreSante.id).label('nombre_centres')
        ).filter(
            # Vérifie si la géométrie du département contient le point du centre
            func.ST_Contains(Departement.geometrie, CentreSante.location)
        ).group_by(Departement.nom).all()
        
        data = [{'departement': nom, 'nombre_centres': count} for nom, count in results]
        
        return {
            'message': 'Statistiques agrégées du nombre de centres de santé par département',
            'data': data
        }