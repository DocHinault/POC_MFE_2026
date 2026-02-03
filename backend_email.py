"""
Service d'envoi d'emails via Gmail
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os


class EmailService:
    """Service pour envoyer des emails via Gmail SMTP"""
    
    def __init__(self, gmail_address: str, gmail_password: str):
        """
        Initialise le service d'email
        
        Args:
            gmail_address: Adresse Gmail
            gmail_password: Mot de passe ou App Password Gmail
        """
        self.gmail_address = gmail_address
        self.gmail_password = gmail_password
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def send_email(self, to_address: str, subject: str, body: str) -> bool:
        """
        Envoie un email
        
        Args:
            to_address: Adresse destinataire
            subject: Sujet
            body: Corps du message
        
        Retourne: True si succès, False sinon
        """
        try:
            # Créer le message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_address
            msg['To'] = to_address
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Envoyer via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi d'email: {e}")
            return False


# Instance globale
_email_service = None


def init_email_service(gmail_address: str, gmail_password: str) -> EmailService:
    """Initialise le service d'email"""
    global _email_service
    _email_service = EmailService(gmail_address, gmail_password)
    return _email_service


def get_email_service() -> Optional[EmailService]:
    """Récupère l'instance du service d'email"""
    return _email_service


def send_confirmation_email(email: str, code: str) -> bool:
    """Envoie un code de confirmation"""
    global _email_service
    
    # Si le service n'est pas initialisé, tenter de l'initialiser depuis les variables d'environnement
    if not _email_service:
        try:
            import os
            gmail_address = os.getenv('GMAIL_ADDRESS')
            gmail_password = os.getenv('GMAIL_PASSWORD')
            if gmail_address and gmail_password:
                init_email_service(gmail_address, gmail_password)
                print(f"✅ Service email initialisé automatiquement lors de l'envoi")
            else:
                print("⚠️ GMAIL_ADDRESS ou GMAIL_PASSWORD non configurés dans .env")
                return False
        except Exception as e:
            print(f"⚠️ Erreur lors de l'initialisation du service email: {e}")
            return False
    
    subject = "Code de confirmation MG"
    body = f"Votre code de confirmation : {code}\n\nValable 15 minutes."
    
    return _email_service.send_email(email, subject, body)
