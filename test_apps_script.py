#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à l'API Apps Script
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL", "").strip()
API_KEY = os.getenv("API_KEY", "").strip()

def test_api_connection():
    """Teste la connexion à l'API Apps Script"""
    print("\n" + "="*70)
    print("🔍 TEST DE CONNEXION - APPS SCRIPT API")
    print("="*70 + "\n")
    
    # Vérifier les variables d'env
    print("1️⃣  VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT")
    print("-" * 70)
    
    if not APPS_SCRIPT_URL:
        print("❌ APPS_SCRIPT_URL non configurée dans .env")
        return False
    else:
        print(f"✅ APPS_SCRIPT_URL: {APPS_SCRIPT_URL[:50]}...")
    
    if not API_KEY:
        print("❌ API_KEY non configurée dans .env")
        return False
    else:
        print(f"✅ API_KEY: {API_KEY[:20]}...")
    
    print("\n2️⃣  TEST DE CONNEXION À L'API")
    print("-" * 70)
    
    try:
        import requests
        
        # Test avec route 'health'
        payload = {
            'api_key': API_KEY,
            'route': 'health'
        }
        
        print(f"📡 Envoi d'une requête POST vers: {APPS_SCRIPT_URL}")
        print(f"📦 Payload: {payload}")
        
        response = requests.post(
            APPS_SCRIPT_URL,
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📨 Code HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Réponse: {data}")
            
            if data.get('ok'):
                print("\n✅ SUCCÈS! L'API Apps Script répond correctement!")
                print(f"   Version: {data.get('version', 'N/A')}")
                print(f"   Timestamp: {data.get('ts', 'N/A')}")
                return True
            else:
                print(f"\n❌ L'API répond mais avec une erreur: {data.get('error')}")
                return False
        else:
            print(f"\n❌ Erreur HTTP {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERREUR: Impossible de se connecter à l'API")
        print("   Vérifiez que:")
        print("   - L'URL est correcte")
        print("   - Le Web App est déployé")
        print("   - Vous avez une connexion Internet")
        return False
    except requests.exceptions.Timeout:
        print("\n❌ ERREUR: La requête a expiré (timeout)")
        print("   Le serveur met trop de temps à répondre")
        return False
    except Exception as e:
        print(f"\n❌ ERREUR: {type(e).__name__}: {e}")
        return False

def test_email_route():
    """Teste la route d'inscription pour vérifier l'email"""
    print("\n3️⃣  TEST DE LA ROUTE D'INSCRIPTION")
    print("-" * 70)
    
    try:
        import requests
        
        # Utiliser un email de test
        test_email = "test@example.com"
        test_password = "TestPassword123"
        test_nom = "Test Company"
        test_secteur = "Influenceur"
        
        payload = {
            'api_key': API_KEY,
            'route': 'register_start',
            'email': test_email,
            'password': test_password,
            'nom_entreprise': test_nom,
            'secteur': test_secteur
        }
        
        print(f"📡 Test d'inscription avec:")
        print(f"   Email: {test_email}")
        print(f"   Entreprise: {test_nom}")
        print(f"   Secteur: {test_secteur}")
        
        response = requests.post(
            APPS_SCRIPT_URL,
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('ok'):
                print(f"\n✅ Route register_start fonctionne!")
                print(f"   Un code de confirmation devrait être envoyé à {test_email}")
            elif data.get('error') == 'EMAIL_EXISTS':
                print(f"\n⚠️  Cet email existe déjà dans la BD")
                print(f"   C'est normal si vous avez déjà testé")
            else:
                print(f"\n❌ Erreur: {data.get('error')}")
                return False
            return True
        else:
            print(f"\n❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        return False

def main():
    """Fonction principale"""
    print("\n" + "🚀 "*35)
    print("TEST DE CONFIGURATION - MG POC V1")
    print("🚀 "*35 + "\n")
    
    # Test 1: Connexion API
    api_ok = test_api_connection()
    
    if not api_ok:
        print("\n" + "="*70)
        print("❌ LA CONNEXION À L'API A ÉCHOUÉ")
        print("="*70)
        print("\n📋 CHECKLIST DE VÉRIFICATION:")
        print("   1. Vérifiez que le fichier .env existe")
        print("   2. Vérifiez APPS_SCRIPT_URL (ne doit pas finir par /edit)")
        print("   3. Vérifiez que le Web App est déployé dans Apps Script")
        print("   4. Vérifiez que API_KEY est correctement définie")
        print("   5. Consultez SETUP_APPS_SCRIPT.md pour plus de détails")
        return False
    
    # Test 2: Route register_start
    email_ok = test_email_route()
    
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DU TEST")
    print("="*70)
    print(f"API Connection:     {'✅ OK' if api_ok else '❌ FAILED'}")
    print(f"Email Route:        {'✅ OK' if email_ok else '⚠️  PARTIAL'}")
    
    if api_ok:
        print("\n✅ La configuration semble correcte!")
        print("   Vous pouvez maintenant lancer l'application:")
        print("   $ streamlit run streamlit_app.py")
        return True
    else:
        print("\n❌ Il y a un problème avec la configuration")
        print("   Consultez les messages d'erreur ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
