"""Page de connexion"""
import streamlit as st
from src.ui.styles import get_custom_css
from src.auth.validation import validate_email_format
from src.helpers import get_api


def page_login():
    """Page de connexion"""
    st.set_page_config(page_title="Connexion - POC-MFE-2026", layout="centered")
    
    # Initialiser le mode sombre dans session_state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Header avec toggle jour/nuit
    header_col1, header_col2 = st.columns([4, 1])
    with header_col2:
        if st.session_state.dark_mode:
            if st.button("🌙", key="toggle_dark_login"):
                st.session_state.dark_mode = False
                st.rerun()
        else:
            if st.button("☀️", key="toggle_light_login"):
                st.session_state.dark_mode = True
                st.rerun()
    
    # Appliquer le CSS personnalisé
    st.markdown(get_custom_css(dark_mode=st.session_state.dark_mode), unsafe_allow_html=True)
    
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
    email = st.text_input("📧 Adresse email", placeholder="votre@email.com", key="login_email")
    
    password = st.text_input("🔒 Mot de passe", type="password", key="login_password")
    
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
                        "email": result.get('email', email),
                        "id_client": result.get('id_client'),
                        "nom_entreprise": result.get('nom_entreprise', ''),
                        "secteur": result.get('secteur', ''),
                        "id_fb": result.get('id_fb', ''),
                        "id_insta": result.get('id_insta', '')
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
