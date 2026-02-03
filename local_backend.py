"""
Client API local - remplace AppsScriptAPI
Appelle directement les fonctions Python au lieu de passer par HTTP
"""

from typing import Dict, Any
import backend_service
from config import GOOGLE_SHEETS_ID


class LocalBackendAPI:
    """
    Client API local qui remplace AppsScriptAPI
    Appelle les fonctions Python directement - BEAUCOUP plus rapide!
    """
    
    def __init__(self, pepper_secret: str):
        """
        Initialise le client
        
        Args:
            pepper_secret: Clé secrète pour PBKDF2
        """
        self.pepper_secret = pepper_secret
    
    def health_check(self) -> bool:
        """Vérifie la santé du backend"""
        return True
    
    def register_start(self, email: str, password: str, nom_entreprise: str, secteur: str) -> dict:
        """
        Lance l'inscription
        """
        return backend_service.register_start(email, password, nom_entreprise, secteur, self.pepper_secret)
    
    def register_verify(self, email: str, code: str) -> dict:
        """
        Vérifie le code et crée le compte
        """
        return backend_service.register_verify(email, code, self.pepper_secret)
    
    def login(self, email: str, password: str) -> dict:
        """
        Authentifie un utilisateur
        """
        return backend_service.login(email, password, self.pepper_secret)
    
    def oauth_init(self, email: str, provider: str) -> dict:
        """
        Initialise une connexion OAuth
        """
        return backend_service.oauth_init(email, provider)
    
    def oauth_status(self, email: str) -> dict:
        """
        Récupère le statut OAuth
        """
        return backend_service.oauth_status(email)
