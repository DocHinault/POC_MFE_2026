"""Composants UI réutilisables"""
import streamlit as st
from typing import Optional

def create_card(title: str, content: str, icon: Optional[str] = None):
    """Crée une carte stylisée"""
    icon_html = f"<span style='font-size: 24px; margin-right: 10px;'>{icon}</span>" if icon else ""
    st.markdown(f"""
    <div class='card'>
        <h3>{icon_html}{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label: str, value: str, delta: Optional[str] = None):
    """Crée une carte de métrique"""
    delta_html = f"<p style='font-size: 14px; margin-top: 8px;'>{delta}</p>" if delta else ""
    st.markdown(f"""
    <div class='metric-card'>
        <p style='font-size: 14px; opacity: 0.9; margin: 0;'>{label}</p>
        <h2 style='margin: 8px 0;'>{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_button(label: str, key: str, use_container_width: bool = False):
    """Crée un bouton stylisé"""
    return st.button(label, key=key, use_container_width=use_container_width)
