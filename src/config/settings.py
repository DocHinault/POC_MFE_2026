"""Configuration de l'application"""
import os
from dotenv import load_dotenv

load_dotenv()

# ===== Google Sheets =====
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

# ===== Facebook & Instagram =====
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID", "")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")

# ===== OpenAI (ÉTAPE 3) =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ===== Email =====
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

# ===== Secteurs =====
SECTEURS = ["Influenceur", "Salle de sport", "Hôtellerie/Restauration"]

# ===== KPIs par secteur =====
KPI_MAPPING = {
    "Influenceur": ["Engagement", "Reach", "Impressions", "Followers Growth"],
    "Salle de sport": ["Member Inquiries", "Class Bookings", "Membership Views", "Location Visits"],
    "Hôtellerie/Restauration": ["Reservations", "Menu Views", "Call Clicks", "Website Visits"]
}

# ===== Prompts GPT par secteur =====
GPT_PROMPTS = {
    "Influenceur": """Analyse les KPIs d'un influenceur.
Focus: engagement, reach, croissance des followers.
Recommandations: type de contenu, horaires de publication, collaborations.""",
    
    "Salle de sport": """Analyse les KPIs d'une salle de sport.
Focus: conversion membres, réservations cours, visites profil.
Recommandations: promotions, types de cours, moments clés.""",
    
    "Hôtellerie/Restauration": """Analyse les KPIs d'un restaurant/hôtel.
Focus: réservations, vues menu, clics appel, visites site web.
Recommandations: plats à mettre en avant, offres spéciales, timing posts."""
}
