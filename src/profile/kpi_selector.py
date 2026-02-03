"""Sélecteur de KPIs et prompts GPT par secteur"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import List, Dict

def get_kpis_for_sector(secteur: str) -> List[str]:
    """
    Retourne la liste des KPIs pertinents pour un secteur donné
    
    Args:
        secteur: Secteur d'activité (Influenceur, Salle de sport, etc.)
        
    Returns:
        Liste des KPIs à suivre pour ce secteur
    """
    from config import KPI_MAPPING
    return KPI_MAPPING.get(secteur, [])

def get_gpt_prompt_for_sector(secteur: str) -> str:
    """
    Retourne le prompt GPT optimisé pour un secteur donné
    
    Args:
        secteur: Secteur d'activité
        
    Returns:
        Prompt GPT personnalisé pour le secteur
    """
    from src.config.settings import GPT_PROMPTS
    return GPT_PROMPTS.get(secteur, "Analyse les KPIs et donne des recommandations.")

def analyze_sector_performance(kpis_data: Dict, secteur: str) -> Dict:
    """
    Analyse les performances selon le secteur d'activité
    
    Args:
        kpis_data: Données KPI
        secteur: Secteur d'activité
        
    Returns:
        Dict avec analyse spécifique au secteur
    """
    sector_kpis = get_kpis_for_sector(secteur)
    
    # Filtrer les KPIs pertinents
    relevant_data = {
        k: v for k, v in kpis_data.items()
        if k in sector_kpis
    }
    
    return {
        "secteur": secteur,
        "kpis_cibles": sector_kpis,
        "donnees": relevant_data,
        "prompt_gpt": get_gpt_prompt_for_sector(secteur)
    }
