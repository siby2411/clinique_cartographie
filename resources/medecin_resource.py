 # resources/medecin_resource.py

from flask_restful import Resource, reqparse
# CORRECT IMPORT: Must be from extensions to break the circular dependency
from extensions import db 
from models.medecin import Medecin
from models.centre_sante import CentreSante # Needed for foreign key check

medecin_parser = reqparse.RequestParser()
medecin_parser.add_argument('nom', type=str, required=True, help="Nom du médecin requis", location='json')
medecin_parser.add_argument('specialite', type=str, location='json')
medecin_parser.add_argument('telephone', type=str, location='json')
medecin_parser.add_argument('centre_id', type=int, required=True, help="ID du centre de santé requis", location='json')

class MedecinListResource(Resource):
    def get(self):
        medecins = Medecin.query.all()
        return [{
            'id': m.id, 
            'nom': m.nom, 
            'specialite': m.specialite, 
            'centre_id': m.centre_id
        } for m in medecins]

    def post(self):
        args = medecin_parser.parse_args()

        # Simple validation for centre_id existence
        if not CentreSante.query.get(args['centre_id']):
            return {'message': f"Centre de santé avec l'ID {args['centre_id']} non trouvé."}, 404

        new_medecin = Medecin(
            nom=args['nom'],
            specialite=args['specialite'],
            telephone=args['telephone'],
            centre_id=args['centre_id']
        )
        
        db.session.add(new_medecin)
        db.session.commit()
        return {'message': 'Médecin créé', 'id': new_medecin.id}, 201

class MedecinResource(Resource):
    def get(self, medecin_id):
        medecin = Medecin.query.get_or_404(medecin_id)
        return {
            'id': medecin.id, 
            'nom': medecin.nom, 
            'specialite': medecin.specialite, 
            'telephone': medecin.telephone,
            'centre_id': medecin.centre_id
        }
    
    # You would add PUT/DELETE methods here if needed