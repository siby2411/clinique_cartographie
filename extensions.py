from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager # Importé pour la gestion des sessions

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Admin with a custom index view 
# NOTE: L'objet AdminIndexView sera remplacé par la classe CustomAdminIndexView définie dans admin_views.py 
# pour implémenter la vérification des rôles (admin/doctor).
# Nous n'avons pas besoin de définir la CustomAdminIndexView simple ici.
admin = Admin(name='Santé Dakar Géo', template_mode='bootstrap3')

# Initialize Flask-Login
login_manager = LoginManager() 

# Définition de la fonction de chargement d'utilisateur
# (Sera initialisée dans app.py après l'import du modèle Utilisateur) 