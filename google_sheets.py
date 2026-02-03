"""Gestion de Google Sheets pour le stockage des utilisateurs"""
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEETS_ID, GOOGLE_CREDENTIALS_PATH
import json

def get_google_sheets_client():
    """Initialise le client Google Sheets"""
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return gspread.authorize(creds)
    except Exception as e:
        print(f"Erreur lors de la connexion à Google Sheets: {e}")
        return None

def check_email_exists(email):
    """Vérifie si un email existe déjà dans Google Sheets"""
    try:
        client = get_google_sheets_client()
        if not client or not GOOGLE_SHEETS_ID:
            return False
        
        sheet = client.open_by_key(GOOGLE_SHEETS_ID)
        worksheet = sheet.worksheet("Utilisateurs")
        
        # Récupère tous les emails
        emails = worksheet.col_values(2)  # Colonne B (email)
        return email.lower() in [e.lower() for e in emails]
    except Exception as e:
        print(f"Erreur lors de la vérification de l'email: {e}")
        return False

def save_user_to_sheets(user_data):
    """Sauvegarde un nouvel utilisateur dans Google Sheets"""
    try:
        client = get_google_sheets_client()
        if not client or not GOOGLE_SHEETS_ID:
            return False
        
        sheet = client.open_by_key(GOOGLE_SHEETS_ID)
        
        # Crée la feuille s'il n'existe pas
        try:
            worksheet = sheet.worksheet("Utilisateurs")
        except:
            worksheet = sheet.add_worksheet("Utilisateurs", rows=1000, cols=10)
            # Ajoute les en-têtes
            headers = ["Nom Entreprise", "Email", "Secteur", "Facebook", "Instagram", "Date Inscription", "Confirmé", "ID Session"]
            worksheet.append_row(headers)
        
        # Ajoute l'utilisateur
        row = [
            user_data.get("nom_entreprise", ""),
            user_data.get("email", ""),
            user_data.get("secteur", ""),
            user_data.get("facebook", ""),
            user_data.get("instagram", ""),
            user_data.get("date_inscription", ""),
            user_data.get("confirmé", ""),
            user_data.get("session_id", "")
        ]
        worksheet.append_row(row)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False

def get_user_data(email):
    """Récupère les données d'un utilisateur depuis Google Sheets"""
    try:
        client = get_google_sheets_client()
        if not client or not GOOGLE_SHEETS_ID:
            return None
        
        sheet = client.open_by_key(GOOGLE_SHEETS_ID)
        worksheet = sheet.worksheet("Utilisateurs")
        
        all_values = worksheet.get_all_values()
        
        for row in all_values[1:]:  # Saute l'en-tête
            if len(row) > 1 and row[1].lower() == email.lower():
                return {
                    "nom_entreprise": row[0],
                    "email": row[1],
                    "secteur": row[2],
                    "facebook": row[3] if len(row) > 3 else "",
                    "instagram": row[4] if len(row) > 4 else "",
                    "confirmé": row[6] if len(row) > 6 else ""
                }
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération: {e}")
        return None
