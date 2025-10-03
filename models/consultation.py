# models/consultation.py (Version Finale Corrigée)

from extensions import db
from datetime import datetime
from geoalchemy2 import Geometry # Importation nécessaire pour la colonne de géométrie

class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True)
    date_consultation = db.Column(db.DateTime, default=datetime.utcnow)
    diagnostic = db.Column(db.Text)
    resultat_examen = db.Column(db.Text)

    # Clés étrangères
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('medecins.id'), nullable=False)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres_sante.id'), nullable=False)

    # NOUVEAU : Colonne de géométrie du patient (conforme au \d consultations)
    geom_patient_location = db.Column(
        Geometry(geometry_type='POINT', srid=4326),
        nullable=True
    )

    # Relations
    patient = db.relationship('Patient', backref=db.backref('consultations', lazy=True))
    medecin = db.relationship('Medecin', backref=db.backref('consultations', lazy=True))
    # centre (backref déjà défini dans models/centre_sante.py)

    def __repr__(self):
        return f"<Consultation {self.patient_id} - {self.date_consultation.strftime('%Y-%m-%d')}>"