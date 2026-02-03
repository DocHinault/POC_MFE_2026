"""Validation des données d'authentification"""
import re
from email_validator import validate_email, EmailNotValidError

def validate_email_format(email: str) -> bool:
    """
    Valide le format d'un email
    
    Args:
        email: Adresse email à valider
        
    Returns:
        True si l'email est valide, False sinon
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def is_valid_password(password: str) -> tuple[bool, str]:
    """
    Vérifie les critères de sécurité du mot de passe
    
    Args:
        password: Mot de passe à valider
        
    Returns:
        Tuple (is_valid, message)
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not any(char.isupper() for char in password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    if not any(char.isdigit() for char in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    return True, "OK"

