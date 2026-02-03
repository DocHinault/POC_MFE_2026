"""Configuration de l'application"""
import os
from dotenv import load_dotenv

load_dotenv()

# ===== APPS SCRIPT API (Production) =====
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL", "")
API_KEY = os.getenv("API_KEY", "")

# ===== Google Sheets (Legacy - si utilisé directement) =====
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

# ===== Facebook & Instagram =====
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID", "")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")

# Email
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

# Secteurs
SECTEURS = ["Influenceur", "Salle de sport", "Hôtellerie/Restauration"]

# KPIs par secteur
KPI_MAPPING = {
    "Influenceur": ["Engagement", "Reach", "Impressions", "Followers Growth"],
    "Salle de sport": ["Member Inquiries", "Class Bookings", "Membership Views", "Location Visits"],
    "Hôtellerie/Restauration": ["Reservations", "Menu Views", "Call Clicks", "Website Visits"]
}
