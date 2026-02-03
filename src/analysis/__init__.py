"""Module d'analyse - Pipeline complet"""
from .pipeline import AnalysisPipeline
from .kpi_fetcher import fetch_instagram_kpis, fetch_facebook_kpis
from .gpt_analyzer import analyze_with_gpt
from .powerpoint_generator import generate_powerpoint_report
from .email_sender import send_email_report

__all__ = [
    'AnalysisPipeline',
    'fetch_instagram_kpis',
    'fetch_facebook_kpis',
    'analyze_with_gpt',
    'generate_powerpoint_report',
    'send_email_report'
]
