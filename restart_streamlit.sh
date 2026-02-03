#!/bin/bash
# Tuer tous les processus Streamlit
echo "🛑 Arrêt des processus Streamlit..."
pkill -f streamlit || true
sleep 2

# Attendre un peu
echo "⏳ Attente de 3 secondes..."
sleep 3

# Lancer Streamlit proprement
echo "🚀 Lancement de Streamlit sur le port 8504..."
cd /workspaces/POC_MFE_2026
source .venv/bin/activate 2>/dev/null || true
/workspaces/POC_MFE_2026/.venv/bin/python -m streamlit run streamlit_app.py --server.port=8504
