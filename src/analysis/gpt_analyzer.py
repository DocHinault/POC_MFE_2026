"""Analyse GPT des KPIs avec prompts personnalisés par secteur"""
from typing import Dict
import logging

def analyze_with_gpt(kpis_data: Dict, secteur: str, api_key: str) -> Dict:
    """
    Analyse les KPIs avec GPT en utilisant un prompt personnalisé selon le secteur
    
    Args:
        kpis_data: Données KPI (Instagram + Facebook)
        secteur: Secteur d'activité (Influenceur, Salle de sport, etc.)
        api_key: Clé API OpenAI
        
    Returns:
        Dict avec: objectives, strengths, weaknesses, next_post_ideas, summary
    """
    # TODO: À extraire de analysis_pipeline.py
    pass
