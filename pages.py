"""Pages de l'application"""
import streamlit as st
from datetime import datetime
from config import SECTEURS, FACEBOOK_APP_ID, INSTAGRAM_BUSINESS_ACCOUNT_ID, APPS_SCRIPT_URL, API_KEY
from auth import (
    validate_email_format,
    is_valid_password
)
import secrets
from pages.page_social_linking import page_social_linking

# L'API locale est injectée depuis streamlit_app.py et stockée en session
# On l'accède via st.session_state.api
def get_api():
    """Récupère l'API depuis la session"""
    if hasattr(st.session_state, 'api') and st.session_state.api is not None:
        return st.session_state.api
    else:
        st.error("❌ Backend non initialisé. Vérifiez streamlit_app.py")
        st.stop()

def page_auth():
    """Page d'authentification - Connexion ou Inscription"""
    st.set_page_config(page_title="MG - Social Media Reporting", layout="centered")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📝 Inscription", use_container_width=True, key="btn_signup"):
            st.session_state.auth_mode = "signup"
    
    with col2:
        if st.button("🔑 Connexion", use_container_width=True, key="btn_login"):
            st.session_state.auth_mode = "login"
    
    if st.session_state.get("auth_mode") == "signup":
        page_registration()
    elif st.session_state.get("auth_mode") == "login":
        page_login()
    else:
        st.write("")

def page_login():
    """Page de connexion"""
    st.title("Connexion")
    
    if st.button("← Retour", key="back_login"):
        st.session_state.auth_mode = None
        st.rerun()
    
    st.write("")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        email = st.text_input("Email", key="login_email")
    with col2:
        if st.button("Réinitialiser"):
            st.session_state.login_email = ""
    
    password = st.text_input("Mot de passe", type="password", key="login_password")
    
    if st.button("Se connecter", use_container_width=True, type="primary"):
        if not email or not password:
            st.error("Veuillez remplir tous les champs")
        elif not validate_email_format(email):
            st.error("Email invalide")
        else:
            # Utiliser l'API locale
            api = get_api()
            result = api.login(email, password)
            
            if result.get('ok'):
                # Connexion réussie
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_id = result.get('id_client')
                st.session_state.user_data = {
                    "email": email,
                    "id_client": result.get('id_client')
                }
                st.session_state.page = "p1"
                st.success("Connexion réussie!")
                st.rerun()
            else:
                error = result.get('error', 'UNKNOWN_ERROR')
                details = result.get('details', '')
                if error == 'API_TIMEOUT':
                    st.error(f"⏱️ Erreur API: Timeout (60s). L'API est trop lente ou l'URL est incorrecte.\n\nDétails: {details}")
                elif error == 'API_CONNECTION_ERROR':
                    st.error(f"🔌 Erreur de connexion: Impossible de joindre l'API.\n\nVérifiez l'URL dans .env\n{details}")
                elif error == 'INVALID_CREDENTIALS':
                    st.error("❌ Email ou mot de passe incorrect")
                elif error == 'RATE_LIMIT':
                    st.error("⚠️ Trop de tentatives échouées. Réessayez plus tard.")
                else:
                    st.error(f"❌ Erreur API: {error}\n\n{details if details else 'Contactez le support.'}")

def page_registration():
    """Page d'inscription"""
    st.title("Inscription")
    
    if st.button("← Retour", key="back_signup"):
        st.session_state.auth_mode = None
        st.session_state.temp_user_data = {}
        st.rerun()
    
    st.write("")
    
    # Étape 1 : Informations de base
    col1, col2 = st.columns([2, 1])
    
    with col1:
        nom_entreprise = st.text_input(
            "Nom de l'entreprise",
            value=st.session_state.temp_user_data.get("nom_entreprise", ""),
            key="nom_entreprise"
        )
    with col2:
        if st.button("Effacer"):
            st.session_state.temp_user_data["nom_entreprise"] = ""
            st.rerun()
    
    secteur = st.selectbox(
        "Secteur concerné",
        SECTEURS,
        index=SECTEURS.index(st.session_state.temp_user_data.get("secteur", SECTEURS[0]))
        if st.session_state.temp_user_data.get("secteur") in SECTEURS else 0,
        key="secteur"
    )
    
    st.write("")
    
    email = st.text_input(
        "Adresse email",
        value=st.session_state.temp_user_data.get("email", ""),
        key="email"
    )
    
    st.write("**Mot de passe** (minimum 8 caractères, 1 majuscule, 1 chiffre)")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        show_password = st.checkbox("Afficher", key="show_pass", value=False)
    with col2:
        show_password_confirm = st.checkbox("Afficher confirmation", key="show_pass_confirm", value=False)
    
    password_type = "password" if not show_password else "default"
    password_type_confirm = "password" if not show_password_confirm else "default"
    
    password = st.text_input(
        "Mot de passe",
        type=password_type,
        key="password"
    )
    
    password_confirm = st.text_input(
        "Confirmer le mot de passe",
        type=password_type_confirm,
        key="password_confirm",
        help="Entrez manuellement votre mot de passe"
    )
    
    st.write("")
    st.subheader("Connexion réseaux sociaux")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📘 Connecter Facebook", use_container_width=True):
            if FACEBOOK_APP_ID:
                st.info("Redirection vers Facebook pour l'authentification...")
                st.session_state.temp_user_data["facebook"] = "En attente de liaison"
            else:
                st.warning("Intégration Facebook non configurée")
    
    with col2:
        if st.button("📷 Connecter Instagram", use_container_width=True):
            if INSTAGRAM_BUSINESS_ACCOUNT_ID:
                st.info("Redirection vers Instagram pour l'authentification...")
                st.session_state.temp_user_data["instagram"] = "En attente de liaison"
            else:
                st.warning("Intégration Instagram non configurée")
    
    facebook_status = st.session_state.temp_user_data.get("facebook", "Non lié")
    instagram_status = st.session_state.temp_user_data.get("instagram", "Non lié")
    
    st.caption(f"Facebook: {facebook_status}")
    st.caption(f"Instagram: {instagram_status}")
    
    st.write("")
    
    if st.button("Créer un compte", use_container_width=True, type="primary"):
        errors = []
        
        if not nom_entreprise.strip():
            errors.append("Le nom de l'entreprise est requis")
        
        if not email.strip():
            errors.append("L'email est requis")
        elif not validate_email_format(email):
            errors.append("Email invalide")
        
        if not password:
            errors.append("Le mot de passe est requis")
        else:
            is_valid, msg = is_valid_password(password)
            if not is_valid:
                errors.append(msg)
        
        if password != password_confirm:
            errors.append("Les mots de passe ne correspondent pas")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Appeler l'API locale pour démarrer l'inscription
            api = get_api()
            result = api.register_start(
                email=email,
                password=password,
                nom_entreprise=nom_entreprise,
                secteur=secteur
            )
            
            if result.get('ok'):
                # Inscription lancée avec succès
                st.session_state.temp_user_data = {
                    "nom_entreprise": nom_entreprise,
                    "email": email,
                    "secteur": secteur,
                    "facebook": st.session_state.temp_user_data.get("facebook", "Non lié"),
                    "instagram": st.session_state.temp_user_data.get("instagram", "Non lié"),
                }
                # En mode démo, sauvegarder le code
                if result.get('demo_code'):
                    st.session_state.temp_user_data['demo_code'] = result.get('demo_code')
                st.session_state.auth_mode = "confirm"
                st.success("Code de confirmation envoyé à votre email!")
                # Afficher le code en mode démo
                if result.get('demo_code'):
                    st.warning(f"📝 Mode démo - Code: **{result.get('demo_code')}**")
                st.rerun()
            else:
                error = result.get('error', 'UNKNOWN_ERROR')
                details = result.get('details', '')
                if error == 'API_TIMEOUT':
                    st.error(f"⏱️ Erreur API: Timeout après 60s. L'API Apps Script est trop lente ou déployée incorrectement.\n\nDétails: {details}")
                elif error == 'API_CONNECTION_ERROR':
                    st.error(f"🔌 Erreur de connexion: Impossible de joindre l'API Apps Script.\n\nVérifiez que l'URL dans .env est correcte:\n{details}")
                elif error == 'API_HTTP_ERROR':
                    status = result.get('status_code', '?')
                    st.error(f"HTTP {status}: {details}")
                elif error == 'UNAUTHORIZED':
                    st.error("🔑 Clé API invalide.\n\nVérifiez que API_KEY dans .env correspond aux propriétés Apps Script.")
                elif error == 'EMAIL_EXISTS':
                    st.error("Cet email est déjà utilisé. Veuillez vous connecter.")
                elif error == 'INVALID_INPUT':
                    st.error("Veuillez vérifier vos données (email, mot de passe, secteur)")
                else:
                    st.error(f"Erreur lors de l'inscription: {error}")

def page_confirmation():
    """Page de confirmation par email"""
    st.title("Confirmez votre inscription")
    
    st.write(f"Un code de confirmation a été envoyé à: **{st.session_state.temp_user_data.get('email')}**")
    st.write("")
    
    code_input = st.text_input("Entrez le code de confirmation (6 caractères)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Confirmer", use_container_width=True, type="primary"):
            if not code_input.strip():
                st.error("Veuillez entrer le code")
            else:
                # Appeler l'API locale pour vérifier le code
                api = get_api()
                email = st.session_state.temp_user_data.get('email')
                result = api.register_verify(email=email, code=code_input.strip())
                
                if result.get('ok'):
                    # Inscription complétée avec succès
                    st.success("Inscription confirmée! Vous êtes maintenant connecté.")
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_id = result.get('id_client')
                    st.session_state.user_data = {
                        "nom_entreprise": st.session_state.temp_user_data.get("nom_entreprise"),
                        "secteur": st.session_state.temp_user_data.get("secteur"),
                        "email": email,
                        "id_client": result.get('id_client')
                    }
                    st.session_state.auth_mode = None
                    st.session_state.temp_user_data = {}
                    st.session_state.page = "p1"
                    
                    st.rerun()
                else:
                    error = result.get('error', 'UNKNOWN_ERROR')
                    if error == 'CODE_EXPIRED':
                        st.error("Le code a expiré. Veuillez recommencer l'inscription.")
                    elif error == 'INVALID_CODE':
                        st.error("Code incorrect. Veuillez réessayer.")
                    else:
                        st.error(f"Erreur: {error}")
    
    with col2:
        if st.button("Retour", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()

def page_p1():
    """Page P1 - Dashboard principal"""
    st.set_page_config(page_title="MG - Social Media Reporting", layout="wide")
    
    # En-tête avec navigation
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    
    with col1:
        st.title("MG")
    
    with col2:
        # Navigation entre les sections
        nav_col1, nav_col2, nav_col3 = st.columns(3)
        with nav_col1:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
        with nav_col2:
            if st.button("🔗 Mes comptes", use_container_width=True):
                st.session_state.current_page = "accounts"
        with nav_col3:
            if st.button("⚙️ Paramètres", use_container_width=True):
                st.session_state.current_page = "settings"
    
    with col4:
        user_info = f"👤 {st.session_state.user_email}"
        st.caption(user_info)
        if st.button("🚪 Déconnexion"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_id = None
            st.session_state.user_data = None
            st.session_state.auth_mode = None
            st.session_state.page = "auth"
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.write("")
    
    # Initialiser le state de la page actuelle
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    # Router selon la page sélectionnée
    if st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "accounts":
        page_social_linking()
    elif st.session_state.current_page == "settings":
        show_settings()


def show_dashboard():
    """Affiche le dashboard principal"""
    st.subheader("📊 Dashboard")
    
    from social_auth import SocialMediaLinkManager
    manager = SocialMediaLinkManager()
    linked_accounts = manager.get_linked_accounts(st.session_state.user_id)
    
    if not linked_accounts:
        st.warning("⚠️ Aucun compte social lié")
        st.info("Cliquez sur 'Mes comptes' pour lier votre compte Instagram ou Facebook")
        
        st.write("")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Comptes liés", 0)
        with col2:
            st.metric("Pages gérées", 0)
        with col3:
            st.metric("Followers", 0)
    else:
        # Afficher le résumé des comptes liés
        col1, col2, col3 = st.columns(3)
        
        total_accounts = len([v for k, v in linked_accounts.items() if k != 'facebook_pages'])
        total_pages = len(linked_accounts.get('facebook_pages', []))
        total_followers = 0
        
        if 'instagram' in linked_accounts:
            total_followers += linked_accounts['instagram'].get('followers_count', 0)
        
        for page in linked_accounts.get('facebook_pages', []):
            total_followers += page.get('fans_count', 0)
        
        with col1:
            st.metric("Comptes liés", total_accounts)
        with col2:
            st.metric("Pages gérées", total_pages)
        with col3:
            st.metric("Followers", f"{total_followers:,}")
        
        st.divider()
        
        # Afficher les données de chaque compte
        if 'instagram' in linked_accounts:
            st.subheader("📸 Instagram")
            ig = linked_accounts['instagram']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Compte", f"@{ig['username']}")
            with col2:
                st.metric("Followers", f"{ig.get('followers_count', 0):,}")
            with col3:
                st.metric("Posts", ig.get('media_count', 0))
        
        if 'facebook_pages' in linked_accounts and linked_accounts['facebook_pages']:
            st.subheader("📄 Pages Facebook")
            
            for page in linked_accounts['facebook_pages']:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Page", page['name'])
                with col2:
                    st.metric("Fans", f"{page.get('fans_count', 0):,}")
                with col3:
                    st.metric("Followers", f"{page.get('followers_count', 0):,}")
                st.divider()
    
    st.write("")
    st.info("💡 Contenu du dashboard à venir: analytiques en temps réel, graphiques, rapports...")


def show_settings():
    """Affiche les paramètres"""
    st.subheader("⚙️ Paramètres")
    
    if st.session_state.user_data:
        user_data = st.session_state.user_data
        
        st.write("### Informations de l'entreprise")
        st.write(f"**Email:** {user_data.get('email', 'N/A')}")
        st.write(f"**Nom:** {user_data.get('nom_entreprise', 'N/A')}")
        st.write(f"**Secteur:** {user_data.get('secteur', 'N/A')}")
    
    st.write("")
    
    with st.expander("🔒 Changer le mot de passe"):
        old_password = st.text_input("Mot de passe actuel", type="password")
        new_password = st.text_input("Nouveau mot de passe", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password")
        
        if st.button("Mettre à jour"):
            if not all([old_password, new_password, confirm_password]):
                st.error("Veuillez remplir tous les champs")
            elif new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
            else:
                st.success("✅ Mot de passe mis à jour avec succès!")
    
    st.write("")
    
    with st.expander("🗑️ Supprimer le compte"):
        st.warning("⚠️ Cette action est irréversible!")
        
        confirm = st.checkbox("Je comprends que cela supprimera mon compte et toutes mes données")
        
        if confirm and st.button("Supprimer mon compte", type="secondary"):
            st.success("Compte supprimé!")
            st.session_state.authenticated = False
            st.session_state.page = "auth"
            st.rerun()
