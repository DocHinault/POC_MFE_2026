"""Page d'inscription"""
import streamlit as st
from src.ui.styles import get_custom_css
from src.auth.validation import validate_email_format, is_valid_password
from config import SECTEURS
from src.helpers import get_api


def page_registration():
    """Page d'inscription"""
    st.set_page_config(page_title="Inscription - POC-MFE-2026", layout="centered")
    
    # Initialiser temp_user_data si elle n'existe pas
    if "temp_user_data" not in st.session_state:
        st.session_state.temp_user_data = {}
    
    # Initialiser le mode sombre dans session_state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Header avec toggle jour/nuit
    header_col1, header_col2 = st.columns([4, 1])
    with header_col2:
        if st.session_state.dark_mode:
            if st.button("🌙", key="toggle_dark_signup"):
                st.session_state.dark_mode = False
                st.rerun()
        else:
            if st.button("☀️", key="toggle_light_signup"):
                st.session_state.dark_mode = True
                st.rerun()
    
    # Appliquer le CSS personnalisé
    st.markdown(get_custom_css(dark_mode=st.session_state.dark_mode), unsafe_allow_html=True)
    
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
    
    # Section 1: Informations entreprise (sans encadré)
    st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
        <span style='font-size: 1.5rem; margin-right: 0.75rem;'>📋</span>
        <h3 style='margin: 0;'>Informations entreprise</h3>
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Section 2: Identifiants (sans encadré)
    st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
        <span style='font-size: 1.5rem; margin-right: 0.75rem;'>🔐</span>
        <h3 style='margin: 0;'>Vos identifiants</h3>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input(
        "Adresse email",
        placeholder="vous@example.com",
        value=st.session_state.temp_user_data.get("email", ""),
        key="email"
    )
    
    st.markdown("<p style='font-size: 0.875rem; margin: 1rem 0 0.5rem 0;'><strong>Mot de passe</strong> <span style='color: #10B981;'>✓</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8rem; color: #78828F; margin: 0 0 0.5rem 0;'>Minimum 8 caractères • 1 majuscule • 1 chiffre</p>", unsafe_allow_html=True)
    
    # Champs de password avec type natif
    password = st.text_input(
        "Mot de passe",
        type="password",
        placeholder="••••••••",
        key="password"
    )
    
    password_confirm = st.text_input(
        "Confirmer le mot de passe",
        type="password",
        placeholder="••••••••",
        key="password_confirm"
    )
    
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
