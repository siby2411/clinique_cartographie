# models/centre_sante.py (Assurez-vous d'avoir ceci)

from extensions import db
from geoalchemy2 import Geometry

class CentreSante(db.Model):
    __tablename__ = 'centre_sante'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.String(255))
    capacite_lits = db.Column(db.Integer)
    
    # Clé étrangère vers la table departement
    departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'), nullable=False)
    
    # Relation SQLAlchemy
    departement = db.relationship('Departement', backref='centres') 
    
    # Colonne geospatiale (Geography pour une meilleure précision)
    location = db.Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=True) 

    def __repr__(self):
        return self.nom