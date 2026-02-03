"""
Client pour l'API Google Apps Script
Communication sécurisée avec le backend Apps Script
"""

import requests
import json
from datetime import datetime
from config import APPS_SCRIPT_URL, API_KEY

class AppsScriptAPI:
    """Client pour communiquer avec l'API Apps Script"""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialise le client
        
        Args:
            base_url: URL de déploiement du Apps Script
            api_key: Clé API pour authentification
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = 120  # PBKDF2 peut prendre 60-90s sur Apps Script
    
    def _request(self, route: str, **kwargs) -> dict:
        """
        Effectue une requête à l'API
        
        Args:
            route: Route API (ex: 'login', 'register_start')
            **kwargs: Données supplémentaires à envoyer
        
        Returns:
            Réponse JSON ou erreur
        """
        try:
            payload = {
                'api_key': self.api_key,
                'route': route,
                **kwargs
            }
            
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Si l'API retourne un JSON mais avec 'ok': False, relayer l'erreur
            if not data.get('ok', True):
                return data
            
            return data
            
        except requests.exceptions.Timeout as e:
            return {
                'ok': False,
                'error': 'API_TIMEOUT',
                'details': f'Requête expirée après {self.timeout}s. L\'API Apps Script est lente ou l\'URL est incorrecte.'
            }
        except requests.exceptions.ConnectionError as e:
            return {
                'ok': False,
                'error': 'API_CONNECTION_ERROR',
                'details': f'Impossible de se connecter à {self.base_url}. Vérifiez l\'URL et votre connexion internet.'
            }
        except requests.exceptions.HTTPError as e:
            try:
                response_text = e.response.text
            except:
                response_text = str(e)
            return {
                'ok': False,
                'error': 'API_HTTP_ERROR',
                'status_code': e.response.status_code if hasattr(e, 'response') else None,
                'details': response_text
            }
        except requests.exceptions.RequestException as e:
            return {
                'ok': False,
                'error': 'API_REQUEST_ERROR',
                'details': str(e)
            }
        except ValueError as e:
            return {
                'ok': False,
                'error': 'API_JSON_ERROR',
                'details': f'Réponse invalide (JSON): {str(e)}'
            }
    
    def health_check(self) -> bool:
        """Vérifie la connexion avec l'API"""
        result = self._request('health')
        return result.get('ok', False)
    
    def register_start(self, email: str, password: str, nom_entreprise: str, secteur: str) -> dict:
        """
        Lance l'inscription
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair
            nom_entreprise: Nom de l'entreprise
            secteur: Secteur d'activité
        
        Returns:
            {'ok': bool, ...}
        """
        return self._request(
            'register_start',
            email=email,
            password=password,
            nom_entreprise=nom_entreprise,
            secteur=secteur
        )
    
    def register_verify(self, email: str, code: str) -> dict:
        """
        Vérifie le code de confirmation
        
        Args:
            email: Email de l'utilisateur
            code: Code de confirmation (6 caractères)
        
        Returns:
            {'ok': bool, 'id_client': str, ...}
        """
        return self._request(
            'register_verify',
            email=email,
            code=code
        )
    
    def login(self, email: str, password: str) -> dict:
        """
        Authentifie l'utilisateur
        
        Args:
            email: Email
            password: Mot de passe en clair
        
        Returns:
            {'ok': bool, 'id_client': str, 'email': str, ...}
        """
        return self._request(
            'login',
            email=email,
            password=password
        )
    
    def oauth_init(self, email: str, provider: str) -> dict:
        """
        Initie le flux OAuth
        
        Args:
            email: Email de l'utilisateur
            provider: 'facebook' ou 'instagram'
        
        Returns:
            {'ok': bool, 'authUrl': str, ...}
        """
        return self._request(
            'oauth_init',
            email=email,
            provider=provider
        )
    
    def oauth_status(self, email: str) -> dict:
        """
        Récupère le statut des liaisons OAuth
        
        Args:
            email: Email de l'utilisateur
        
        Returns:
            {'ok': bool, 'facebookLinked': bool, 'instagramLinked': bool, ...}
        """
        return self._request(
            'oauth_status',
            email=email
        )


# Instance globale
if APPS_SCRIPT_URL and API_KEY:
    api_client = AppsScriptAPI(APPS_SCRIPT_URL, API_KEY)
else:
    api_client = None


def get_api_client() -> AppsScriptAPI:
    """Récupère l'instance du client API"""
    if not api_client:
        raise ValueError("APPS_SCRIPT_URL ou API_KEY non configuré dans .env")
    return api_client
