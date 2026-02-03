"""Dashboard principal P1 - Page d'accueil après authentification"""
import streamlit as st
from src.ui.styles import get_custom_css
from src.profile.profile_page import show_profile_tab
from src.profile.edit_page import show_edit_profile


def page_p1():
    """Page P1 - Dashboard principal"""
    st.set_page_config(page_title="POC-MFE-2026 - Dashboard", layout="wide")
    
    # Initialiser le mode sombre dans session_state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    # Appliquer le CSS personnalisé
    st.markdown(get_custom_css(dark_mode=st.session_state.dark_mode), unsafe_allow_html=True)
    
    # Déterminer les couleurs selon le mode
    if st.session_state.dark_mode:
        header_bg = "#1A1F2E"
        header_border = "#374151"
        title_color = "#F59E0B"
        subtitle_color = "#94A3B8"
    else:
        header_bg = "linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)"
        header_border = "#E2E8F0"
        title_color = "#2563EB"
        subtitle_color = "#64748B"
    
    # Header professionnel avec toggle
    st.markdown(f"""
    <div style='background: {header_bg}; border-bottom: 1px solid {header_border}; padding: 1.5rem 2rem; margin: -1rem -1rem 2rem -1rem;'>
        <div style='display: flex; align-items: center; justify-content: space-between; max-width: 1400px; margin: 0 auto;'>
            <div style='display: flex; align-items: center; gap: 0.75rem;'>
                <span style='font-size: 2rem;'>📊</span>
                <h1 style='margin: 0; color: {title_color}; font-size: 1.75rem;'>POC-MFE-2026</h1>
                <span style='color: {subtitle_color}; font-size: 0.875rem; margin-left: 1rem;'>Social Media Dashboard</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle jour/nuit + Navigation
    col_toggle, col1, col2, col3, col_spacer, col_logout = st.columns([0.5, 1.2, 1.2, 1.2, 2.5, 1])
    
    with col_toggle:
        if st.session_state.dark_mode:
            if st.button("🌙", key="toggle_dark_dashboard"):
                st.session_state.dark_mode = False
                st.rerun()
        else:
            if st.button("☀️", key="toggle_light_dashboard"):
                st.session_state.dark_mode = True
                st.rerun()
    
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
    elif st.session_state.current_page == "edit_profile":
        show_edit_profile()
    elif st.session_state.current_page == "linking":
        show_linking_tab()
    elif st.session_state.current_page == "analysis":
        show_analysis_tab()


def show_linking_tab():
    """Onglet Liaison - Connecter Instagram et Facebook"""
    from pages.page_social_linking import page_social_linking
    page_social_linking()


def show_analysis_tab():
    """Onglet Analyse - Analyser et générer rapports"""
    st.markdown("""
    <h2 style='margin-bottom: 2rem;'>📈 Analyse & Recommandations</h2>
    """, unsafe_allow_html=True)
    
    # Vérifier si des comptes sont liés
    from social_auth import SocialMediaLinkManager
    manager = SocialMediaLinkManager()
    linked_accounts = manager.get_linked_accounts(st.session_state.user_id)
    
    if not linked_accounts:
        st.markdown("""
        <div style='text-align: center; padding: 3rem 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔐</div>
            <p style='font-size: 1.1rem; margin: 0.5rem 0; font-weight: 500; opacity: 0.8;'>Aucun compte lié</p>
            <p style='font-size: 0.95rem; margin: 0; opacity: 0.6;'>Connectez vos comptes Instagram et Facebook pour activer l'analyse</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Afficher les options d'analyse
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
            <span style='font-size: 1.5rem; margin-right: 0.75rem;'>📊</span>
            <h3 style='margin: 0;'>Pipeline d'analyse</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style='opacity: 0.8; margin-bottom: 1.5rem;'>
    Lancez l'analyse complète de vos performances sociales du dernier mois. 
    Le système va:
    </p>
    
    <ul style='opacity: 0.8; line-height: 1.8;'>
        <li>📊 Récupérer tous les KPI de vos comptes</li>
        <li>💾 Sauvegarder les données dans Google Sheet</li>
        <li>🤖 Utiliser l'IA (GPT) pour analyser les performances</li>
        <li>📄 Générer un PowerPoint professionnel</li>
        <li>📧 Envoyer le rapport par email avec recommandations</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Afficher les comptes liés
    st.markdown("""
    <h3 style='margin-top: 0;'>Comptes connectés</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    if 'instagram' in linked_accounts:
        with col1:
            st.markdown(f"""
            <div style='padding: 1rem; background: rgba(232, 121, 249, 0.1); border-radius: 8px; border-left: 4px solid #E879F9;'>
                <p style='margin: 0 0 0.5rem 0; font-size: 0.875rem; opacity: 0.7;'>Instagram</p>
                <p style='margin: 0; font-weight: 600;'>@{linked_accounts['instagram'].get('username', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if 'facebook' in linked_accounts or 'facebook_pages' in linked_accounts:
        with col2:
            pages = linked_accounts.get('facebook_pages', [])
            if pages:
                pages_text = f"{len(pages)} page(s)"
                st.markdown(f"""
                <div style='padding: 1rem; background: rgba(24, 119, 242, 0.1); border-radius: 8px; border-left: 4px solid #1877F2;'>
                    <p style='margin: 0 0 0.5rem 0; font-size: 0.875rem; opacity: 0.7;'>Facebook</p>
                    <p style='margin: 0; font-weight: 600;'>{pages_text}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
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
                            st.info("📧 Le rapport a été envoyé à l'adresse de reporting interne")
                        if result['powerpoint_path']:
                            st.info(f"📄 PowerPoint généré: {result['powerpoint_path']}")
                    else:
                        st.warning(f"⚠️ L'analyse a eu des problèmes: {', '.join(result['errors'])}")
                        if result['powerpoint_path']:
                            st.info(f"Un rapport partiel a été généré: {result['powerpoint_path']}")
                        
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
