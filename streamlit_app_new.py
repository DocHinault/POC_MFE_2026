#!/usr/bin/env python3
"""
POC_MFE_2026 - Application Streamlit
Point d'entrée principal avec nouvelle architecture modulaire
"""
import sys
import os

# Ajouter src au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import streamlit as st
from dotenv import load_dotenv

# Imports depuis la nouvelle structure
from src.auth import initialize_session_state, page_auth, page_login, page_registration, page_confirmation
from src.profile import page_p1
from src.backend import LocalBackendAPI
import src.backend.database as backend_database
import src.backend.email_service as backend_email

load_dotenv()

# Initialiser les services
api = None
try:
    # Initialiser la base de données (optionnel)
    sheet_id = os.getenv('GOOGLE_SHEETS_ID')
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
    
    # Vérifier si credentials.json est valide (contient "private_key")
    is_valid_credentials = False
    if creds_path and os.path.exists(creds_path):
        try:
            import json
            with open(creds_path, 'r') as f:
                creds_json = json.load(f)
                # Vérifier qu'on a les champs obligatoires pour une vraie service account
                is_valid_credentials = 'private_key' in creds_json and creds_json.get('private_key') != 'fake-key'
        except:
            is_valid_credentials = False
    
    if sheet_id and is_valid_credentials:
        try:
            backend_database.init_database(sheet_id, creds_path)
            print(f"✅ Google Sheets initialisé avec ID: {sheet_id}")
        except Exception as e:
            print(f"⚠️ Impossible de connecter à Google Sheets: {e}")
            print("   Utilisation du mode cache local pour les données utilisateur")
    else:
        if not os.path.exists(creds_path):
            print(f"⚠️ Fichier credentials.json non trouvé")
            print("   Utilisation du mode cache local (données non persistées)")
        elif os.path.exists(creds_path) and not is_valid_credentials:
            print(f"⚠️ Fichier credentials.json trouvé mais invalide (pas de clé privée)")
            print("   Téléchargez un vrai fichier de service account depuis Google Cloud Console")
            print("   Utilisation du mode cache local pour les données utilisateur")
        if not sheet_id:
            print("⚠️ GOOGLE_SHEETS_ID non configuré")
    
    # Initialiser le service email (optionnel)
    smtp_server = os.getenv('SMTP_SERVER')
    if smtp_server:
        try:
            backend_email.test_connection()
            print(f"✅ Service email initialisé: {smtp_server}")
        except Exception as e:
            print(f"⚠️ Service email non disponible: {e}")
            print("   Les emails de confirmation ne seront pas envoyés")
    
    # Créer l'API backend locale
    pepper_secret = os.getenv('PEPPER_SECRET', 'default-pepper-change-me-in-production')
    api = LocalBackendAPI(pepper_secret)
    print("✅ Backend local initialisé")

except Exception as e:
    print(f"❌ Erreur lors de l'initialisation: {e}")
    api = None

# Stocker l'API dans session_state pour y accéder dans les pages
if 'api' not in st.session_state and api:
    st.session_state.api = api

# Initialiser l'état de session
initialize_session_state()

# Gestion des routes
def main():
    """Fonction principale de routage"""
    
    # Page d'accueil / choix login-signup
    if st.session_state.page == "auth":
        page_auth()
    
    # Page de connexion
    elif st.session_state.page == "login":
        page_login()
    
    # Page d'inscription
    elif st.session_state.page == "registration":
        page_registration()
    
    # Page de confirmation email
    elif st.session_state.page == "confirmation":
        page_confirmation()
    
    # Dashboard principal (authentifié)
    elif st.session_state.page == "p1":
        page_p1()
    
    # Retour page auth par défaut
    else:
        st.session_state.page = "auth"
        page_auth()

if __name__ == "__main__":
    main()
