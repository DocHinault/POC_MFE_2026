"""Page de confirmation par email"""
import streamlit as st
from src.ui.styles import get_custom_css
from src.helpers import get_api


def page_confirmation():
    """Page de confirmation par email"""
    st.set_page_config(page_title="Confirmation - POC-MFE-2026", layout="centered")
    
    # Initialiser le mode sombre dans session_state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Header avec toggle jour/nuit
    header_col1, header_col2 = st.columns([4, 1])
    with header_col2:
        if st.session_state.dark_mode:
            if st.button("🌙", key="toggle_dark_confirm"):
                st.session_state.dark_mode = False
                st.rerun()
        else:
            if st.button("☀️", key="toggle_light_confirm"):
                st.session_state.dark_mode = True
                st.rerun()
    
    # Appliquer le CSS personnalisé
    st.markdown(get_custom_css(dark_mode=st.session_state.dark_mode), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #1E293B; margin: 20px 0;'>✉️ Confirmation</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Vérifiez votre email</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <p style='font-size: 16px;'>Un code de confirmation a été envoyé à:</p>
        <p style='color: #F59E0B; font-weight: 600; font-size: 18px;'>{st.session_state.temp_user_data.get('email')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    code_input = st.text_input(
        "Entrez le code de confirmation",
        placeholder="000000",
        key="confirm_code",
        max_chars=6
    )
    
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
