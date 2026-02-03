"""
Service principal - logique métier pour authentification
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import re

import backend_cache as cache
import backend_auth as auth
import backend_email as email_service
import backend_database as database


def validate_email(email: str) -> bool:
    """Valide le format d'un email"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """Valide un mot de passe (8+ chars, 1 majuscule, 1 chiffre)"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


def validate_secteur(secteur: str) -> bool:
    """Valide le secteur"""
    allowed = ['Influenceur', 'Salle de sport', 'Hôtellerie/Restauration']
    return secteur in allowed


def register_start(email: str, password: str, nom_entreprise: str, secteur: str, pepper: str) -> Dict[str, Any]:
    """
    Lance l'inscription (étape 1)
    
    Crée une entrée temporaire et envoie un code
    """
    # Validation
    if not validate_email(email):
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    if not validate_password(password):
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    if not nom_entreprise or not nom_entreprise.strip():
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    if not validate_secteur(secteur):
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    # Vérifier que l'email n'existe pas
    db = database.get_database()
    if db and db.find_client_by_email(email):
        return {'ok': False, 'error': 'EMAIL_EXISTS'}
    
    # Générer le hash du mot de passe
    password_hash = auth.hash_password(password, pepper)
    
    # Générer le code
    code = auth.generate_confirmation_code()
    code_salt, code_hash, code_iterations = auth.hash_code(code, pepper)
    
    # Sauvegarder dans le cache pendant 15 minutes
    pending_data = {
        'email': email,
        'nom_entreprise': nom_entreprise,
        'secteur': secteur,
        'password_hash': password_hash,
        'id_fb': '',
        'id_insta': '',
        'code_salt': code_salt,
        'code_hash': code_hash,
        'code_iterations': code_iterations,
        'created_at': datetime.now().isoformat()
    }
    cache.put(f'PENDING_{email}', pending_data, 15 * 60)
    
    # Envoyer l'email
    email_sent = email_service.send_confirmation_email(email, code)
    
    # En mode démo (si email non configuré), retourner le code
    response = {'ok': True}
    if not email_sent:
        print(f"⚠️ EMAIL NON CONFIGURÉ - Code de confirmation: {code}")
        response['demo_code'] = code  # Pour le test
    
    return response


def register_verify(email: str, code: str, pepper: str) -> Dict[str, Any]:
    """
    Vérifie le code et crée le compte (étape 2)
    """
    if not email or not code:
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    # Récupérer les données temporaires
    pending_data = cache.get(f'PENDING_{email}')
    if not pending_data:
        return {'ok': False, 'error': 'CODE_EXPIRED'}
    
    # Vérifier le code
    if not auth.verify_code(code, pending_data['code_hash'], pending_data['code_salt'], 
                             pending_data['code_iterations'], pepper):
        return {'ok': False, 'error': 'INVALID_CODE'}
    
    # Créer le client
    id_client = str(uuid.uuid4())
    
    db = database.get_database()
    if db:
        success = db.add_client(
            id_client=id_client,
            email=email,
            password_hash=pending_data['password_hash'],
            id_fb=pending_data['id_fb'],
            id_insta=pending_data['id_insta'],
            nom_entreprise=pending_data['nom_entreprise'],
            secteur=pending_data['secteur'],
            created_at=pending_data['created_at']
        )
        
        if not success:
            return {'ok': False, 'error': 'DATABASE_ERROR'}
    
    # Supprimer les données temporaires
    cache.remove(f'PENDING_{email}')
    
    return {'ok': True, 'id_client': id_client}


def login(email: str, password: str, pepper: str) -> Dict[str, Any]:
    """
    Authentifie un utilisateur
    """
    if not validate_email(email) or not password:
        return {'ok': False, 'error': 'INVALID_CREDENTIALS'}
    
    # Rate limiting
    rate_limit_key = f'LOGIN_ATTEMPTS_{email}'
    attempt_data = cache.get(rate_limit_key)
    if attempt_data and attempt_data.get('count', 0) >= 10:
        return {'ok': False, 'error': 'RATE_LIMIT'}
    
    # Chercher le client
    db = database.get_database()
    if not db:
        return {'ok': False, 'error': 'DATABASE_ERROR'}
    
    client = db.get_client_by_email(email)
    if not client:
        # Incrémenter le rate limit
        if not attempt_data:
            attempt_data = {'count': 0, 'reset_at': datetime.now().isoformat()}
        attempt_data['count'] += 1
        cache.put(rate_limit_key, attempt_data, 15 * 60)
        
        return {'ok': False, 'error': 'INVALID_CREDENTIALS'}
    
    # Vérifier le mot de passe
    if not auth.verify_password(password, client['password_hash'], pepper):
        if not attempt_data:
            attempt_data = {'count': 0, 'reset_at': datetime.now().isoformat()}
        attempt_data['count'] += 1
        cache.put(rate_limit_key, attempt_data, 15 * 60)
        
        return {'ok': False, 'error': 'INVALID_CREDENTIALS'}
    
    # Succès - réinitialiser le rate limit
    cache.remove(rate_limit_key)
    
    return {
        'ok': True,
        'id_client': client['id_client'],
        'email': email,
        'nom_entreprise': client.get('nom_entreprise', ''),
        'secteur': client.get('secteur', ''),
        'id_fb': client.get('id_fb', ''),
        'id_insta': client.get('id_insta', '')
    }


def oauth_init(email: str, provider: str) -> Dict[str, Any]:
    """
    Initialise une connexion OAuth
    """
    if not validate_email(email) or provider not in ['facebook', 'instagram']:
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    state = str(uuid.uuid4())
    oauth_data = {
        'email': email,
        'provider': provider,
        'created_at': datetime.now().isoformat()
    }
    cache.put(f'OAUTH_STATE_{state}', oauth_data, 10 * 60)
    
    # Générer l'URL d'authentification (simplifié pour la démo)
    # En production, utiliser OAuth.io ou une autre solution
    auth_url = f"https://www.facebook.com/v19.0/dialog/oauth?client_id=YOUR_APP_ID&redirect_uri=YOUR_CALLBACK&response_type=code&state={state}&scope=email"
    
    return {'ok': True, 'authUrl': auth_url}


def oauth_status(email: str) -> Dict[str, Any]:
    """
    Récupère le statut OAuth d'un utilisateur
    """
    if not validate_email(email):
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    oauth_data = cache.get(f'OAUTH_LINK_{email}')
    
    if not oauth_data:
        return {
            'ok': True,
            'facebookLinked': False,
            'instagramLinked': False,
            'id_fb': None,
            'id_insta': None
        }
    
    return {
        'ok': True,
        'facebookLinked': bool(oauth_data.get('id_fb')),
        'instagramLinked': bool(oauth_data.get('id_insta')),
        'id_fb': oauth_data.get('id_fb'),
        'id_insta': oauth_data.get('id_insta')
    }


def update_user_profile(user_id: str, email: str = None, nom_entreprise: str = None, secteur: str = None, password: str = None, pepper: str = None) -> Dict[str, Any]:
    """
    Met à jour le profil d'un utilisateur
    
    Args:
        user_id: ID du client
        email: Nouvel email (optionnel)
        nom_entreprise: Nouveau nom (optionnel)
        secteur: Nouveau secteur (optionnel)
        password: Nouveau mot de passe (optionnel)
        pepper: Clé secrète pour PBKDF2
    """
    print(f"🔍 [backend_service] update_user_profile appelé avec user_id={user_id}")
    
    # Validation
    if not user_id:
        print(f"❌ [backend_service] user_id manquant")
        return {'ok': False, 'error': 'INVALID_INPUT'}
    
    # Récupérer le client
    db = database.get_database()
    if not db:
        print(f"❌ [backend_service] Database non disponible")
        return {'ok': False, 'error': 'DATABASE_ERROR'}
    
    client = db.get_client_by_id(user_id)
    if not client:
        print(f"❌ [backend_service] Client {user_id} non trouvé")
        return {'ok': False, 'error': 'CLIENT_NOT_FOUND'}
    
    print(f"✅ [backend_service] Client trouvé: {client}")
    
    # Valider les nouvelles données
    if email and not validate_email(email):
        return {'ok': False, 'error': 'INVALID_EMAIL'}
    
    # Vérifier si l'email est déjà utilisé (par un autre utilisateur)
    if email and email != client.get('email'):
        existing = db.find_client_by_email(email)
        if existing:
            return {'ok': False, 'error': 'EMAIL_EXISTS'}
    
    if password and not validate_password(password):
        return {'ok': False, 'error': 'INVALID_PASSWORD'}
    
    if secteur and not validate_secteur(secteur):
        return {'ok': False, 'error': 'INVALID_SECTEUR'}
    
    # Préparer la mise à jour - utiliser les valeurs existantes comme fallback
    update_data = {
        'id_client': user_id,
        'email': email if email else client.get('email'),
        'nom_entreprise': nom_entreprise if nom_entreprise else client.get('nom_entreprise'),
        'secteur': secteur if secteur else client.get('secteur'),
        'password_hash': auth.hash_password(password, pepper) if password and pepper else client.get('password_hash'),
        'id_fb': client.get('id_fb', ''),
        'id_insta': client.get('id_insta', ''),
    }
    
    print(f"📝 [backend_service] Données de mise à jour: {update_data}")
    
    # Mettre à jour dans la base de données
    try:
        if db and hasattr(db, 'update_client'):
            result = db.update_client(update_data)
            print(f"🔄 [backend_service] Résultat update_client: {result}")
            if result:
                return {'ok': True, 'id_client': user_id}
            else:
                return {'ok': False, 'error': 'UPDATE_FAILED'}
        else:
            # Fallback: mettre à jour le client en cache
            cache.put(f'CLIENT_{user_id}', update_data, 24 * 60 * 60)
            return {'ok': True, 'id_client': user_id}
    except Exception as e:
        print(f"❌ [backend_service] Erreur lors de la mise à jour: {e}")
        import traceback
        traceback.print_exc()
        return {'ok': False, 'error': 'UPDATE_FAILED'}
