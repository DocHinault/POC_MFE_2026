"""Gestion de la session utilisateur Streamlit"""
import streamlit as st

def initialize_session_state():
    """Initialise l'état de session Streamlit"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'page' not in st.session_state:
        st.session_state.page = "auth"
    if 'registration_step' not in st.session_state:
        st.session_state.registration_step = 1
    if 'temp_registration_data' not in st.session_state:
        st.session_state.temp_registration_data = {}
    if 'confirmation_code' not in st.session_state:
        st.session_state.confirmation_code = None

