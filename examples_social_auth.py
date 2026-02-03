"""
Exemples d'utilisation de la liaison des comptes sociaux
"""

from social_auth import SocialMediaAuthenticator, SocialMediaLinkManager
import streamlit as st


# ============================================================================
# EXEMPLE 1: Récupérer les comptes disponibles
# ============================================================================

def exemple_recuperer_comptes_disponibles():
    """
    Récupère tous les comptes Instagram et pages Facebook disponibles
    après une connexion OAuth réussie
    """
    authenticator = SocialMediaAuthenticator()
    
    # Supposons que nous avons un token d'accès (obtenu via OAuth)
    access_token = "VOTRE_TOKEN_ICI"
    
    # Récupérer les comptes Instagram Business
    instagram_accounts = authenticator.get_instagram_business_accounts(access_token)
    print("Comptes Instagram Business disponibles:")
    for account in instagram_accounts:
        print(f"  - @{account['username']} ({account['followers_count']} followers)")
    
    # Récupérer les pages Facebook
    facebook_pages = authenticator.get_facebook_pages(access_token)
    print("\nPages Facebook disponibles:")
    for page in facebook_pages:
        print(f"  - {page['name']} ({page.get('fan_count', 0)} fans)")


# ============================================================================
# EXEMPLE 2: Lier un compte Instagram
# ============================================================================

def exemple_lier_instagram():
    """Exemple de liaison d'un compte Instagram"""
    
    manager = SocialMediaLinkManager()
    
    instagram_data = {
        'id': '123456789',
        'username': 'my_instagram_handle',
        'name': 'My Display Name',
        'followers_count': 10500,
        'media_count': 145,
        'access_token': 'IGQVJf...'  # Le token d'accès récupéré via OAuth
    }
    
    user_id = 'user_123'
    success, message = manager.link_instagram_account(user_id, instagram_data)
    
    if success:
        print(message)  # ✅ Compte Instagram @my_instagram_handle lié avec succès!
    else:
        print(f"Erreur: {message}")


# ============================================================================
# EXEMPLE 3: Lier des pages Facebook
# ============================================================================

def exemple_lier_facebook_pages():
    """Exemple de liaison de pages Facebook"""
    
    manager = SocialMediaLinkManager()
    user_id = 'user_123'
    
    # Lier la première page
    page_data_1 = {
        'id': '987654321',
        'name': 'My Business Page',
        'fan_count': 5200,
        'followers_count': 3100,
        'access_token': 'EAABsZC...'
    }
    
    success, message = manager.link_facebook_page(user_id, page_data_1)
    print(message)
    
    # Lier une deuxième page
    page_data_2 = {
        'id': '111222333',
        'name': 'My Second Page',
        'fan_count': 2100,
        'followers_count': 1500,
        'access_token': 'EAABsZC...'
    }
    
    success, message = manager.link_facebook_page(user_id, page_data_2)
    print(message)


# ============================================================================
# EXEMPLE 4: Récupérer les comptes liés d'un utilisateur
# ============================================================================

def exemple_recuperer_comptes_lies():
    """Récupère tous les comptes liés d'un utilisateur"""
    
    manager = SocialMediaLinkManager()
    user_id = 'user_123'
    
    linked_accounts = manager.get_linked_accounts(user_id)
    
    print("\n=== Comptes liés de l'utilisateur ===\n")
    
    if 'instagram' in linked_accounts:
        ig = linked_accounts['instagram']
        print(f"📸 Instagram: @{ig['username']}")
        print(f"   Followers: {ig['followers_count']:,}")
        print(f"   Posts: {ig['media_count']}")
        print(f"   Lié le: {ig['linked_at']}")
    
    if 'facebook' in linked_accounts:
        fb = linked_accounts['facebook']
        print(f"\n👤 Facebook: {fb['name']}")
        print(f"   Email: {fb['email']}")
        print(f"   Lié le: {fb['linked_at']}")
    
    if 'facebook_pages' in linked_accounts:
        print(f"\n📄 Pages Facebook ({len(linked_accounts['facebook_pages'])})")
        for page in linked_accounts['facebook_pages']:
            print(f"   - {page['name']}")
            print(f"     Fans: {page['fans_count']:,}")
            print(f"     Followers: {page['followers_count']:,}")


# ============================================================================
# EXEMPLE 5: Récupérer les insights Instagram
# ============================================================================

def exemple_insights_instagram():
    """Récupère les analytiques d'un compte Instagram"""
    
    authenticator = SocialMediaAuthenticator()
    
    instagram_id = '123456789'
    access_token = 'IGQVJf...'
    
    insights = authenticator.get_instagram_insights(instagram_id, access_token)
    
    print("=== Insights Instagram ===\n")
    
    if 'data' in insights:
        for metric in insights['data']:
            metric_name = metric.get('name', 'Unknown')
            metric_value = metric.get('values', [{}])[0].get('value', 0)
            print(f"{metric_name}: {metric_value}")
    else:
        print("Erreur lors de la récupération des insights")
        print(insights)


# ============================================================================
# EXEMPLE 6: Récupérer les insights Facebook
# ============================================================================

def exemple_insights_facebook():
    """Récupère les analytiques d'une page Facebook"""
    
    authenticator = SocialMediaAuthenticator()
    
    page_id = '987654321'
    page_access_token = 'EAABsZC...'
    
    # Différentes métriques disponibles:
    metrics = [
        'page_views',          # Nombre de vue de la page
        'page_fans',           # Nombre de fans
        'page_engaged_users',  # Utilisateurs engagés
        'page_post_engagements' # Engagements sur les posts
    ]
    
    for metric in metrics:
        insights = authenticator.get_page_insights(
            page_id=page_id,
            page_access_token=page_access_token,
            metric=metric
        )
        
        print(f"\n{metric}:")
        if 'data' in insights:
            for data_point in insights['data']:
                print(f"  {data_point}")


# ============================================================================
# EXEMPLE 7: Délier un compte
# ============================================================================

def exemple_delier_compte():
    """Exemple de déliaison d'un compte"""
    
    manager = SocialMediaLinkManager()
    user_id = 'user_123'
    
    # Délier Instagram
    success, message = manager.unlink_account(user_id, 'instagram')
    print(message)
    
    # Délier Facebook
    success, message = manager.unlink_account(user_id, 'facebook')
    print(message)


# ============================================================================
# EXEMPLE 8: Délier une page Facebook spécifique
# ============================================================================

def exemple_delier_page_facebook():
    """Délier une page Facebook spécifique (garder les autres)"""
    
    manager = SocialMediaLinkManager()
    user_id = 'user_123'
    page_id = '987654321'  # L'ID de la page à délier
    
    success, message = manager.unlink_facebook_page(user_id, page_id)
    print(message)


# ============================================================================
# EXEMPLE 9: Utilisation complète dans Streamlit
# ============================================================================

def exemple_streamlit_complet():
    """
    Exemple complet d'intégration dans une page Streamlit
    (Ce code est déjà dans pages/page_social_linking.py)
    """
    
    st.title("🔗 Lier vos comptes sociaux")
    
    if 'user_id' not in st.session_state:
        st.warning("Vous devez être connecté")
        return
    
    user_id = st.session_state['user_id']
    manager = SocialMediaLinkManager()
    
    # Afficher les comptes liés
    linked = manager.get_linked_accounts(user_id)
    
    st.subheader("Comptes actuellement liés")
    if not linked:
        st.info("Aucun compte lié")
    else:
        # Afficher Instagram
        if 'instagram' in linked:
            st.success(f"✅ Instagram: @{linked['instagram']['username']}")
        
        # Afficher Facebook
        if 'facebook' in linked:
            st.success(f"✅ Facebook: {linked['facebook']['name']}")
        
        # Afficher les pages
        if 'facebook_pages' in linked:
            for page in linked['facebook_pages']:
                st.success(f"✅ Page: {page['name']}")
    
    # Bouton pour lier un nouveau compte
    if st.button("Ajouter un compte"):
        authenticator = SocialMediaAuthenticator()
        login_url = authenticator.get_facebook_login_url()
        st.markdown(f"[Se connecter]({login_url})")


# ============================================================================
# EXEMPLE 10: Créer un dashboard avec les données
# ============================================================================

def exemple_dashboard():
    """Exemple de dashboard affichant les données des comptes liés"""
    
    st.title("📊 Mon Dashboard Social Media")
    
    user_id = st.session_state['user_id']
    manager = SocialMediaLinkManager()
    
    linked = manager.get_linked_accounts(user_id)
    
    # Métriques globales
    col1, col2, col3 = st.columns(3)
    
    total_followers = 0
    total_pages = len(linked.get('facebook_pages', []))
    
    if 'instagram' in linked:
        total_followers += linked['instagram'].get('followers_count', 0)
    
    for page in linked.get('facebook_pages', []):
        total_followers += page.get('fans_count', 0)
    
    with col1:
        st.metric("Followers totaux", f"{total_followers:,}")
    
    with col2:
        st.metric("Pages gérées", total_pages)
    
    with col3:
        st.metric("Comptes connectés", len([k for k in linked if k != 'facebook_pages']))
    
    # Instagram
    if 'instagram' in linked:
        st.subheader("📸 Instagram")
        ig = linked['instagram']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", f"{ig['followers_count']:,}")
        col2.metric("Posts", ig['media_count'])
        col3.metric("Compte", f"@{ig['username']}")
    
    # Facebook Pages
    if 'facebook_pages' in linked:
        st.subheader("📄 Pages Facebook")
        for page in linked['facebook_pages']:
            with st.expander(f"📄 {page['name']}"):
                col1, col2 = st.columns(2)
                col1.metric("Fans", f"{page['fans_count']:,}")
                col2.metric("Followers", f"{page['followers_count']:,}")


if __name__ == "__main__":
    # Décommenter l'exemple à tester
    
    # exemple_recuperer_comptes_disponibles()
    # exemple_lier_instagram()
    # exemple_lier_facebook_pages()
    # exemple_recuperer_comptes_lies()
    # exemple_insights_instagram()
    # exemple_insights_facebook()
    # exemple_delier_compte()
    # exemple_delier_page_facebook()
    
    print("✅ Exemples disponibles. Décommenter la fonction à tester.")
