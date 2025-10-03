import os

class Config:
    # Réglages de la base de données pour le cluster commercial (Port 5433)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@127.0.0.1:5433/sante_dakar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clé secrète pour la sécurité des sessions Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_clé_secrète_complexe'