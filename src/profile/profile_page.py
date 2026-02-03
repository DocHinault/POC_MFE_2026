"""Page de profil - Affichage des informations utilisateur"""
import streamlit as st


def show_profile_tab():
    """Onglet Profil - Affichage et édition des informations"""
    st.markdown("<h2 style='margin-bottom: 2rem;'>👤 Votre profil</h2>", unsafe_allow_html=True)
    
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
            user_data = st.session_state.user_data
            
            # Créer les lignes d'info
            email_val = user_data.get('email', 'N/A')
            entreprise_val = user_data.get('nom_entreprise', 'N/A')
            secteur_val = user_data.get('secteur', 'N/A')
            
            # Si vides, afficher N/A sinon afficher la valeur
            if not entreprise_val or entreprise_val.strip() == '':
                entreprise_val = 'N/A'
            if not secteur_val or secteur_val.strip() == '':
                secteur_val = 'N/A'
            
            st.markdown(f"""
<h3 style='margin-bottom: 1rem;'>Informations du compte</h3>
<div style='margin-bottom: 1.5rem;'>
    <p style='font-size: 0.875rem; margin: 0 0 0.25rem 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; opacity: 0.7;'>Email</p>
    <p style='font-size: 1rem; margin: 0; font-weight: 500;'>{email_val}</p>
</div>
<div style='margin-bottom: 1.5rem;'>
    <p style='font-size: 0.875rem; margin: 0 0 0.25rem 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; opacity: 0.7;'>Entreprise</p>
    <p style='font-size: 1rem; margin: 0; font-weight: 500;'>{entreprise_val}</p>
</div>
<div style='margin-bottom: 1.5rem;'>
    <p style='font-size: 0.875rem; margin: 0 0 0.25rem 0; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; opacity: 0.7;'>Secteur</p>
    <p style='font-size: 1rem; margin: 0; font-weight: 500;'>{secteur_val}</p>
</div>
            """, unsafe_allow_html=True)
            
            if st.button("✏️ Modifier le profil", use_container_width=True, key="edit_profile_btn"):
                st.session_state.current_page = "edit_profile"
                st.rerun()
