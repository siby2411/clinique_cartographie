# models/departement.py (Vérifiez le nom de la table)

from extensions import db

class Departement(db.Model):
    # CORRECTION CRITIQUE : Assurez-vous que le nom de la table est AU SINGULIER
    # Si votre table dans PostgreSQL est nommée "departement" (sans 's'):
    __tablename__ = 'departement' 
    
    # Si votre table dans PostgreSQL est nommée "departements" (avec 's'):
    # __tablename__ = 'departements' # D'après l'erreur, c'est le cas

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    
    # ... autres colonnes ...