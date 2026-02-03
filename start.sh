#!/bin/bash

# MG - POC V1 - Script de démarrage

echo "🚀 Démarrage de MG - POC V1 - Social Media Reporting"
echo "=================================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

echo "✅ Python3 trouvé"

# Vérifier pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé"
    exit 1
fi

echo "✅ pip3 trouvé"
echo ""

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip3 install -r requirements.txt > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Dépendances installées"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

echo ""

# Tester la configuration
echo "🔍 Vérification de la configuration..."
python3 test_config.py

if [ $? -ne 0 ]; then
    echo "❌ Configuration incomplète"
    exit 1
fi

echo ""
echo "🎉 Configuration OK!"
echo ""
echo "Lancement de l'application..."
echo "L'application sera disponible sur: http://localhost:8501"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

# Lancer l'application
streamlit run streamlit_app.py
