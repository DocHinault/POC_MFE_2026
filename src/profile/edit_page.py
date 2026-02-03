"""Page d'édition du profil"""
import streamlit as st
from config import SECTEURS
from src.auth.validation import validate_email_format, is_valid_password
from src.helpers import get_api


def show_edit_profile():
    """Page d'édition du profil"""
    # Ajouter du CSS pour fixer les selectbox en mode jour/nuit
    st.markdown("""
    <style>
    /* Selectbox styling */
    [data-baseweb="select"] {
        color: inherit !important;
    }
    [data-baseweb="select"] > div {
        color: inherit !important;
    }
    [data-testid="stSelectboxBaseRoot"] {
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='margin-bottom: 2rem;'>✏️ Modifier le profil</h2>", unsafe_allow_html=True)
    
    # Bouton Retour au-dessus
    if st.button("← Retour", use_container_width=True, key="back_profile"):
        st.session_state.current_page = "profile"
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Récupérer les données actuelles
    user_data = st.session_state.user_data
    
    # Section 1: Informations entreprise
    st.markdown("<h3>📋 Informations entreprise</h3>", unsafe_allow_html=True)
    
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Section 2: Email et sécurité
    st.markdown("<h3>🔐 Email et sécurité</h3>", unsafe_allow_html=True)
    
    email = st.text_input(
        "Adresse email",
        placeholder="vous@example.com",
        value=user_data.get("email", ""),
        key="edit_email"
    )
    
    st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.875rem; font-weight: 600; margin: 0 0 1rem 0;'>Modifier le mot de passe</p>", unsafe_allow_html=True)
    
    change_password = st.checkbox("Modifier mon mot de passe", key="edit_change_pwd")
    
    if change_password:
        new_password = st.text_input(
            "Nouveau mot de passe",
            type="password",
            placeholder="••••••••",
            key="edit_new_password"
        )
        
        new_password_confirm = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            placeholder="••••••••",
            key="edit_new_password_confirm"
        )
    else:
        new_password = None
        new_password_confirm = None
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Boutons d'action - responsive
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        if st.button("← Annuler", use_container_width=True, key="cancel_edit"):
            st.session_state.current_page = "profile"
            st.rerun()
    
    with col2:
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
                    "nom_entreprise": nom_entreprise.strip(),
                    "secteur": secteur,
                    "email": email.strip()
                }
                
                if change_password and new_password:
                    update_data["password"] = new_password
                
                print(f"🔍 DEBUG - Tentative d'update avec user_id={st.session_state.user_id}")
                print(f"🔍 DEBUG - Données: {update_data}")
                
                # Important: passer user_id en tant que user_id, pas id_client
                result = api.update_user_profile(
                    user_id=st.session_state.user_id,
                    **update_data
                )
                
                print(f"🔍 DEBUG - Résultat API: {result}")
                
                if result.get('ok'):
                    # Mettre à jour le session state
                    st.session_state.user_data = {
                        "nom_entreprise": nom_entreprise.strip(),
                        "secteur": secteur,
                        "email": email.strip(),
                        "id_client": st.session_state.user_id
                    }
                    st.session_state.user_email = email.strip()
                    
                    st.success("✅ Profil mis à jour avec succès!")
                    st.balloons()
                    
                    # Rediriger vers le dashboard
                    import time
                    time.sleep(1.5)
                    st.session_state.current_page = "profile"
                    st.rerun()
                else:
                    error = result.get('error', 'UNKNOWN_ERROR')
                    if error == 'EMAIL_EXISTS':
                        st.error("Cet email est déjà utilisé. Veuillez en choisir un autre.")
                    elif error == 'UPDATE_FAILED':
                        st.error("La mise à jour a échoué. Veuillez vérifier que vous avez modifié au moins un champ.")
                    else:
                        st.error(f"Erreur: {error}")
