#!/bin/bash
cd /workspaces/POC_MFE_2026
source .venv/bin/activate
streamlit run streamlit_app.py --server.port=8503
