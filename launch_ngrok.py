#!/usr/bin/env python3
"""
Lance ngrok tunnel pour exposer localhost:8503 en HTTPS
Installe pyngrok et l'utilise
"""

import subprocess
import sys
import time

print("🔄 Installation de pyngrok...")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyngrok"], check=True)

print("✅ pyngrok installé")

from pyngrok import ngrok

print("\n🌐 Lancement du tunnel ngrok sur le port 8503...")
public_url = ngrok.connect(8503, "http")

print(f"\n{'='*70}")
print(f"✅ TUNNEL NGROK ACTIVE!")
print(f"{'='*70}")
print(f"\n🔗 VOTRE URL PUBLIQUE HTTPS:")
print(f"\n    {public_url}\n")
print(f"{'='*70}")
print(f"\nUtilisez cette URL dans:")
print(f"  1. Meta App > Facebook Login > Paramètres")
print(f"  2. Fichier .env (OAUTH_REDIRECT_URI)")
print(f"\nAccédez à votre app via: {public_url}")
print(f"\nAppuyez sur Ctrl+C pour arrêter le tunnel")
print(f"{'='*70}\n")

# Garder le tunnel actif
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n🛑 Tunnel ngrok arrêté")
    ngrok.kill()
