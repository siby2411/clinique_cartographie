from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from config import Config
from extensions import db, admin, login_manager # Assurez-vous d'importer login_manager
from werkzeug.utils import redirect

# Importation pour l'authentification
from flask_login import login_user, logout_user, login_required, current_user 
from forms import LoginForm # Assurez-vous que ce fichier existe
from models.utilisateur import Utilisateur # Assurez-vous que ce fichier existe et est correct

# Importez vos modèles et vues d'administration
from models.patient import Patient
from models.centre_sante import CentreSante
from models.medecin import Medecin
from models.consultation import Consultation
from models.departement import Departement

from admin_views import (
    PatientAdminView, CentreSanteAdminView, MedecinAdminView,
    ConsultationAdminView, DepartmentAdminView, CustomAdminIndexView # Importez la vue d'index personnalisée
)
from analytics import get_cases_geojson, get_kpis, get_centres_geojson 

# ==========================================================
# INITIALISATION DE L'APPLICATION
# ==========================================================
app = Flask(__name__)
app.config.from_object(Config)

# ------------------------------------------------------------------
# LIAISON DES EXTENSIONS À L'APPLICATION (init_app)
# ------------------------------------------------------------------
with app.app_context():
    db.init_app(app)  
    
    # 1. Configuration de l'objet 'admin' avec la vue d'index personnalisée
    # ATTENTION : On modifie l'objet existant au lieu de le réaffecter
   # Ligne corrigée dans app.py :
    admin._set_admin_index_view(CustomAdminIndexView(name='Accueil Admin', url='/admin'))
    admin.init_app(app)

    # 2. Initialisation de Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'login' # La vue de connexion sera 'login'


# Fonction requise par Flask-Login pour charger l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    # Assurez-vous que le modèle Utilisateur est importé
    return db.session.get(Utilisateur, int(user_id))

# ==========================================================
# CONFIGURATION FLASK-ADMIN
# ==========================================================
# Les vues doivent utiliser les classes de CustomModelView dans admin_views.py pour la protection par rôles
admin.add_view(DepartmentAdminView(Departement, db.session, name='Départements'))
admin.add_view(CentreSanteAdminView(CentreSante, db.session, name='Centres de Santé'))
admin.add_view(MedecinAdminView(Medecin, db.session, name='Médecins'))
admin.add_view(PatientAdminView(Patient, db.session, name='Patients'))
admin.add_view(ConsultationAdminView(Consultation, db.session, name='Consultations'))

# ==========================================================
# ROUTES D'AUTHENTIFICATION ET D'ADMINISTRATION PROTÉGÉE
# ==========================================================

 

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route de connexion avec gestion des rôles et redirections."""
    
    # 1. Vérification si l'utilisateur est déjà connecté
    if current_user.is_authenticated:
        # Redirection vers l'index principal si déjà authentifié
        return redirect(url_for('main_index'))

    form = LoginForm()

    # 2. Traitement du formulaire de connexion
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(email=form.email.data).first()
        
        # --- Début de la Vérification du Mot de Passe ---
        if user and user.check_password(form.password.data):
            
            # --- DEBUGGING : Afficher le rôle et le résultat de la fonction de rôle ---
            print(">>> SUCCÈS : Connexion utilisateur réussie ! <<<")
            print(f"DEBUG: Rôle de l'utilisateur trouvé: '{user.role}'")
            # Assurez-vous que les méthodes is_admin/is_doctor existent dans le modèle Utilisateur
            print(f"DEBUG: user.is_admin() résultat: {user.is_admin()}") 
            print(f"DEBUG: user.is_doctor() résultat: {user.is_doctor()}") 
            # --------------------------------------------------------------------------
            
            login_user(user)
            
            # Récupération de la page demandée initialement
            next_page = request.args.get('next')
            
            # Redirection basée sur le rôle utilisateur (Utilisation des méthodes is_role)
            if user.is_admin():
                # Redirection vers la vue d'index d'administration
                return redirect(next_page or url_for('admin.index'))
                
            elif user.is_doctor():
                # Redirection vers le tableau de bord du médecin
                return redirect(next_page or url_for('doctor_dashboard'))
                
            else:
                # Utilisateur régulier (ou rôle non spécifié)
                return redirect(next_page or url_for('main_index'))

        else:
            # Échec de la vérification du mot de passe ou utilisateur non trouvé
            print(">>> ÉCHEC : Email ou mot de passe incorrect <<<")
            flash('Email ou mot de passe incorrect', 'error')
    
    # 3. Affichage du formulaire de connexion (Méthode GET ou échec POST)
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_index'))

# Route pour le tableau de bord du médecin (doctor.html ou vue simple)
@app.route('/admin/doctor')
@login_required
def doctor_dashboard():
    # Protéger la vue pour que seuls les médecins y aient accès
    if not current_user.is_doctor() and not current_user.is_admin():
        # L'accès sera normalement géré par Flask-Admin, mais cette route assure le tableau de bord
        return redirect(url_for('main_index')) 
        
    return render_template('doctor_dashboard.html') # Créer ce template

# ==========================================================
# ROUTES PUBLIQUES (Vues Utilisateurs)
# ==========================================================

# Route RACINE (Index)
@app.route('/')
def main_index():
    """Affiche la page d'index principale (Menu de navigation : index.html)."""
    return render_template('index.html') 

@app.route('/stats')
@app.route('/dashboard/index') 
def stats_dashboard_main():
    """Affiche les KPIs et les statistiques agrégées (via stats_dashboard.html)."""
    
    try:
        total_centres = db.session.query(CentreSante).count()
    except Exception:
        total_centres = 0
        
    stats = get_kpis()
    return render_template('stats_dashboard.html', stats=stats, total_centres=total_centres) 

@app.route('/map')
def epidemiological_map():
    """Affiche le template de la carte Leaflet (map.html)."""
    return render_template('map.html')

@app.route('/dashboard/carte')
def dashboard_carte():
    """Affiche la carte géospatiale spécifique (dashboard/carte.html)."""
    return render_template('dashboard/carte.html') 
    
# ==========================================================
# ROUTES DE L'APPLICATION (API ENDPOINTS)
# ==========================================================

@app.route('/api/centres/geojson')
def api_centres_geojson():
    """Endpoint API pour les données GeoJSON des centres de santé."""
    data = get_centres_geojson() 
    return jsonify(data)

@app.route('/api/cases')
@app.route('/api/cases/<disease>')
def api_cases(disease=None):
    """Endpoint API pour les données GeoJSON des cas/patients."""
    data = get_cases_geojson(disease)
    return jsonify(data)

@app.route('/api/stats/departements')
def api_stats_departements():
    """Endpoint API pour les statistiques de centres par département."""
    # NOTE: Cette fonction doit être implémentée dans analytics.py
    return jsonify({"data": []})


# ==========================================================
# EXÉCUTION
# ==========================================================
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  
        port=5011,      
        debug=True      
    )