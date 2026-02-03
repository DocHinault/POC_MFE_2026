import streamlit as st
from src.auth import initialize_session_state, page_auth, page_login, page_registration, page_confirmation
from src.profile import page_p1

# Initialiser le backend local
import os
import json
from dotenv import load_dotenv
import backend_database
import backend_email
from local_backend import LocalBackendAPI

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
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    if gmail_address and gmail_password:
        try:
            backend_email.init_email_service(gmail_address, gmail_password)
            print(f"✅ Service email initialisé: {gmail_address}")
        except Exception as e:
            print(f"⚠️ Impossible d'initialiser le service email: {e}")
    else:
        print("⚠️ GMAIL_ADDRESS ou GMAIL_PASSWORD non configurés")
        print("   Les codes de confirmation ne seront pas envoyés par email")
    
    # Créer l'instance API locale
    pepper_secret = os.getenv('PEPPER_SECRET', 'default-pepper-change-me')
    api = LocalBackendAPI(pepper_secret)
    print("✅ Backend Python initialisé avec succès!")
    # Si on est en mode fallback local mais que des credentials et sheet_id sont maintenant disponibles,
    # tenter une ré-initialisation automatique de la base Google Sheets
    try:
        current_db = backend_database.get_database()
        if isinstance(current_db, backend_database.LocalFileDatabase):
            # Re-vérifier les credentials/ID
            sheet_id2 = os.getenv('GOOGLE_SHEETS_ID')
            creds_path2 = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
            if sheet_id2 and os.path.exists(creds_path2):
                try:
                    backend_database.init_database(sheet_id2, creds_path2)
                    print(f"🔄 Tentative de connexion à Google Sheets avec ID: {sheet_id2}")
                except Exception as e:
                    print(f"⚠️ Ré-initialisation Google Sheets échouée: {e}")
    except Exception:
        pass
    
except Exception as e:
    print(f"❌ Erreur d'initialisation du backend: {e}")
    import traceback
    traceback.print_exc()
    st.error(f"Erreur d'initialisation: {e}")
    st.stop()

# Configuration de la page
st.set_page_config(
    page_title="POC-MFE-2026 - Social Media Reporting",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Stocker l'API dans session_state pour y accéder dans pages.py
st.session_state.api = api

# Initialiser l'état de session
initialize_session_state()

# Routeur principal
if st.session_state.authenticated:
    page_p1()
else:
    if st.session_state.get("auth_mode") == "login":
        page_login()
    elif st.session_state.get("auth_mode") == "signup":
        page_registration()
    elif st.session_state.get("auth_mode") == "confirm":
        page_confirmation()
    else:
        page_auth()

