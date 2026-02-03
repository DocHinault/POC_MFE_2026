"""Styles CSS et configuration de page"""
import streamlit as st
from page_functions import configure_page_style

# Réexporter pour utilisation facile
__all__ = ["configure_page_style", "get_custom_css"]


def get_custom_css(dark_mode: bool = False) -> str:
    """Retourne le CSS personnalisé pour l'application"""
    if dark_mode:
        bg_color = "#1A1F2E"
        text_color = "#E8EAF0"
        card_bg = "#252C3A"
        secondary_text = "#94A3B8"
        accent_color = "#F59E0B"
        border_color = "#374151"
    else:
        bg_color = "linear-gradient(135deg, #F0F4F8 0%, #E2E8F0 100%)"
        text_color = "#1E293B"
        card_bg = "#FFFFFF"
        secondary_text = "#64748B"
        accent_color = "#D97706"
        border_color = "#E2E8F0"
    
    return f"""
    <style>
    /* Styles globaux */
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Texte global */
    body, p, div, span {{
        color: {text_color} !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-weight: 700 !important;
    }}
    
    /* Cards élégantes */
    .card {{
        background: {card_bg};
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid {border_color};
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }}
    
    /* Boutons Gold premium */
    .stButton > button {{
        background: linear-gradient(135deg, {accent_color} 0%, #F59E0B 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 16px;
        letter-spacing: 0.3px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #FBBF24 0%, #FCD34D 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }}
    
    /* Inputs stylisés */
    .stTextInput > div > div > input,
    .stTextArea textarea {{
        border-radius: 8px;
        border: 2px solid {border_color};
        padding: 12px;
        font-size: 15px;
        transition: border-color 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {{
        border-color: {accent_color};
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
    }}
    
    /* Metrics modernes */
    .metric-card {{
        background: linear-gradient(135deg, #1E3A8A 0%, #1F3A5F 100%);
        color: white;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(30, 58, 138, 0.2);
    }}
    
    /* Headers avec espacement */
    h1 {{
        font-size: 2.5rem !important;
        margin-bottom: 8px !important;
    }}
    
    h2 {{
        font-size: 1.75rem !important;
        margin-bottom: 12px !important;
    }}
    
    h3 {{
        font-size: 1.25rem !important;
        margin-bottom: 16px !important;
    }}
    
    /* Divider subtil */
    hr {{
        border: none;
        height: 1px;
        background: {border_color};
        margin: 32px 0;
    }}
    
    /* Secondary text */
    .secondary-text {{
        color: {secondary_text} !important;
        font-size: 14px;
    }}
    
    /* Toggle button style */
    div[data-testid="stButton"] button[kind="secondary"] {{
        background: {card_bg};
        border: 2px solid {border_color};
        color: {text_color};
    }}
    </style>
    """
