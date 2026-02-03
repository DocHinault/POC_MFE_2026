"""Envoi d'emails avec rapports"""
from typing import Optional

def send_email_report(
    recipient_email: str,
    recipient_name: str,
    powerpoint_path: str,
    gpt_analysis: dict,
    sheet_url: Optional[str] = None
) -> bool:
    """
    Envoie un email avec le rapport PowerPoint en pièce jointe
    
    Args:
        recipient_email: Email du destinataire
        recipient_name: Nom du destinataire
        powerpoint_path: Chemin vers le fichier PowerPoint
        gpt_analysis: Résultats de l'analyse GPT
        sheet_url: URL de la Google Sheet (optionnel)
        
    Returns:
        True si envoi réussi, False sinon
    """
    # TODO: À extraire de analysis_pipeline.py
    pass
