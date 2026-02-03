"""Authentification et liaison des comptes sociaux (Instagram, Facebook)"""
import requests
import json
import os
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
import backend_database

load_dotenv()

class SocialMediaAuthenticator:
    """Gestionnaire d'authentification pour Instagram et Facebook"""
    
    def __init__(self):
        self.facebook_app_id = os.getenv("FACEBOOK_APP_ID", "")
        self.facebook_app_secret = os.getenv("FACEBOOK_APP_SECRET", "")
        # Toujours forcer le slash final pour la redirection Facebook
        uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8501/")
        if not uri.endswith("/"):
            uri = uri + "/"
        self.redirect_uri = uri
        
    # ===== FACEBOOK / INSTAGRAM OAUTH =====
    
    def get_facebook_login_url(self) -> str:
        """Génère l'URL de connexion Facebook pour OAuth 2.0"""
        if not self.facebook_app_id:
            raise ValueError("FACEBOOK_APP_ID non configuré")
        
        permissions = [
            "instagram_basic",
            "instagram_business_basic",
            "pages_read_engagement",
            "pages_manage_metadata",
            "instagram_manage_insights"
        ]
        
        scope = ",".join(permissions)
        
        url = (
            f"https://www.facebook.com/v18.0/dialog/oauth?"
            f"client_id={self.facebook_app_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&scope={scope}"
            f"&response_type=code"
            f"&auth_type=rerequest"
        )
        return url
    
    def exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """Échange le code d'autorisation contre un token d'accès"""
        if not self.facebook_app_id or not self.facebook_app_secret:
            raise ValueError("Facebook credentials non configurées")
        
        token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        
        params = {
            "client_id": self.facebook_app_id,
            "client_secret": self.facebook_app_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        
        try:
            response = requests.post(token_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'échange de code: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Récupère les infos utilisateur Facebook"""
        url = "https://graph.facebook.com/v18.0/me"
        
        params = {
            "fields": "id,name,email,picture",
            "access_token": access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de l'utilisateur: {e}")
            return None
    
    def get_instagram_business_accounts(self, access_token: str) -> list:
        """Récupère les comptes Instagram Business liés"""
        url = "https://graph.facebook.com/v18.0/me"
        
        params = {
            "fields": "instagram_business_account{id,name,username,followers_count,media_count}",
            "access_token": access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "instagram_business_account" in data:
                return [data["instagram_business_account"]]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des comptes Instagram: {e}")
            return []
    
    def get_facebook_pages(self, access_token: str) -> list:
        """Récupère les pages Facebook liées"""
        url = "https://graph.facebook.com/v18.0/me/accounts"
        
        params = {
            "fields": "id,name,picture,fan_count,followers_count",
            "access_token": access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des pages Facebook: {e}")
            return []
    
    def get_page_insights(self, page_id: str, page_access_token: str, metric: str = "page_views") -> Dict:
        """Récupère les statistiques d'une page Facebook"""
        url = f"https://graph.facebook.com/v18.0/{page_id}/insights"
        
        params = {
            "metric": metric,
            "period": "day",
            "access_token": page_access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des insights: {e}")
            return {}
    
    def get_instagram_insights(self, instagram_id: str, access_token: str) -> Dict:
        """Récupère les statistiques d'un compte Instagram Business"""
        url = f"https://graph.instagram.com/v18.0/{instagram_id}/insights"
        
        params = {
            "metric": "impressions,reach,profile_views,follower_count",
            "period": "day",
            "access_token": access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des insights Instagram: {e}")
            return {}
    
    def refresh_long_lived_token(self, short_lived_token: str) -> Optional[Dict]:
        """Convertit un token court en token long (valide 60 jours)"""
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.facebook_app_id,
            "client_secret": self.facebook_app_secret,
            "fb_exchange_token": short_lived_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du refresh du token: {e}")
            return None


class SocialMediaLinkManager:
    """Gestionnaire de liaison des comptes sociaux à l'utilisateur"""
    
    def __init__(self):
        self.db = backend_database.get_database()
        self.authenticator = SocialMediaAuthenticator()
    
    def link_instagram_account(self, user_id: str, instagram_data: Dict) -> Tuple[bool, str]:
        """Lie un compte Instagram à l'utilisateur"""
        try:
            # Vérifier que les données requises sont présentes
            if not all(k in instagram_data for k in ['id', 'username']):
                return False, "Données Instagram incomplètes"
            
            # Récupérer l'utilisateur
            user = self.db.get_user(user_id)
            if not user:
                return False, "Utilisateur non trouvé"
            
            # Ajouter/mettre à jour les données Instagram
            if 'linked_accounts' not in user:
                user['linked_accounts'] = {}
            
            user['linked_accounts']['instagram'] = {
                'id': instagram_data['id'],
                'username': instagram_data['username'],
                'name': instagram_data.get('name', ''),
                'followers_count': instagram_data.get('followers_count', 0),
                'media_count': instagram_data.get('media_count', 0),
                'access_token': instagram_data.get('access_token', ''),
                'linked_at': str(__import__('datetime').datetime.now())
            }
            
            # Sauvegarder l'utilisateur
            self.db.update_user(user_id, user)
            
            return True, f"✅ Compte Instagram @{instagram_data['username']} lié avec succès!"
        
        except Exception as e:
            print(f"Erreur lors de la liaison Instagram: {e}")
            return False, f"Erreur: {str(e)}"
    
    def link_facebook_account(self, user_id: str, facebook_data: Dict) -> Tuple[bool, str]:
        """Lie un compte Facebook à l'utilisateur"""
        try:
            if not all(k in facebook_data for k in ['id', 'name']):
                return False, "Données Facebook incomplètes"
            
            user = self.db.get_user(user_id)
            if not user:
                return False, "Utilisateur non trouvé"
            
            if 'linked_accounts' not in user:
                user['linked_accounts'] = {}
            
            user['linked_accounts']['facebook'] = {
                'id': facebook_data['id'],
                'name': facebook_data['name'],
                'email': facebook_data.get('email', ''),
                'access_token': facebook_data.get('access_token', ''),
                'linked_at': str(__import__('datetime').datetime.now())
            }
            
            self.db.update_user(user_id, user)
            
            return True, f"✅ Compte Facebook {facebook_data['name']} lié avec succès!"
        
        except Exception as e:
            print(f"Erreur lors de la liaison Facebook: {e}")
            return False, f"Erreur: {str(e)}"
    
    def link_facebook_page(self, user_id: str, page_data: Dict) -> Tuple[bool, str]:
        """Lie une page Facebook à l'utilisateur"""
        try:
            if not all(k in page_data for k in ['id', 'name']):
                return False, "Données de page incomplètes"
            
            user = self.db.get_user(user_id)
            if not user:
                return False, "Utilisateur non trouvé"
            
            if 'linked_accounts' not in user:
                user['linked_accounts'] = {}
            
            if 'facebook_pages' not in user['linked_accounts']:
                user['linked_accounts']['facebook_pages'] = []
            
            # Vérifier si la page n'est pas déjà liée
            existing_pages = [p['id'] for p in user['linked_accounts']['facebook_pages']]
            if page_data['id'] in existing_pages:
                return False, "Cette page est déjà liée"
            
            user['linked_accounts']['facebook_pages'].append({
                'id': page_data['id'],
                'name': page_data['name'],
                'fans_count': page_data.get('fan_count', 0),
                'followers_count': page_data.get('followers_count', 0),
                'access_token': page_data.get('access_token', ''),
                'linked_at': str(__import__('datetime').datetime.now())
            })
            
            self.db.update_user(user_id, user)
            
            return True, f"✅ Page Facebook '{page_data['name']}' liée avec succès!"
        
        except Exception as e:
            print(f"Erreur lors de la liaison de la page: {e}")
            return False, f"Erreur: {str(e)}"
    
    def get_linked_accounts(self, user_id: str) -> Dict:
        """Récupère tous les comptes liés d'un utilisateur"""
        try:
            user = self.db.get_user(user_id)
            if not user:
                return {}
            
            return user.get('linked_accounts', {})
        except Exception as e:
            print(f"Erreur lors de la récupération des comptes liés: {e}")
            return {}
    
    def unlink_account(self, user_id: str, platform: str) -> Tuple[bool, str]:
        """Délie un compte social"""
        try:
            user = self.db.get_user(user_id)
            if not user:
                return False, "Utilisateur non trouvé"
            
            if 'linked_accounts' not in user:
                return False, f"Aucun compte {platform} lié"
            
            if platform in user['linked_accounts']:
                del user['linked_accounts'][platform]
                self.db.update_user(user_id, user)
                return True, f"✅ Compte {platform} délié avec succès!"
            
            return False, f"Aucun compte {platform} lié"
        
        except Exception as e:
            print(f"Erreur lors de la déliaison: {e}")
            return False, f"Erreur: {str(e)}"
    
    def unlink_facebook_page(self, user_id: str, page_id: str) -> Tuple[bool, str]:
        """Délie une page Facebook spécifique"""
        try:
            user = self.db.get_user(user_id)
            if not user:
                return False, "Utilisateur non trouvé"
            
            if 'linked_accounts' not in user or 'facebook_pages' not in user['linked_accounts']:
                return False, "Aucune page Facebook liée"
            
            pages = user['linked_accounts']['facebook_pages']
            new_pages = [p for p in pages if p['id'] != page_id]
            
            if len(new_pages) == len(pages):
                return False, "Cette page n'est pas liée"
            
            user['linked_accounts']['facebook_pages'] = new_pages
            self.db.update_user(user_id, user)
            
            return True, "✅ Page Facebook déliée avec succès!"
        
        except Exception as e:
            print(f"Erreur lors de la déliaison de la page: {e}")
            return False, f"Erreur: {str(e)}"
