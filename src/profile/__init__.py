"""Module de gestion du profil utilisateur"""
from .profile_page import show_profile_tab
from .edit_page import show_edit_profile
from .kpi_selector import get_kpis_for_sector, get_gpt_prompt_for_sector, analyze_sector_performance
from .dashboard import page_p1, show_linking_tab, show_analysis_tab

__all__ = [
    'show_profile_tab',
    'show_edit_profile',
    'get_kpis_for_sector',
    'get_gpt_prompt_for_sector',
    'analyze_sector_performance',
    'page_p1',
    'show_linking_tab',
    'show_analysis_tab'
]
