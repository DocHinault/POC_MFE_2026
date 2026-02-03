"""Helpers - Utilitaires partagés"""
import streamlit as st


def get_api():
    """Récupère l'API depuis la session"""
    if hasattr(st.session_state, 'api') and st.session_state.api is not None:
        return st.session_state.api
    else:
        st.error("❌ Backend non initialisé. Vérifiez streamlit_app.py")
        st.stop()
