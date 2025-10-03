from extensions import db  # Assurez-vous que db est l'instance SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateur' # ou 'users' si vous l'avez nommé ainsi

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='utilisateur') # admin, doctor, utilisateur, etc.

    # --- Fonctions Cruciales pour l'Authentification ---
    
    def set_password(self, password):
        """Hache le mot de passe avant de le stocker."""
        # Ceci utilise le hachage sécurisé de Werkzeug (via Flask-Login)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe soumis contre le hash stocké."""
        return check_password_hash(self.password_hash, password)
    
    # --- Fonctions de Rôle (pour votre logique de redirection) ---

    def is_admin(self):
        return self.role == 'admin'

    def is_doctor(self):
        return self.role == 'doctor'
    
    # Pour Flask-Admin (si vous gérez les permissions)
    @property
    def is_active(self):
        # Pour une application réelle, vérifiez si l'utilisateur est actif
        return True 

    # ... autres champs et méthodes ...