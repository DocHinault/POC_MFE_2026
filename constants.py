"""Messages et constantes de l'application"""

MESSAGES = {
    "email_required": "L'email est requis",
    "email_invalid": "Email invalide",
    "email_exists": "Cet email est déjà utilisé. Veuillez vous connecter.",
    "password_required": "Le mot de passe est requis",
    "password_short": "Le mot de passe doit contenir au moins 8 caractères",
    "password_no_upper": "Le mot de passe doit contenir au moins une majuscule",
    "password_no_digit": "Le mot de passe doit contenir au moins un chiffre",
    "password_mismatch": "Les mots de passe ne correspondent pas",
    "company_required": "Le nom de l'entreprise est requis",
    "code_invalid": "Code incorrect",
    "login_success": "Connexion réussie!",
    "signup_success": "Inscription confirmée! Vous êtes maintenant connecté.",
    "code_sent": "Code de confirmation envoyé",
    "invalid_credentials": "Email ou mot de passe incorrect",
    "all_fields": "Veuillez remplir tous les champs"
}

# Regex patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PASSWORD_MIN_LENGTH = 8
