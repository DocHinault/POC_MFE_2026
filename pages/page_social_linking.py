"""Page de liaison des comptes sociaux"""
import streamlit as st
import os
from urllib.parse import parse_qs, urlparse
from social_auth import SocialMediaAuthenticator, SocialMediaLinkManager

def page_social_linking():
    """Page pour lier les comptes Instagram et Facebook"""
    
    st.title("🔗 Lier vos comptes sociaux")
    st.write("Connectez votre compte Instagram ou Facebook pour afficher votre dashboard")
    
    # Vérifier que l'utilisateur est connecté
    if not st.session_state.get('user_id'):
        st.warning("⚠️ Vous devez être connecté pour lier vos comptes sociaux")
        st.stop()
    
    user_id = st.session_state['user_id']
    manager = SocialMediaLinkManager()
    
    # Afficher les comptes déjà liés
    st.subheader("📊 Vos comptes liés")
    linked_accounts = manager.get_linked_accounts(user_id)
    
    if linked_accounts:
        col1, col2 = st.columns(2)
        
        # Instagram
        if 'instagram' in linked_accounts:
            with col1:
                st.success("✅ Instagram lié")
                instagram = linked_accounts['instagram']
                st.write(f"👤 **@{instagram['username']}**")
                st.write(f"📱 Followers: {instagram.get('followers_count', 0):,}")
                st.write(f"📸 Posts: {instagram.get('media_count', 0)}")
                
                if st.button("🔌 Délier Instagram", key="unlink_ig"):
                    success, message = manager.unlink_account(user_id, 'instagram')
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        # Facebook
        if 'facebook' in linked_accounts:
            with col2:
                st.success("✅ Facebook lié")
                facebook = linked_accounts['facebook']
                st.write(f"👤 **{facebook['name']}**")
                if facebook.get('email'):
                    st.write(f"📧 {facebook['email']}")
        
        # Facebook Pages
        if 'facebook_pages' in linked_accounts and linked_accounts['facebook_pages']:
            st.subheader("📄 Vos pages Facebook")
            for page in linked_accounts['facebook_pages']:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📄 **{page['name']}**")
                    st.caption(f"👥 {page.get('fans_count', 0):,} fans")
                with col2:
                    if st.button("🗑️", key=f"unlink_page_{page['id']}"):
                        success, message = manager.unlink_facebook_page(user_id, page['id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    else:
        st.info("ℹ️ Aucun compte social lié pour le moment")
    
    # Separator
    st.divider()
    
    # Section pour lier de nouveaux comptes
    st.subheader("➕ Ajouter un compte")
    
    tab1, tab2 = st.tabs(["Instagram", "Facebook"])
    
    with tab1:
        st.write("### Connecter votre compte Instagram Business")
        st.info(
            "💡 Vous devez avoir un compte Instagram Business pour pouvoir le connecter. "
            "Les comptes personnels ne sont pas supportés."
        )
        
        if st.button("🔐 Se connecter avec Instagram", key="login_ig", use_container_width=True):
            try:
                authenticator = SocialMediaAuthenticator()
                login_url = authenticator.get_facebook_login_url()
                st.write("👇 Cliquez sur le lien ci-dessous pour vous connecter:")
                st.markdown(f"[Connecter Instagram]({login_url})")
                st.session_state['awaiting_oauth'] = True
            except ValueError as e:
                st.error(f"❌ Configuration manquante: {e}")
        
        st.markdown("""
        **Après la connexion:**
        1. Acceptez les permissions demandées
        2. Vous serez redirigé et vos données seront importées automatiquement
        """)
    
    with tab2:
        st.write("### Connecter vos pages Facebook")
        st.info(
            "💡 Vous pouvez connecter plusieurs pages Facebook. "
            "Assurez-vous d'être administrateur des pages que vous souhaitez connecter."
        )
        
        if st.button("🔐 Se connecter avec Facebook", key="login_fb", use_container_width=True):
            try:
                authenticator = SocialMediaAuthenticator()
                login_url = authenticator.get_facebook_login_url()
                st.write("👇 Cliquez sur le lien ci-dessous pour vous connecter:")
                st.markdown(f"[Connecter Facebook]({login_url})")
                st.session_state['awaiting_oauth'] = True
            except ValueError as e:
                st.error(f"❌ Configuration manquante: {e}")
        
        st.markdown("""
        **Après la connexion:**
        1. Acceptez les permissions demandées
        2. Sélectionnez les pages que vous souhaitez ajouter
        3. Les données seront importées automatiquement
        """)
    
    # Gérer le callback OAuth
    handle_oauth_callback(user_id, manager)


def handle_oauth_callback(user_id: str, manager: SocialMediaLinkManager):
    """Gère le callback de l'authentification OAuth"""
    
    # Vérifier si on a un code d'autorisation dans l'URL
    query_params = st.query_params
    
    if 'code' in query_params:
        code = query_params['code']
        
        try:
            authenticator = SocialMediaAuthenticator()
            
            # Échanger le code contre un token
            token_response = authenticator.exchange_code_for_token(code)
            
            if not token_response:
                st.error("❌ Erreur lors de l'échange du token")
                return
            
            access_token = token_response.get('access_token')
            
            # Récupérer les infos utilisateur
            user_info = authenticator.get_user_info(access_token)
            
            if not user_info:
                st.error("❌ Erreur lors de la récupération des infos utilisateur")
                return
            
            # Récupérer les comptes Instagram
            instagram_accounts = authenticator.get_instagram_business_accounts(access_token)
            
            # Récupérer les pages Facebook
            facebook_pages = authenticator.get_facebook_pages(access_token)
            
            # Afficher les comptes disponibles et laisser l'utilisateur choisir
            st.session_state['oauth_data'] = {
                'user_info': user_info,
                'access_token': access_token,
                'instagram_accounts': instagram_accounts,
                'facebook_pages': facebook_pages
            }
            
            show_oauth_selection(user_id, manager)
        
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement OAuth: {e}")
    
    elif 'error' in query_params:
        error = query_params['error']
        error_description = query_params.get('error_description', 'Erreur inconnue')
        st.error(f"❌ {error}: {error_description}")


def show_oauth_selection(user_id: str, manager: SocialMediaLinkManager):
    """Affiche la sélection des comptes/pages à lier"""
    
    if 'oauth_data' not in st.session_state:
        return
    
    oauth_data = st.session_state['oauth_data']
    
    st.subheader("🔗 Sélectionnez les comptes à lier")
    
    # Instagram
    if oauth_data['instagram_accounts']:
        st.write("### Instagram Business")
        for account in oauth_data['instagram_accounts']:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"👤 @{account.get('username', 'Unknown')}")
                st.caption(f"📱 {account.get('followers_count', 0):,} followers")
            with col2:
                if st.button("Lier", key=f"select_ig_{account['id']}", use_container_width=True):
                    # Ajouter le token d'accès aux données
                    account['access_token'] = oauth_data['access_token']
                    success, message = manager.link_instagram_account(user_id, account)
                    
                    if success:
                        st.success(message)
                        del st.session_state['oauth_data']
                        st.rerun()
                    else:
                        st.error(message)
    
    # Facebook Pages
    if oauth_data['facebook_pages']:
        st.write("### Pages Facebook")
        for page in oauth_data['facebook_pages']:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"📄 {page.get('name', 'Unknown')}")
                st.caption(f"👥 {page.get('fan_count', 0):,} fans")
            with col2:
                if st.button("Lier", key=f"select_fb_{page['id']}", use_container_width=True):
                    # Ajouter le token d'accès aux données
                    page['access_token'] = oauth_data['access_token']
                    success, message = manager.link_facebook_page(user_id, page)
                    
                    if success:
                        st.success(message)
                        del st.session_state['oauth_data']
                        st.rerun()
                    else:
                        st.error(message)
    
    if st.button("❌ Annuler", use_container_width=True):
        del st.session_state['oauth_data']
        st.rerun()
