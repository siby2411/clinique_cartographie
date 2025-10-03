# models/medecin.py (Assurez-vous que ces champs existent)

from extensions import db

class Medecin(db.Model):
    __tablename__ = 'medecins' # Supposition : votre table se nomme 'medecins'
    id = db.Column(db.Integer, primary_key=True)
    
    # CHAMPS REQUIS POUR LA VUE D'ADMINISTRATION
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False) # <--- Ce champ doit exister
    specialite = db.Column(db.String(100))
    
    # Clé étrangère vers CentreSante (si un médecin est attaché à un centre)
    centre_sante_id = db.Column(db.Integer, db.ForeignKey('centre_sante.id'), nullable=True) 
    centre_sante = db.relationship('CentreSante', backref='medecins')

    def __repr__(self):
        return f'{self.nom} {self.prenom}'