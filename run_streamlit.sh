#!/bin/bash
cd /workspaces/POC_MFE_2026
source .venv/bin/activate 2>/dev/null || true
/workspaces/POC_MFE_2026/.venv/bin/python -m streamlit run streamlit_app.py --server.port=8503
