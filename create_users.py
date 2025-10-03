# create_users.py

from app import app, db
from models.utilisateur import Utilisateur

# Utilisateurs à créer : (email, mot_de_passe, role)
USERS_TO_CREATE = [
    ('admin@sante.sn', 'secure_admin_pass', 'admin'),
    ('dr.fall@sante.sn', 'secure_doctor_pass', 'doctor'),
]

def create_initial_users():
    """Crée les utilisateurs admin et doctor dans la BDD."""
    with app.app_context():
        # Assurez-vous que la table Utilisateur est créée (si ce n'est pas déjà fait)
        db.create_all() 
        
        print("--- Création des utilisateurs initiaux ---")

        for email, password, role in USERS_TO_CREATE:
            user = Utilisateur.query.filter_by(email=email).first()
            if not user:
                new_user = Utilisateur(email=email, role=role)
                new_user.set_password(password) # Le mot de passe est haché ici
                db.session.add(new_user)
                print(f"✅ Utilisateur '{email}' créé avec le rôle '{role}'.")
            else:
                print(f"⚠️ Utilisateur '{email}' existe déjà.")

        db.session.commit()
        print("--- Opération terminée. ---")

if __name__ == '__main__':
    create_initial_users()