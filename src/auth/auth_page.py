"""Page d'authentification - Connexion ou Inscription"""
import streamlit as st
from src.ui.styles import configure_page_style, get_custom_css


def page_auth():
    """Page d'authentification - Connexion ou Inscription"""
    st.set_page_config(page_title="POC-MFE-2026 - Social Media Reporting", layout="centered")
    
    # Initialiser le mode sombre dans session_state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Si on est sur une sous-page (signup/login/confirm), ne pas afficher le toggle ici
    # car ces pages ont leur propre toggle
    if st.session_state.get("auth_mode") in ["signup", "login", "confirm"]:
        # Déléguer directement aux sous-pages
        if st.session_state.get("auth_mode") == "signup":
            from src.auth.signup_page import page_registration
            page_registration()
        elif st.session_state.get("auth_mode") == "login":
            from src.auth.login_page import page_login
            page_login()
        elif st.session_state.get("auth_mode") == "confirm":
            from src.auth.confirmation_page import page_confirmation
            page_confirmation()
        return
    
    # Header avec toggle jour/nuit (uniquement sur la page d'accueil)
    header_col1, header_col2 = st.columns([4, 1])
    with header_col2:
        if st.session_state.dark_mode:
            if st.button("🌙", key="toggle_dark_auth"):
                st.session_state.dark_mode = False
                st.rerun()
        else:
            if st.button("☀️", key="toggle_light_auth"):
                st.session_state.dark_mode = True
                st.rerun()
    
    # Appliquer le CSS personnalisé
    st.markdown(get_custom_css(dark_mode=st.session_state.dark_mode), unsafe_allow_html=True)
    
    # Déterminer les couleurs selon le mode
    if st.session_state.dark_mode:
        logo_color = "#F59E0B"
        subtitle_color = "#94A3B8"
        desc_color = "#CBD5E1"
    else:
        logo_color = "#1E3A8A"
        subtitle_color = "#64748B"
        desc_color = "#475569"
    
    # En-tête avec logo
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; margin: 40px 0 20px 0;'>
            <h1 style='color: {logo_color}; font-size: 3rem; margin-bottom: 8px; font-weight: 800;'>
                📊 POC-MFE-2026
            </h1>
            <p style='color: {subtitle_color}; font-size: 18px; font-weight: 500; margin-bottom: 0;'>
                Social Media Reporting Platform
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Boutons d'authentification avec meilleure structure
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        if st.button("📝 Créer un compte", use_container_width=True, key="btn_signup"):
            st.session_state.auth_mode = "signup"
            st.rerun()
        st.markdown(f"<p style='text-align: center; color: {subtitle_color}; font-size: 12px; margin-top: 8px;'><em>Créez votre profil pour démarrer</em></p>", unsafe_allow_html=True)
    
    with col2:
        if st.button("🔑 Se connecter", use_container_width=True, key="btn_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
        st.markdown(f"<p style='text-align: center; color: {subtitle_color}; font-size: 12px; margin-top: 8px;'><em>Accédez à votre compte</em></p>", unsafe_allow_html=True)
    
    # Page d'accueil avec description complète
    st.markdown(f"""
    <div style='text-align: center; padding: 60px 20px 40px 20px; max-width: 600px; margin: 0 auto;'>
        <h3 style='color: {logo_color}; margin-bottom: 20px; font-size: 1.5rem;'>
            Bienvenue sur POC-MFE-2026
            </h3>
            <p style='color: {desc_color}; font-size: 16px; line-height: 1.8; margin-bottom: 20px;'>
                Votre plateforme tout-en-un pour gérer et analyser vos réseaux sociaux Instagram et Facebook.
            </p>
            <div style='background: {'#252C3A' if st.session_state.dark_mode else '#F8FAFC'}; 
                        padding: 24px; 
                        border-radius: 12px; 
                        margin-top: 32px;
                        border-left: 4px solid {logo_color};'>
                <p style='color: {subtitle_color}; font-size: 14px; line-height: 1.6; text-align: left; margin: 0;'>
                    ✨ <strong>Connectez</strong> vos comptes sociaux en toute sécurité<br>
                    📊 <strong>Analysez</strong> vos performances avec des KPI détaillés<br>
                    📈 <strong>Générez</strong> des rapports automatiques personnalisés<br>
                    ⚡ <strong>Optimisez</strong> votre stratégie marketing en temps réel
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
