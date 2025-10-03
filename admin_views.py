# admin_views.py

from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from werkzeug.utils import redirect
from flask import url_for, request

# ==========================================================
# 1. VUE PRINCIPALE SÉCURISÉE (CustomAdminIndexView)
# ==========================================================
class CustomAdminIndexView(AdminIndexView):
    """
    Vue d'index personnalisée qui vérifie l'authentification et les rôles (admin/doctor).
    """
    def is_accessible(self):
        # Accessible si l'utilisateur est connecté et est admin ou docteur
        return current_user.is_authenticated and (current_user.is_admin() or current_user.is_doctor())

    def inaccessible_callback(self, name, **kwargs):
        # Redirige vers la page de connexion si l'utilisateur n'est pas authentifié
        return redirect(url_for('login', next=request.url))

# ==========================================================
# 2. VUE DE MODÈLE DE BASE SÉCURISÉE (pour l'héritage)
# ==========================================================
class CustomModelView(ModelView):
    """
    Classe de base pour toutes les vues qui ne devraient être accessibles qu'aux Admins.
    """
    def is_accessible(self):
        # Accessible uniquement si l'utilisateur est Admin
        return current_user.is_authenticated and current_user.is_admin()
        
    def inaccessible_callback(self, name, **kwargs):
        # Si connecté mais non-admin (ex: Doctor), rediriger vers le tableau de bord Doctor
        if current_user.is_authenticated:
             return redirect(url_for('doctor_dashboard'))
        return redirect(url_for('login', next=request.url))


# ==========================================================
# 3. VUES SPÉCIFIQUES (Patient et Consultation - accès Admin OU Docteur)
# ==========================================================
class PatientAdminView(ModelView):
    """Accessible aux Admins et aux Docteurs."""
    column_list = ('nom', 'prenom', 'date_naissance', 'sexe', 'residence_location')
    form_columns = ('nom', 'prenom', 'date_naissance', 'sexe', 'residence_location')
    
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.is_admin() or current_user.is_doctor())
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class ConsultationAdminView(ModelView):
    """Accessible aux Admins et aux Docteurs."""
    column_list = ('patient', 'medecin', 'date_consultation', 'diagnostic')
    form_columns = ('patient', 'medecin', 'date_consultation', 'diagnostic', 'resultat_examen')
    
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.is_admin() or current_user.is_doctor())
        
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

# ==========================================================
# 4. VUES ADMINISTRATIVES (Accès Admin SEULEMENT)
# ==========================================================

class DepartmentAdminView(CustomModelView):
    """Accès Admin seulement."""
    # Cette classe hérite de CustomModelView et est donc sécurisée pour l'admin.
    pass

class CentreSanteAdminView(CustomModelView):
    """Accès Admin seulement."""
    # Cette classe est celle qui était manquante dans votre import !
    column_list = ('nom', 'departement', 'adresse', 'capacite_lits')
    form_columns = ('nom', 'departement', 'adresse', 'location', 'capacite_lits')

# admin_views.py (Extrait de la MedecinAdminView)

class MedecinAdminView(CustomModelView):
    """Accès Admin seulement."""
    # Ces colonnes doivent exister dans le modèle Medecin
    column_list = ('nom', 'prenom', 'specialite', 'centre_sante') 
    form_columns = ('nom', 'prenom', 'specialite', 'centre_sante')