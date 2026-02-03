#!/bin/bash

# Script pour lancer Streamlit avec ngrok

cd /workspaces/POC_MFE_2026

# Activer venv
source .venv/bin/activate

# Tuer les anciens processus
echo "⏹️  Arrêt des anciens processus Streamlit..."
pkill -f "streamlit run" 2>/dev/null || true
sleep 2

# Afficher l'URL ngrok
echo ""
echo "🔗 URL ngrok: https://platinous-sturdiest-lianne.ngrok-free.dev/"
echo "📱 Application: http://localhost:8504"
echo ""

# Lancer Streamlit
echo "🚀 Lancement de Streamlit sur port 8504..."
echo "=================================================="
streamlit run streamlit_app.py --server.port=8504 --logger.level=info
