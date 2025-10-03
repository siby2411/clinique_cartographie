from sqlalchemy import func, or_, extract, cast
from extensions import db
from models.patient import Patient
from models.consultation import Consultation
from models.centre_sante import CentreSante
from datetime import datetime, timedelta

# IMPORT CRITIQUE pour le casting de géométrie
from geoalchemy2.types import Geometry 

# ==========================================================
# 1. FONCTIONS DE REQUÊTE POUR LA CARTE (GeoJSON)
# ==========================================================

def get_cases_geojson(disease=None):
    """
    Récupère les cas de maladie (patients) et leurs coordonnées géographiques.
    Utilisé par /api/cases.
    """
    
    query = db.session.query(
        Patient.nom,
        Patient.prenom,
        Consultation.diagnostic,
        # Caste la colonne GEOGRAPHY en GEOMETRY pour ST_X/ST_Y
        func.ST_X(cast(Patient.residence_location, Geometry)).label('longitude'),
        func.ST_Y(cast(Patient.residence_location, Geometry)).label('latitude'),
        Consultation.date_consultation
    ).join(Consultation)
    
    if disease:
        query = query.filter(Consultation.diagnostic == disease)
        
    cases = query.all()
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for case in cases:
        # Assurez-vous que les coordonnées sont présentes
        if case.longitude is not None and case.latitude is not None:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    # Longitude, Latitude (X, Y)
                    "coordinates": [case.longitude, case.latitude] 
                },
                "properties": {
                    "patient": f"{case.prenom} {case.nom}",
                    "diagnostic": case.diagnostic,
                    "date": case.date_consultation.strftime('%Y-%m-%d')
                }
            }
            geojson_data['features'].append(feature)
            
    return geojson_data


def get_centres_geojson():
    """
    Récupère les centres de santé et leurs coordonnées géographiques.
    Utilisé par /api/centres/geojson.
    """
    query = db.session.query(
        CentreSante.nom,
        CentreSante.adresse,
        # Caste la colonne GEOGRAPHY en GEOMETRY pour ST_X/ST_Y
        func.ST_X(cast(CentreSante.location, Geometry)).label('longitude'),
        func.ST_Y(cast(CentreSante.location, Geometry)).label('latitude')
    ).all()
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for centre in query:
        # Assurez-vous que les coordonnées sont présentes
        if centre.longitude is not None and centre.latitude is not None:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    # Longitude, Latitude (X, Y)
                    "coordinates": [centre.longitude, centre.latitude] 
                },
                "properties": {
                    "nom": centre.nom,
                    "adresse": centre.adresse,
                    "type": "Centre de Santé"
                }
            }
            geojson_data['features'].append(feature)
            
    return geojson_data


# ==========================================================
# 2. FONCTIONS D'ANALYSE ÉPIDÉMIOLOGIQUE (KPIs)
# ==========================================================

def get_kpis():
    """Récupère les indicateurs clés de performance pour le tableau de bord."""
    
    # 1. Total Patients
    total_patients = db.session.query(Patient).count()
    
    # 2. Total Consultations
    total_consultations = db.session.query(Consultation).count()

    # 3. Cas par Diagnostic (Agrégation)
    cases_by_disease = db.session.query(
        Consultation.diagnostic,
        func.count(Consultation.id).label('count')
    ).group_by(Consultation.diagnostic).order_by('count').all()
    
    # 4. Cas récents (ex: 30 derniers jours)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_cases = db.session.query(Consultation).filter(
        Consultation.date_consultation >= thirty_days_ago
    ).count()

    # 5. Cas par Centre de Santé
    cases_by_center = db.session.query(
        CentreSante.nom,
        func.count(Consultation.id).label('count')
    ).join(Consultation).group_by(CentreSante.nom).all()
    
    return {
        'total_patients': total_patients,
        'total_consultations': total_consultations,
        'recent_cases_30d': recent_cases,
        'cases_by_disease': {diag: count for diag, count in cases_by_disease},
        'cases_by_center': {center: count for center, count in cases_by_center} 
    }

# ==========================================================
# 3. FONCTIONS POUR GRAPHIQUES (CHART.JS)
# ==========================================================

def get_centres_par_departement():
    """
    Récupère le nombre de centres de santé par département.
    Utilisé par l'API /api/stats/departements pour les graphiques.
    """
    # NOTE: Cette requête suppose que votre modèle CentreSante a une relation avec Departement
    result = db.session.query(
        Departement.nom.label('departement'),
        func.count(CentreSante.id).label('nombre_centres')
    ).join(CentreSante).group_by(Departement.nom).all()
    
    # Formatage pour l'API
    return {
        "data": [
            {"departement": r.departement, "nombre_centres": r.nombre_centres}
            for r in result
        ]
    }