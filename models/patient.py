# models/patient.py (Assurez-vous d'avoir ceci)

from extensions import db
from geoalchemy2 import Geography # Utilisation de Geography pour la localisation

class Patient(db.Model):
    __tablename__ = 'patients' # D'après votre schéma PostgreSQL (public.patients)
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date)
    telephone = db.Column(db.String(20))
    
    # CHAMPS MANQUANT : 'sexe'
    sexe = db.Column(db.String(10)) # Peut être 'Homme', 'Femme', etc.

    # Colonne géospatiale (correspondant à votre schéma 'residence_location')
    # NOTE: Utilisez Geography car c'est ce que votre schéma Postgres utilise.
    residence_location = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True) 

    def __repr__(self):
        return f'{self.nom} {self.prenom}'