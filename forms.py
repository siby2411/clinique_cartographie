from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email

# ==========================================================
# 1. Formulaire de Connexion (Requis pour l'authentification)
# ==========================================================
class LoginForm(FlaskForm):
    """Formulaire de connexion pour l'accès sécurisé."""
    
    # L'email est utilisé comme identifiant de connexion
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Le champ 'password' pour le mot de passe
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    # Bouton de soumission
    submit = SubmitField('Se connecter')

# ----------------------------------------------------------
# 2. Formulaire de Consultation (Votre formulaire existant)
# ----------------------------------------------------------
 