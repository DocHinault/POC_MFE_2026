#!/bin/bash

# 🚀 QUICKSTART - POC_MFE_2026
# Script pour démarrer le projet en 3 commandes

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "🚀 POC_MFE_2026 - DÉMARRAGE RAPIDE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# 1. Vérifier l'environnement
echo "[1/3] 🔍 Vérification de l'environnement..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi
echo "✅ Python3 trouvé: $(python3 --version)"

# 2. Installer les dépendances
echo ""
echo "[2/3] 📦 Installation des dépendances..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment créé"
fi

source .venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées"
else
    echo "⚠️ Installation partiellement réussie"
fi

# 3. Configuration
echo ""
echo "[3/3] ⚙️ Configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Fichier .env créé (remplir les valeurs!)"
else
    echo "✅ .env existe déjà"
fi

# Lancer l'app
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ PRÊT À DÉMARRER!"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📝 CONFIGURATION REQUISE:"
echo "   1. Remplir .env avec vos clés API:"
echo "      - OPENAI_API_KEY"
echo "      - SMTP_* (pour emails)"
echo "      - FACEBOOK_APP_ID, FACEBOOK_APP_SECRET"
echo ""
echo "🚀 LANCER L'APP:"
echo "   streamlit run streamlit_app.py --server.port=8503"
echo ""
echo "📚 DOCUMENTATION:"
echo "   - EXECUTIVE_SUMMARY.md (résumé exécutif)"
echo "   - ANALYSIS_PIPELINE_README.md (guide pipeline)"
echo "   - INDEX_COMPLET.md (structure projet)"
echo ""
echo "🧪 VALIDER L'INSTALLATION:"
echo "   python3 final_validation.py"
echo "   python3 test_analysis_pipeline.py"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
