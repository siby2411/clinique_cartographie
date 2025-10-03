# dashboard_views.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.centre_sante import CentreSante
from models.patient import Patient
from forms import ConsultationForm # <--- CORRECTION D'IMPORTATION

# Création d'un Blueprint pour organiser les routes web
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def index():
    # Exemple de récupération de données simples pour le dashboard
    total_centres = db.session.query(CentreSante).count()
    return render_template('dashboard/index.html', total_centres=total_centres)

@bp.route('/carte')
def carte_view():
    return render_template('dashboard/carte.html')

@bp.route('/consultation/new', methods=['GET', 'POST'])
def new_consultation():
    form = ConsultationForm()
    
    if form.validate_on_submit():
        # Logique de traitement du formulaire (Doit être ajouté)
        try:
            # Note: Vous devez importer le modèle Consultation ici si ce n'est pas fait en haut
            from models.consultation import Consultation 
            
            # Vérification basique des ID (à améliorer si l'app est en production)
            if not db.session.query(Patient).get(form.patient_id.data):
                flash('Erreur: ID Patient non trouvé.', 'danger')
                return redirect(url_for('dashboard.new_consultation'))
                
            new_record = Consultation(
                patient_id=form.patient_id.data,
                medecin_id=form.medecin_id.data,
                diagnostic=form.diagnostic.data,
                resultat_examen=form.resultat_examen.data
                # Note: centre_id est manquant dans ce formulaire simple
            )
            
            db.session.add(new_record)
            db.session.commit()
            flash('Consultation enregistrée avec succès!', 'success')
            return redirect(url_for('dashboard.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'enregistrement: {e}", 'danger')
            
    return render_template('dashboard/consultation_form.html', form=form)