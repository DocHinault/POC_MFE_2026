"""
Authentification et chiffrement PBKDF2
"""

import hmac
import hashlib
import secrets
import base64
from typing import Tuple

# Constantes de sécurité
PBKDF2_ITERATIONS = 50000
PBKDF2_HASH_ALGORITHM = 'sha256'


def hash_password(password: str, pepper: str) -> str:
    """
    Hache un mot de passe avec PBKDF2-SHA256
    
    Format: pbkdf2_sha256$iterations$salt$hash
    """
    salt = secrets.token_bytes(16)
    password_with_pepper = (password + pepper).encode('utf-8')
    
    hash_bytes = hashlib.pbkdf2_hmac(
        PBKDF2_HASH_ALGORITHM,
        password_with_pepper,
        salt,
        PBKDF2_ITERATIONS,
        dklen=32
    )
    
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(hash_bytes).decode('ascii')
    
    return f'pbkdf2_sha256${PBKDF2_ITERATIONS}${salt_b64}${hash_b64}'


def verify_password(password: str, password_hash: str, pepper: str) -> bool:
    """
    Vérifie un mot de passe contre son hash
    """
    try:
        parts = password_hash.split('$')
        if len(parts) != 4:
            return False
        
        algorithm, iterations_str, salt_b64, hash_b64 = parts
        
        if algorithm != 'pbkdf2_sha256':
            return False
        
        iterations = int(iterations_str)
        salt = base64.b64decode(salt_b64)
        expected_hash = base64.b64decode(hash_b64)
        
        password_with_pepper = (password + pepper).encode('utf-8')
        computed_hash = hashlib.pbkdf2_hmac(
            PBKDF2_HASH_ALGORITHM,
            password_with_pepper,
            salt,
            iterations,
            dklen=32
        )
        
        return hmac.compare_digest(expected_hash, computed_hash)
    except Exception:
        return False


def hash_code(code: str, pepper: str) -> Tuple[str, str, str]:
    """
    Hache un code de confirmation
    
    Retourne: (salt_b64, hash_b64, iterations)
    """
    salt = secrets.token_bytes(16)
    code_with_pepper = (code + pepper).encode('utf-8')
    
    iterations = 50000
    hash_bytes = hashlib.pbkdf2_hmac(
        PBKDF2_HASH_ALGORITHM,
        code_with_pepper,
        salt,
        iterations,
        dklen=32
    )
    
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(hash_bytes).decode('ascii')
    
    return salt_b64, hash_b64, iterations


def verify_code(code: str, code_hash: str, code_salt_b64: str, code_iterations: int, pepper: str) -> bool:
    """
    Vérifie un code de confirmation
    """
    try:
        code_with_pepper = (code + pepper).encode('utf-8')
        salt = base64.b64decode(code_salt_b64)
        expected_hash = base64.b64decode(code_hash)
        
        computed_hash = hashlib.pbkdf2_hmac(
            PBKDF2_HASH_ALGORITHM,
            code_with_pepper,
            salt,
            code_iterations,
            dklen=32
        )
        
        return hmac.compare_digest(expected_hash, computed_hash)
    except Exception:
        return False


def generate_confirmation_code() -> str:
    """
    Génère un code de confirmation 6 chiffres
    """
    return str(secrets.randbelow(1000000)).zfill(6)
