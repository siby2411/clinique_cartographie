 # resources/patient_resource.py

from flask import jsonify
from flask_restful import Resource, reqparse
# CORRECT IMPORT: Must be from extensions to break the circular dependency
from extensions import db 
from models.patient import Patient
from geoalchemy2.functions import ST_GeomFromText 

patient_parser = reqparse.RequestParser()
patient_parser.add_argument('nom', type=str, required=True, help="Nom du patient requis", location='json')
patient_parser.add_argument('prenom', type=str, required=True, help="Prénom du patient requis", location='json')
patient_parser.add_argument('date_naissance', type=str, location='json')
patient_parser.add_argument('telephone', type=str, location='json')
patient_parser.add_argument('coords', type=str, help="Coordonnées (latitude,longitude) du domicile", location='json')

class PatientListResource(Resource):
    def get(self):
        patients = Patient.query.all()
        # Ensure that models.patient has the 'coords' property defined for serialization
        return [{'id': p.id, 'nom': p.nom, 'prenom': p.prenom, 'coords': p.coords} for p in patients]

    def post(self):
        args = patient_parser.parse_args()
        
        residence_location = None
        if args['coords']:
            try:
                lat, lon = map(float, args['coords'].split(','))
                wkt_point = f"POINT({lon} {lat})" 
                residence_location = ST_GeomFromText(wkt_point, 4326)
            except ValueError:
                return {'message': 'Format de coordonnées invalide. Utilisez "latitude,longitude"'}, 400

        new_patient = Patient(
            nom=args['nom'],
            prenom=args['prenom'],
            residence_location=residence_location
        )
        
        db.session.add(new_patient)
        db.session.commit()
        return {'message': 'Patient créé', 'id': new_patient.id}, 201

class PatientResource(Resource):
    def get(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        return {'id': patient.id, 'nom': patient.nom, 'prenom': patient.prenom, 'coords': patient.coords}