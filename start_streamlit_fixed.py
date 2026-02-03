#!/usr/bin/env python3
"""
Script pour démarrer Streamlit et vérifier que tout fonctionne correctement
"""

import subprocess
import os
import sys
import time

# Changer au répertoire du projet
os.chdir('/workspaces/POC_MFE_2026')

# Activer le venv
venv_path = '/workspaces/POC_MFE_2026/.venv/bin/activate'

print("🚀 Démarrage de Streamlit...")
print("=" * 60)

# Tuer les anciens processus Streamlit
print("⏹️  Arrêt des anciens processus Streamlit...")
os.system("pkill -f 'streamlit run' 2>/dev/null")
time.sleep(2)

# Vérifier que le port 8504 est libre
print("🔍 Vérification du port 8504...")
result = os.system("netstat -tuln 2>/dev/null | grep 8504")
if result == 0:
    print("⚠️  Port 8504 en cours d'utilisation, tentative de libération...")
    os.system("pkill -f 'streamlit' 2>/dev/null")
    time.sleep(3)

# Vérifier les imports
print("📦 Vérification des imports Python...")
try:
    from page_functions import page_auth, page_login, page_registration, page_confirmation, page_p1
    from pages.page_social_linking import page_social_linking
    print("✅ Tous les imports sont valides!")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# Lancer Streamlit
print("\n🎬 Lancement de Streamlit sur le port 8504...")
print("=" * 60)

# Utiliser subprocess avec activate
cmd = f'source {venv_path} && streamlit run streamlit_app.py --server.port=8504 --logger.level=debug'

try:
    os.system(cmd)
except KeyboardInterrupt:
    print("\n\n✋ Streamlit arrêté par l'utilisateur")
    sys.exit(0)
