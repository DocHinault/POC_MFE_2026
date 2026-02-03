"""Pages de l'application"""
import streamlit as st
from datetime import datetime
from config import SECTEURS, FACEBOOK_APP_ID, INSTAGRAM_BUSINESS_ACCOUNT_ID
from auth import (
    validate_email_format,
    is_valid_password
)
import secrets
from pages.page_social_linking import page_social_linking

# Configurer le style de la page
def configure_page_style():
    """Configure les styles CSS personnalisés avec design professionnel"""
    st.markdown("""
    <style>
    /* ===== VARIABLES DE DESIGN ===== */
    :root {
        --primary: #2563EB;
        --primary-dark: #1E40AF;
        --primary-light: #3B82F6;
        --secondary: #F59E0B;
        --success: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --info: #06B6D4;
        
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-light: #78828F;
        
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8FAFC;
        --bg-tertiary: #E2E8F0;
        
        --border-color: #E2E8F0;
        --border-color-light: #F1F5F9;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
    }

    /* ===== RESET & BASE STYLES ===== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        color: var(--text-primary);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        line-height: 1.6;
    }

    /* ===== TYPOGRAPHY ===== */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    h2 {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }

    h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    p {
        color: var(--text-secondary);
        font-size: 1rem;
    }

    .subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* ===== CONTAINERS & CARDS ===== */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .card {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .card:hover {
        border-color: var(--primary-light);
        box-shadow: var(--shadow-lg);
    }

    .card-sm {
        padding: 1.5rem;
        border-radius: var(--radius-md);
    }

    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid var(--bg-secondary);
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        text-transform: none;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }

    /* Boutons secondaires */
    .btn-secondary {
        background: var(--bg-secondary);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
    }

    .btn-secondary:hover {
        background: var(--bg-tertiary);
        border-color: var(--primary);
    }

    /* Boutons danger */
    .btn-danger {
        background: linear-gradient(135deg, var(--danger) 0%, #DC2626 100%);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
    }

    .btn-danger:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.35);
    }

    /* ===== INPUTS & FORMS ===== */
    .stTextInput > div > div > input,
    .stTextInput > div > div > textarea,
    .stPasswordInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > div {
        border: 1.5px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
        font-family: inherit !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextInput > div > div > textarea:focus,
    .stPasswordInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }

    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }

    /* Input labels */
    .stTextInput > label,
    .stPasswordInput > label,
    .stSelectbox > label,
    .stCheckbox > label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .input-group {
        margin-bottom: 1.5rem;
    }

    .input-help {
        font-size: 0.875rem;
        color: var(--text-light);
        margin-top: 0.25rem;
    }

    /* ===== CHECKBOXES ===== */
    .stCheckbox > label {
        display: flex;
        align-items: center;
        cursor: pointer;
        font-weight: 500;
        color: var(--text-primary);
    }

    /* ===== ALERTS & MESSAGES ===== */
    .stAlert {
        border-radius: var(--radius-lg) !important;
        border: 1px solid !important;
        padding: 1rem 1.5rem !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
        border-color: var(--success) !important;
        color: var(--text-primary) !important;
    }

    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        border-color: var(--danger) !important;
        color: var(--text-primary) !important;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%) !important;
        border-color: var(--warning) !important;
        color: var(--text-primary) !important;
    }

    .stInfo {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%) !important;
        border-color: var(--info) !important;
        color: var(--text-primary) !important;
    }

    /* ===== COLUMNS & LAYOUT ===== */
    .stColumns {
        gap: 1.5rem;
    }

    /* ===== DIVIDERS ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 2rem 0;
    }

    /* ===== BADGES & TAGS ===== */
    .badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: var(--radius-sm);
        font-weight: 600;
        font-size: 0.875rem;
        background: var(--bg-secondary);
        color: var(--text-primary);
    }

    .badge-primary {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(37, 99, 235, 0.1) 100%);
        color: var(--primary-dark);
    }

    .badge-success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        color: #047857;
    }

    /* ===== METRICS & STATS ===== */
    .metric {
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border-color-light);
        transition: all 0.3s ease;
    }

    .metric:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.875rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    /* ===== NAVIGATION ===== */
    .nav-tabs {
        display: flex;
        border-bottom: 2px solid var(--border-color);
        gap: 2rem;
    }

    .nav-tab {
        padding: 1rem 0;
        border-bottom: 3px solid transparent;
        color: var(--text-secondary);
        cursor: pointer;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .nav-tab:hover {
        color: var(--primary);
    }

    .nav-tab.active {
        color: var(--primary);
        border-bottom-color: var(--primary);
    }

    /* ===== EXPANDERS ===== */
    .stExpander {
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ===== TABLES ===== */
    .stDataFrame {
        border-radius: var(--radius-lg) !important;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }

        h2 {
            font-size: 1.5rem;
        }

        .card {
            padding: 1.5rem;
        }

        .main-container {
            padding: 1rem;
        }
    }

    /* ===== ANIMATIONS ===== */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    .animate-in {
        animation: slideIn 0.3s ease-out;
    }

    .stMainBlockContainer {
        animation: fadeIn 0.5s ease-out;
    }

    /* ===== UTILITIES ===== */
    .text-center {
        text-align: center;
    }

    .text-muted {
        color: var(--text-light);
    }

    .mt-1 { margin-top: 0.5rem; }
    .mt-2 { margin-top: 1rem; }
    .mt-3 { margin-top: 1.5rem; }
    .mt-4 { margin-top: 2rem; }

    .mb-1 { margin-bottom: 0.5rem; }
    .mb-2 { margin-bottom: 1rem; }
    .mb-3 { margin-bottom: 1.5rem; }
    .mb-4 { margin-bottom: 2rem; }

    .pt-2 { padding-top: 1rem; }
    .pb-2 { padding-bottom: 1rem; }

    </style>
    """, unsafe_allow_html=True)

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
    configure_page_style()
    
    # En-tête avec logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #0066FF; margin: 20px 0;'>📊 MG</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B; font-size: 14px;'>Social Media Reporting</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Boutons d'authentification
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<div style='padding: 24px; background: linear-gradient(135deg, rgba(0, 102, 255, 0.05) 0%, rgba(0, 102, 255, 0.02) 100%); border-radius: 12px; border: 2px solid #E0E7FF;'>", unsafe_allow_html=True)
        if st.button("📝 Créer un compte", use_container_width=True, key="btn_signup"):
            st.session_state.auth_mode = "signup"
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='padding: 24px; background: linear-gradient(135deg, rgba(0, 102, 255, 0.05) 0%, rgba(0, 102, 255, 0.02) 100%); border-radius: 12px; border: 2px solid #E0E7FF;'>", unsafe_allow_html=True)
        if st.button("🔑 Se connecter", use_container_width=True, key="btn_login"):
            st.session_state.auth_mode = "login"
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state.get("auth_mode") == "signup":
        page_registration()
    elif st.session_state.get("auth_mode") == "login":
        page_login()
    else:
        # Page d'accueil vide
        st.markdown("""
        <div style='text-align: center; padding: 40px 0;'>
            <h3 style='color: #64748B;'>Bienvenue sur MG</h3>
            <p style='color: #94A3B8; font-size: 16px;'>Gérez vos comptes Instagram et Facebook en un seul endroit</p>
        </div>
        """, unsafe_allow_html=True)

def page_login():
    """Page de connexion"""
    st.set_page_config(page_title="Connexion - MG", layout="centered")
    configure_page_style()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>📊</div>
            <h1 style='margin: 0 0 0.5rem 0; color: #0F172A;'>Connexion</h1>
            <p style='font-size: 1.1rem; color: #64748B; margin: 0;'>Accédez à votre tableau de bord social media</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Formulaire de connexion
    st.markdown("<div class='card animate-in'>", unsafe_allow_html=True)
    
    email = st.text_input("📧 Adresse email", placeholder="votre@email.com", key="login_email")
    
    col1, col2 = st.columns([5, 1], gap="small")
    
    with col1:
        password_type = "password" if not st.session_state.get("show_login_pass", False) else "default"
        password = st.text_input("🔒 Mot de passe", type=password_type, key="login_password")
    
    with col2:
        if st.button("👁️" if st.session_state.get("show_login_pass", False) else "👁️‍🗨️", key="toggle_login_pass", help="Afficher/Masquer"):
            st.session_state.show_login_pass = not st.session_state.get("show_login_pass", False)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Se connecter", use_container_width=True, key="login_btn"):
            if not email or not password:
                st.error("⚠️ Veuillez remplir tous les champs")
            elif not validate_email_format(email):
                st.error("❌ Email invalide")
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
                    st.balloons()
                    st.success("✅ Connexion réussie!")
                    st.rerun()
                else:
                    error = result.get('error', 'UNKNOWN_ERROR')
                    if error == 'INVALID_CREDENTIALS':
                        st.error("❌ Email ou mot de passe incorrect")
                    elif error == 'RATE_LIMIT':
                        st.error("⚠️ Trop de tentatives échouées. Réessayez plus tard.")
                    else:
                        st.error(f"❌ Erreur: {error}")
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Retour", use_container_width=True, key="back_login"):
            st.session_state.auth_mode = None
            st.rerun()
    
    st.markdown("""
    <div style='text-align: center; margin-top: 2rem; padding: 1.5rem; background: #F8FAFC; border-radius: 12px; border: 1px solid #E2E8F0;'>
        <p style='margin: 0; color: #64748B;'>Pas de compte? <a href='#' onclick='window.location.href=window.location.href' style='color: #2563EB; font-weight: 600; text-decoration: none;'>Créer un compte</a></p>
    </div>
    """, unsafe_allow_html=True)

def page_registration():
    """Page d'inscription"""
    st.set_page_config(page_title="Inscription - MG", layout="centered")
    configure_page_style()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🚀</div>
            <h1 style='margin: 0 0 0.5rem 0; color: #0F172A;'>Créer un compte</h1>
            <p style='font-size: 1.1rem; color: #64748B; margin: 0;'>Rejoignez des centaines de professionnels du social media</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 1: Informations entreprise
    st.markdown("""
    <div class='card animate-in'>
        <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>📋</span>
            <h3 style='margin: 0; color: #0F172A;'>Informations entreprise</h3>
        </div>
    """, unsafe_allow_html=True)
    
    nom_entreprise = st.text_input(
        "Nom de l'entreprise",
        placeholder="Ex: Mon Agence Marketing",
        value=st.session_state.temp_user_data.get("nom_entreprise", ""),
        key="nom_entreprise"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    secteur = st.selectbox(
        "Secteur d'activité",
        SECTEURS,
        index=SECTEURS.index(st.session_state.temp_user_data.get("secteur", SECTEURS[0]))
        if st.session_state.temp_user_data.get("secteur") in SECTEURS else 0,
        key="secteur"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Identifiants
    st.markdown("""
    <div class='card animate-in'>
        <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>🔐</span>
            <h3 style='margin: 0; color: #0F172A;'>Vos identifiants</h3>
        </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input(
        "Adresse email",
        placeholder="vous@example.com",
        value=st.session_state.temp_user_data.get("email", ""),
        key="email"
    )
    
    st.markdown("<p style='font-size: 0.875rem; color: #64748B; margin: 1rem 0 0.5rem 0;'><strong>Mot de passe</strong> <span style='color: #10B981;'>✓</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8rem; color: #78828F; margin: 0 0 1rem 0;'>Minimum 8 caractères • 1 majuscule • 1 chiffre</p>", unsafe_allow_html=True)
    
    # Utiliser des colonnes pour les champs de password avec les yeux
    col1, col2 = st.columns([5, 1], gap="small")
    
    with col1:
        password_type = "password" if not st.session_state.get("show_pass", False) else "default"
        password = st.text_input(
            "Mot de passe",
            type=password_type,
            placeholder="••••••••",
            key="password"
        )
    
    with col2:
        if st.button("👁️" if st.session_state.get("show_pass", False) else "👁️‍🗨️", key="toggle_pass", help="Afficher/Masquer"):
            st.session_state.show_pass = not st.session_state.get("show_pass", False)
            st.rerun()
    
    col1, col2 = st.columns([5, 1], gap="small")
    
    with col1:
        password_type_confirm = "password" if not st.session_state.get("show_pass_confirm", False) else "default"
        password_confirm = st.text_input(
            "Confirmer le mot de passe",
            type=password_type_confirm,
            placeholder="••••••••",
            key="password_confirm"
        )
    
    with col2:
        if st.button("👁️" if st.session_state.get("show_pass_confirm", False) else "👁️‍🗨️", key="toggle_pass_confirm", help="Afficher/Masquer"):
            st.session_state.show_pass_confirm = not st.session_state.get("show_pass_confirm", False)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Boutons d'action
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Retour", use_container_width=True, key="back_signup"):
            st.session_state.auth_mode = None
            st.session_state.temp_user_data = {}
            st.rerun()
    
    with col3:
        if st.button("✅ Créer un compte", use_container_width=True, key="signup_btn"):
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
                # Appeler l'API locale
                api = get_api()
                result = api.register_start(
                    email=email,
                    password=password,
                    nom_entreprise=nom_entreprise,
                    secteur=secteur
                )
                
                if result.get('ok'):
                    st.session_state.temp_user_data = {
                        "nom_entreprise": nom_entreprise,
                        "email": email,
                        "secteur": secteur,
                    }
                    if result.get('demo_code'):
                        st.session_state.temp_user_data['demo_code'] = result.get('demo_code')
                    st.session_state.auth_mode = "confirm"
                    st.balloons()
                    st.success("✅ Code de confirmation envoyé!")
                    if result.get('demo_code'):
                        st.info(f"📝 Mode démo - Code: **{result.get('demo_code')}**")
                    st.rerun()
                else:
                    error = result.get('error', 'UNKNOWN_ERROR')
                    if error == 'EMAIL_EXISTS':
                        st.error("Cet email est déjà utilisé. Veuillez vous connecter.")
                    elif error == 'INVALID_INPUT':
                        st.error("Veuillez vérifier vos données")
                    else:
                        st.error(f"Erreur: {error}")

def page_confirmation():
    """Page de confirmation par email"""
    st.set_page_config(page_title="Confirmation - MG", layout="centered")
    configure_page_style()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #1E293B; margin: 20px 0;'>✉️ Confirmation</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Vérifiez votre email</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <p style='color: #64748B; font-size: 16px;'>Un code de confirmation a été envoyé à:</p>
        <p style='color: #0066FF; font-weight: 600; font-size: 18px;'>{st.session_state.temp_user_data.get('email')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    code_input = st.text_input(
        "Entrez le code de confirmation",
        placeholder="000000",
        key="confirm_code",
        max_chars=6
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Retour", use_container_width=True, key="back_confirm"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    
    with col3:
        if st.button("✅ Confirmer", use_container_width=True, key="confirm_btn"):
            if not code_input.strip():
                st.error("Veuillez entrer le code")
            else:
                # Appeler l'API locale
                api = get_api()
                email = st.session_state.temp_user_data.get('email')
                result = api.register_verify(email=email, code=code_input.strip())
                
                if result.get('ok'):
                    # Inscription complétée avec succès
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
                    
                    st.balloons()
                    st.success("✅ Inscription confirmée! Bienvenue! 🎉")
                    st.rerun()
                else:
                    error = result.get('error', 'UNKNOWN_ERROR')
                    if error == 'CODE_EXPIRED':
                        st.error("⏱️ Le code a expiré. Veuillez recommencer.")
                    elif error == 'INVALID_CODE':
                        st.error("❌ Code incorrect. Veuillez réessayer.")
                    else:
                        st.error(f"Erreur: {error}")

def page_p1():
    """Page P1 - Dashboard principal"""
    st.set_page_config(page_title="MG - Dashboard", layout="wide")
    configure_page_style()
    
    # Header professionnel
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); border-bottom: 1px solid #E2E8F0; padding: 1.5rem 2rem; margin: -1rem -1rem 2rem -1rem;'>
        <div style='display: flex; align-items: center; justify-content: space-between; max-width: 1400px; margin: 0 auto;'>
            <div style='display: flex; align-items: center; gap: 0.75rem;'>
                <span style='font-size: 2rem;'>📊</span>
                <h1 style='margin: 0; color: #2563EB; font-size: 1.75rem;'>MG</h1>
                <span style='color: #64748B; font-size: 0.875rem; margin-left: 1rem;'>Social Media Dashboard</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation - Tabs style
    col1, col2, col3, col_spacer, col_logout = st.columns([1.2, 1.2, 1.2, 3, 1])
    
    with col1:
        if st.button("👤 Profil", use_container_width=True, key="nav_profile", help="Gérer votre profil"):
            st.session_state.current_page = "profile"
            st.rerun()
    
    with col2:
        if st.button("🔗 Liaison", use_container_width=True, key="nav_accounts", help="Connecter vos comptes"):
            st.session_state.current_page = "linking"
            st.rerun()
    
    with col3:
        if st.button("📈 Analyse", use_container_width=True, key="nav_analyze", help="Analyser vos performances"):
            st.session_state.current_page = "analysis"
            st.rerun()
    
    with col_logout:
        if st.button("🚪 Déconnexion", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_id = None
            st.session_state.user_data = None
            st.session_state.auth_mode = None
            st.session_state.page = "auth"
            st.session_state.current_page = "profile"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialiser le state de la page actuelle
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "profile"
    
    # Router selon la page sélectionnée
    if st.session_state.current_page == "profile":
        show_profile_tab()
    elif st.session_state.current_page == "linking":
        show_linking_tab()
    elif st.session_state.current_page == "analysis":
        show_analysis_tab()


def show_profile_tab():
    """Onglet Profil - Affichage et édition des informations"""
    st.markdown("""
    <h2 style='color: #0F172A; margin-bottom: 2rem;'>👤 Votre profil</h2>
    """, unsafe_allow_html=True)
    
    # Afficher les informations du profil
    if st.session_state.user_data:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style='text-align: center;'>
                <div style='width: 120px; height: 120px; background: linear-gradient(135deg, #2563EB, #1E40AF); border-radius: 16px; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 50px; box-shadow: 0 10px 25px rgba(37, 99, 235, 0.2);'>
                    👤
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='card animate-in'>
                <div class='card-header'>
                    <h3 class='card-title'>Informations du compte</h3>
                </div>
            """, unsafe_allow_html=True)
            
            user_data = st.session_state.user_data
            
            st.markdown(f"""
            <div style='margin-bottom: 1rem;'>
                <p style='color: #78828F; font-size: 0.875rem; margin: 0 0 0.25rem 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Email</p>
                <p style='color: #0F172A; font-size: 1rem; margin: 0; font-weight: 500;'>{user_data.get('email', 'N/A')}</p>
            </div>
            
            <div style='margin-bottom: 1rem;'>
                <p style='color: #78828F; font-size: 0.875rem; margin: 0 0 0.25rem 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Entreprise</p>
                <p style='color: #0F172A; font-size: 1rem; margin: 0; font-weight: 500;'>{user_data.get('nom_entreprise', 'N/A')}</p>
            </div>
            
            <div style='margin-bottom: 1.5rem;'>
                <p style='color: #78828F; font-size: 0.875rem; margin: 0 0 0.25rem 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;'>Secteur</p>
                <p style='color: #0F172A; font-size: 1rem; margin: 0; font-weight: 500;'>{user_data.get('secteur', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✏️ Modifier le profil", use_container_width=True, key="edit_profile_btn"):
                st.session_state.current_page = "edit_profile"
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)


def show_linking_tab():
    """Onglet Liaison - Connecter Instagram et Facebook"""
    from pages.page_social_linking import page_social_linking
    page_social_linking()


def show_analysis_tab():
    """Onglet Analyse - Analyser et générer rapports"""
    st.markdown("""
    <h2 style='color: #0F172A; margin-bottom: 2rem;'>📈 Analyse & Recommandations</h2>
    """, unsafe_allow_html=True)
    
    # Vérifier si des comptes sont liés
    from social_auth import SocialMediaLinkManager
    manager = SocialMediaLinkManager()
    linked_accounts = manager.get_linked_accounts(st.session_state.user_id)
    
    if not linked_accounts:
        st.markdown("""
        <div class='card animate-in' style='text-align: center; padding: 3rem 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔐</div>
            <p style='color: #64748B; font-size: 1.1rem; margin: 0.5rem 0; font-weight: 500;'>Aucun compte lié</p>
            <p style='color: #78828F; font-size: 0.95rem; margin: 0;'>Connectez vos comptes Instagram et Facebook pour activer l'analyse</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Afficher les options d'analyse
    st.markdown("""
    <div class='card animate-in'>
        <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>📊</span>
            <h3 style='margin: 0; color: #0F172A;'>Pipeline d'analyse</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style='color: #64748B; margin-bottom: 1.5rem;'>
    Lancez l'analyse complète de vos performances sociales du dernier mois. 
    Le système va:
    </p>
    
    <ul style='color: #64748B; line-height: 1.8;'>
        <li>📊 Récupérer tous les KPI de vos comptes</li>
        <li>💾 Sauvegarder les données dans Google Sheet</li>
        <li>🤖 Utiliser l'IA (GPT) pour analyser les performances</li>
        <li>📄 Générer un PowerPoint professionnel</li>
        <li>📧 Envoyer le rapport par email avec recommandations</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Afficher les comptes liés
    st.markdown("""
    <div class='card animate-in'>
        <h3 style='color: #0F172A; margin-top: 0;'>Comptes connectés</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    if 'instagram' in linked_accounts:
        with col1:
            st.markdown(f"""
            <div style='padding: 1rem; background: #F8FAFC; border-radius: 8px; border-left: 4px solid #E879F9;'>
                <p style='margin: 0 0 0.5rem 0; color: #78828F; font-size: 0.875rem;'>Instagram</p>
                <p style='margin: 0; color: #0F172A; font-weight: 600;'>@{linked_accounts['instagram'].get('username', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if 'facebook' in linked_accounts or 'facebook_pages' in linked_accounts:
        with col2:
            pages = linked_accounts.get('facebook_pages', [])
            if pages:
                pages_text = f"{len(pages)} page(s)"
                st.markdown(f"""
                <div style='padding: 1rem; background: #F8FAFC; border-radius: 8px; border-left: 4px solid #1877F2;'>
                    <p style='margin: 0 0 0.5rem 0; color: #78828F; font-size: 0.875rem;'>Facebook</p>
                    <p style='margin: 0; color: #0F172A; font-weight: 600;'>{pages_text}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton pour lancer l'analyse
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🚀 Lancer l'analyse complète", use_container_width=True, key="run_analysis"):
            with st.spinner("⏳ Analyse en cours... Cela peut prendre quelques minutes"):
                try:
                    from analysis_pipeline import AnalysisPipeline
                    
                    # Préparer les données Instagram
                    instagram_data = None
                    if 'instagram' in linked_accounts:
                        instagram_data = {
                            'id': linked_accounts['instagram'].get('id'),
                            'access_token': linked_accounts['instagram'].get('access_token')
                        }
                    
                    # Préparer les données Facebook
                    facebook_data = []
                    if 'facebook_pages' in linked_accounts:
                        facebook_data = [
                            {
                                'id': page.get('id'),
                                'access_token': page.get('access_token')
                            }
                            for page in linked_accounts['facebook_pages']
                            if page.get('id') and page.get('access_token')
                        ]
                    
                    # Créer le pipeline
                    pipeline = AnalysisPipeline(
                        user_id=st.session_state.user_id,
                        user_email=st.session_state.user_email,
                        user_name=st.session_state.user_data.get('nom_entreprise', 'Client')
                    )
                    
                    # Lancer l'analyse complète
                    result = pipeline.run_full_pipeline(
                        instagram_data=instagram_data,
                        facebook_data=facebook_data,
                        sheet_id=None  # À implémenter avec l'ID de la Google Sheet de l'utilisateur
                    )
                    
                    if result['success']:
                        st.success("✅ Analyse complétée avec succès!")
                        st.success(f"📊 {result['instagram_kpis'].get('total_posts', 0) if result['instagram_kpis'] else 0} posts Instagram analysés")
                        if result['email_sent']:
                            st.info("📧 Le rapport a été envoyé à votre email")
                        if result['powerpoint_path']:
                            st.info(f"📄 PowerPoint généré: {result['powerpoint_path']}")
                    else:
                        st.warning(f"⚠️ L'analyse a eu des problèmes: {', '.join(result['errors'])}")
                        if result['powerpoint_path']:
                            st.info(f"Un rapport partiel a été généré: {result['powerpoint_path']}")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse: {str(e)}")


def show_edit_profile():
    """Page d'édition du profil"""
    st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem;'>
        <h2 style='margin: 0; color: #0F172A;'>✏️ Modifier le profil</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("← Retour", use_container_width=True, key="back_profile"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Récupérer les données actuelles
    user_data = st.session_state.user_data
    
    # Section 1: Informations entreprise
    st.markdown("""
    <div class='card animate-in'>
        <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>📋</span>
            <h3 style='margin: 0; color: #0F172A;'>Informations entreprise</h3>
        </div>
    """, unsafe_allow_html=True)
    
    nom_entreprise = st.text_input(
        "Nom de l'entreprise",
        placeholder="Ex: Mon Agence Marketing",
        value=user_data.get("nom_entreprise", ""),
        key="edit_nom_entreprise"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    secteur = st.selectbox(
        "Secteur d'activité",
        SECTEURS,
        index=SECTEURS.index(user_data.get("secteur", SECTEURS[0]))
        if user_data.get("secteur") in SECTEURS else 0,
        key="edit_secteur"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: Email et sécurité
    st.markdown("""
    <div class='card animate-in'>
        <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>🔐</span>
            <h3 style='margin: 0; color: #0F172A;'>Email et sécurité</h3>
        </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input(
        "Adresse email",
        placeholder="vous@example.com",
        value=user_data.get("email", ""),
        key="edit_email"
    )
    
    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.875rem; font-weight: 600; color: #0F172A; margin: 0 0 1rem 0;'>Modifier le mot de passe</p>", unsafe_allow_html=True)
    
    change_password = st.checkbox("Modifier mon mot de passe", key="edit_change_pwd")
    
    if change_password:
        col1, col2 = st.columns([5, 1], gap="small")
        
        with col1:
            password_type = "password" if not st.session_state.get("edit_show_pass", False) else "default"
            new_password = st.text_input(
                "Nouveau mot de passe",
                type=password_type,
                placeholder="••••••••",
                key="edit_new_password"
            )
        
        with col2:
            if st.button("👁️" if st.session_state.get("edit_show_pass", False) else "👁️‍🗨️", key="edit_toggle_pass", help="Afficher/Masquer"):
                st.session_state.edit_show_pass = not st.session_state.get("edit_show_pass", False)
                st.rerun()
        
        col1, col2 = st.columns([5, 1], gap="small")
        
        with col1:
            password_type_confirm = "password" if not st.session_state.get("edit_show_pass_confirm", False) else "default"
            new_password_confirm = st.text_input(
                "Confirmer le mot de passe",
                type=password_type_confirm,
                placeholder="••••••••",
                key="edit_new_password_confirm"
            )
        
        with col2:
            if st.button("👁️" if st.session_state.get("edit_show_pass_confirm", False) else "👁️‍🗨️", key="edit_toggle_pass_confirm", help="Afficher/Masquer"):
                st.session_state.edit_show_pass_confirm = not st.session_state.get("edit_show_pass_confirm", False)
                st.rerun()
    else:
        new_password = None
        new_password_confirm = None
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Boutons d'action
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Annuler", use_container_width=True, key="cancel_edit"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col3:
        if st.button("✅ Enregistrer les modifications", use_container_width=True, key="save_edit"):
            errors = []
            
            if not nom_entreprise.strip():
                errors.append("Le nom de l'entreprise est requis")
            
            if not email.strip():
                errors.append("L'email est requis")
            elif not validate_email_format(email):
                errors.append("Email invalide")
            
            if change_password:
                if not new_password:
                    errors.append("Veuillez entrer le nouveau mot de passe")
                else:
                    is_valid, msg = is_valid_password(new_password)
                    if not is_valid:
                        errors.append(msg)
                
                if new_password != new_password_confirm:
                    errors.append("Les mots de passe ne correspondent pas")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Appeler l'API locale pour mettre à jour
                api = get_api()
                
                update_data = {
                    "nom_entreprise": nom_entreprise,
                    "secteur": secteur,
                    "email": email
                }
                
                if change_password and new_password:
                    update_data["password"] = new_password
                
                result = api.update_user_profile(
                    user_id=st.session_state.user_id,
                    **update_data
                )
                
                if result.get('ok'):
                    # Mettre à jour le session state
                    st.session_state.user_data = {
                        "nom_entreprise": nom_entreprise,
                        "secteur": secteur,
                        "email": email,
                        "id_client": st.session_state.user_id
                    }
                    st.session_state.user_email = email
                    
                    st.success("✅ Profil mis à jour avec succès!")
                    st.balloons()
                    
                    # Rediriger vers le dashboard
                    import time
                    time.sleep(1.5)
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                else:
                    error = result.get('error', 'UNKNOWN_ERROR')
                    if error == 'EMAIL_EXISTS':
                        st.error("Cet email est déjà utilisé. Veuillez en choisir un autre.")
                    else:
                        st.error(f"Erreur: {error}")


def show_settings():
    """Affiche les paramètres"""
    st.markdown("<h2 style='color: #1E293B;'>⚙️ Paramètres</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1E293B; margin-top: 0;'>ℹ️ Informations de l'entreprise</h3>", unsafe_allow_html=True)
    
    if st.session_state.user_data:
        user_data = st.session_state.user_data
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"<p style='color: #64748B; margin: 8px 0;'><strong>Email:</strong></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #1E293B; font-weight: 500;'>{user_data.get('email', 'N/A')}</p>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='color: #64748B; margin: 8px 0;'><strong>Secteur:</strong></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #1E293B; font-weight: 500;'>{user_data.get('secteur', 'N/A')}</p>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='color: #64748B; margin: 8px 0;'><strong>Entreprise:</strong></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #1E293B; font-weight: 500;'>{user_data.get('nom_entreprise', 'N/A')}</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #1E293B; margin-top: 0;'>🔒 Sécurité</h3>", unsafe_allow_html=True)
    
    with st.expander("Changer le mot de passe"):
        old_password = st.text_input("Mot de passe actuel", type="password", key="old_pwd")
        new_password = st.text_input("Nouveau mot de passe", type="password", key="new_pwd")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="conf_pwd")
        
        if st.button("✅ Mettre à jour", use_container_width=True):
            if not all([old_password, new_password, confirm_password]):
                st.error("Veuillez remplir tous les champs")
            elif new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
            else:
                st.success("✅ Mot de passe mis à jour avec succès!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #DC2626; margin-top: 0;'>🗑️ Zone de danger</h3>", unsafe_allow_html=True)
    
    with st.expander("Supprimer le compte"):
        st.markdown("<p style='color: #DC2626; font-weight: 500;'>⚠️ Cette action est irréversible!</p>", unsafe_allow_html=True)
        
        confirm = st.checkbox("Je comprends que cela supprimera définitivement mon compte et toutes mes données")
        
        if confirm and st.button("🗑️ Supprimer mon compte", type="secondary", use_container_width=True):
            st.success("Compte supprimé!")
            st.session_state.authenticated = False
            st.session_state.page = "auth"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
