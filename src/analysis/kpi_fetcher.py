"""Récupération des KPIs Instagram et Facebook"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List
import logging

def fetch_instagram_kpis(instagram_account_id: str, access_token: str) -> Dict:
    """
    Récupère les KPIs Instagram via Graph API
    
    Args:
        instagram_account_id: ID du compte Instagram Business
        access_token: Token d'accès Instagram
        
    Returns:
        Dict avec: impressions, reach, profile_views, engagement_rate, top_posts
    """
    # TODO: À extraire de analysis_pipeline.py
    pass

def fetch_facebook_kpis(page_id: str, access_token: str) -> Dict:
    """
    Récupère les KPIs Facebook via Graph API
    
    Args:
        page_id: ID de la page Facebook
        access_token: Token d'accès Facebook
        
    Returns:
        Dict avec: reach, impressions, fans_count, engagement, top_posts
    """
    # TODO: À extraire de analysis_pipeline.py
    pass
