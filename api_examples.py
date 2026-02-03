"""
Exemples d'intégration API pour Facebook et Instagram
À utiliser pour la phase 2 du développement
"""

# ====== FACEBOOK API ======

def get_facebook_page_insights(access_token, page_id):
    """
    Récupère les insights d'une page Facebook
    
    Args:
        access_token (str): Token d'accès Facebook
        page_id (str): ID de la page Facebook
    
    Returns:
        dict: Données des insights
    """
    import requests
    
    url = f"https://graph.facebook.com/v18.0/{page_id}/insights"
    
    params = {
        'access_token': access_token,
        'metric': 'page_fans,page_engagement,page_impressions'
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Erreur Facebook API: {e}")
        return None


def get_facebook_post_data(access_token, page_id):
    """
    Récupère les données des posts d'une page Facebook
    
    Args:
        access_token (str): Token d'accès Facebook
        page_id (str): ID de la page Facebook
    
    Returns:
        dict: Données des posts avec engagement
    """
    import requests
    
    url = f"https://graph.facebook.com/v18.0/{page_id}/posts"
    
    params = {
        'access_token': access_token,
        'fields': 'message,created_time,type,story,permalink_url,shares,likes.summary(true),comments.summary(true)'
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Erreur Facebook API: {e}")
        return None


# ====== INSTAGRAM BUSINESS API ======

def get_instagram_business_insights(access_token, business_account_id):
    """
    Récupère les insights du compte Instagram Business
    
    Args:
        access_token (str): Token d'accès Instagram Business
        business_account_id (str): ID du compte Business
    
    Returns:
        dict: Données des insights (impressions, reach, followers_count)
    """
    import requests
    
    url = f"https://graph.instagram.com/v18.0/{business_account_id}/insights"
    
    params = {
        'access_token': access_token,
        'metric': 'impressions,reach,profile_views,follower_count,email_contacts,phone_call_clicks,text_message_clicks,get_directions_clicks,website_clicks'
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Erreur Instagram API: {e}")
        return None


def get_instagram_media_insights(access_token, business_account_id):
    """
    Récupère les données des media du compte Instagram Business
    
    Args:
        access_token (str): Token d'accès Instagram Business
        business_account_id (str): ID du compte Business
    
    Returns:
        dict: Données des media avec engagement
    """
    import requests
    
    url = f"https://graph.instagram.com/v18.0/{business_account_id}/media"
    
    params = {
        'access_token': access_token,
        'fields': 'id,caption,media_type,media_url,timestamp,like_count,comments_count,insights.metric(impressions,reach,engagement,saved)'
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Erreur Instagram API: {e}")
        return None


def get_instagram_follower_count(access_token, business_account_id):
    """
    Récupère le nombre de followers du compte Instagram Business
    
    Args:
        access_token (str): Token d'accès Instagram Business
        business_account_id (str): ID du compte Business
    
    Returns:
        dict: Nombre de followers
    """
    import requests
    
    url = f"https://graph.instagram.com/v18.0/{business_account_id}"
    
    params = {
        'access_token': access_token,
        'fields': 'followers_count,biography,website,profile_picture_url'
    }
    
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Erreur Instagram API: {e}")
        return None


# ====== ANALYSE ET AGRÉGATION ======

def aggregate_social_metrics(facebook_data, instagram_data):
    """
    Agrège les métriques de Facebook et Instagram
    
    Args:
        facebook_data (dict): Données Facebook
        instagram_data (dict): Données Instagram
    
    Returns:
        dict: Métriques agrégées
    """
    metrics = {
        'facebook': facebook_data or {},
        'instagram': instagram_data or {},
        'total_reach': 0,
        'total_engagement': 0,
        'total_followers': 0
    }
    
    # À implémenter en fonction des données retournées par les API
    
    return metrics


# ====== STOCKAGE DES TOKENS ======

def save_social_credentials(email, platform, credentials):
    """
    Sauvegarde les identifiants de réseau social
    
    Args:
        email (str): Email de l'utilisateur
        platform (str): 'facebook' ou 'instagram'
        credentials (dict): {access_token, account_id, ...}
    """
    from google_sheets import get_google_sheets_client
    
    try:
        client = get_google_sheets_client()
        # Sauvegarder dans une feuille dédiée "SocialCredentials"
        # Utiliser une clé de chiffrement pour les tokens sensibles
        pass
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")


# ====== NOTIFICATIONS ======

def send_social_connection_confirmation(user_email, platform):
    """
    Envoie une notification de confirmation de liaison
    Similaire à GitHub Codex liant à GitHub
    
    Args:
        user_email (str): Email de l'utilisateur
        platform (str): 'facebook' ou 'instagram'
    """
    # Implémenter notification email ou in-app
    message = f"Votre compte {platform} a été lié avec succès à votre application MG"
    print(f"[NOTIFICATION] {user_email}: {message}")
