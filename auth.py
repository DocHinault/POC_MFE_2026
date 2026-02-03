"""Gestion de l'authentification et des utilisateurs"""
import hmac
import hashlib
import secrets
import json
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import streamlit as st

def hash_password(password):
    """Hash un mot de passe avec salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${password_hash.hex()}"

def verify_password(password, hashed):
    """Vérifie un mot de passe"""
    try:
        salt, password_hash = hashed.split('$')
        password_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_check.hex() == password_hash
    except:
        return False

def validate_email_format(email):
    """Valide le format d'un email"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def generate_confirmation_code():
    """Génère un code de confirmation"""
    return secrets.token_hex(3).upper()  # Génère un code de 6 caractères

def send_confirmation_email(email, code, nom_entreprise):
    """Envoie un email de confirmation (simulation)"""
    # Cette fonction devrait utiliser SMTP pour envoyer un vrai email
    # Pour le moment, on retourne juste True pour la démo
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
        
        if not all([SENDER_EMAIL, SENDER_PASSWORD]):
            print("Configuration email manquante - simulation uniquement")
            return True
        
        subject = f"MG Social Media Reporting - Code de confirmation"
        body = f"""
        Bonjour {nom_entreprise},
        
        Votre code de confirmation est: {code}
        
        Entrez ce code dans l'application pour confirmer votre inscription.
        
        Cordialement,
        L'équipe MG
        """
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return True  # Continue même si l'envoi échoue (démo)

def is_valid_password(password):
    """Vérifie les critères de sécurité du mot de passe"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not any(char.isupper() for char in password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    if not any(char.isdigit() for char in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    return True, "OK"

def initialize_session_state():
    """Initialise l'état de session Streamlit"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'page' not in st.session_state:
        st.session_state.page = "auth"
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 1
    if 'confirmation_code' not in st.session_state:
        st.session_state.confirmation_code = None
    if 'temp_user_data' not in st.session_state:
        st.session_state.temp_user_data = {}
