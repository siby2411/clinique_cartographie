# resources/consultation_resource.py

from flask_restful import Resource, reqparse
# CORRECTION: Use extensions to break the circular dependency!
from extensions import db 
from models.consultation import Consultation
from models.patient import Patient
from models.medecin import Medecin
from models.centre_sante import CentreSante
from datetime import datetime

consultation_parser = reqparse.RequestParser()
consultation_parser.add_argument('patient_id', type=int, required=True, location='json')
consultation_parser.add_argument('medecin_id', type=int, required=True, location='json')
consultation_parser.add_argument('centre_id', type=int, required=True, location='json')
consultation_parser.add_argument('diagnostic', type=str, location='json')
consultation_parser.add_argument('resultat_examen', type=str, location='json')
# Note: date_consultation uses a default datetime.utcnow, so it's not strictly required in POST

class ConsultationListResource(Resource):
    def get(self):
        consultations = Consultation.query.all()
        return [{
            'id': c.id, 
            'date': c.date_consultation.isoformat(),
            'patient_id': c.patient_id,
            'medecin_id': c.medecin_id
        } for c in consultations]

    def post(self):
        args = consultation_parser.parse_args()

        # Basic validation for existence of foreign keys
        if not Patient.query.get(args['patient_id']):
            return {'message': f"Patient ID {args['patient_id']} non trouvé."}, 404
        if not Medecin.query.get(args['medecin_id']):
            return {'message': f"Médecin ID {args['medecin_id']} non trouvé."}, 404
        if not CentreSante.query.get(args['centre_id']):
            return {'message': f"Centre ID {args['centre_id']} non trouvé."}, 404

        new_consultation = Consultation(
            patient_id=args['patient_id'],
            medecin_id=args['medecin_id'],
            centre_id=args['centre_id'],
            diagnostic=args['diagnostic'],
            resultat_examen=args['resultat_examen']
        )
        
        db.session.add(new_consultation)
        db.session.commit()
        return {'message': 'Consultation créée', 'id': new_consultation.id}, 201

class ConsultationResource(Resource):
    def get(self, consultation_id):
        consultation = Consultation.query.get_or_404(consultation_id)
        return {
            'id': consultation.id, 
            'date': consultation.date_consultation.isoformat(),
            'patient_id': consultation.patient_id,
            'diagnostic': consultation.diagnostic
        }