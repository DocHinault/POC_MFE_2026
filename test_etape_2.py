#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les imports fonctionnent
Lancez avec: python3 test_etape_2.py
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("  TEST ÉTAPE 2 - Vérification des imports")
print("=" * 70)
print()

tests_passed = 0
tests_failed = 0

# Test 1: Importer social_auth
print("[1/5] Test import social_auth.py...")
try:
    from social_auth import SocialMediaAuthenticator, SocialMediaLinkManager
    print("    ✅ PASS: social_auth.py importe correctement")
    print("       - SocialMediaAuthenticator disponible")
    print("       - SocialMediaLinkManager disponible")
    tests_passed += 1
except Exception as e:
    print(f"    ❌ FAIL: {e}")
    tests_failed += 1

# Test 2: Vérifier les méthodes de SocialMediaAuthenticator
print("\n[2/5] Test méthodes SocialMediaAuthenticator...")
try:
    auth = SocialMediaAuthenticator()
    
    # Vérifier que les méthodes existent
    required_methods = [
        'get_facebook_login_url',
        'exchange_code_for_token',
        'get_user_info',
        'get_instagram_business_accounts',
        'get_facebook_pages',
        'get_page_insights',
        'get_instagram_insights',
        'refresh_long_lived_token'
    ]
    
    for method in required_methods:
        if not hasattr(auth, method):
            raise ValueError(f"Méthode manquante: {method}")
    
    print(f"    ✅ PASS: {len(required_methods)} méthodes trouvées")
    for method in required_methods:
        print(f"       - {method}()")
    tests_passed += 1
except Exception as e:
    print(f"    ❌ FAIL: {e}")
    tests_failed += 1

# Test 3: Vérifier les méthodes de SocialMediaLinkManager
print("\n[3/5] Test méthodes SocialMediaLinkManager...")
try:
    manager = SocialMediaLinkManager()
    
    required_methods = [
        'link_instagram_account',
        'link_facebook_account',
        'link_facebook_page',
        'get_linked_accounts',
        'unlink_account',
        'unlink_facebook_page'
    ]
    
    for method in required_methods:
        if not hasattr(manager, method):
            raise ValueError(f"Méthode manquante: {method}")
    
    print(f"    ✅ PASS: {len(required_methods)} méthodes trouvées")
    for method in required_methods:
        print(f"       - {method}()")
    tests_passed += 1
except Exception as e:
    print(f"    ❌ FAIL: {e}")
    tests_failed += 1

# Test 4: Importer la page Streamlit (sans exécuter Streamlit)
print("\n[4/5] Test import pages.py...")
try:
    # On teste juste que le fichier compile
    import py_compile
    py_compile.compile('pages.py', doraise=True)
    print("    ✅ PASS: pages.py compile correctement")
    print("       - Modifications appliquées sans erreur")
    tests_passed += 1
except Exception as e:
    print(f"    ❌ FAIL: {e}")
    tests_failed += 1

# Test 5: Vérifier que les fichiers documentation existent
print("\n[5/5] Test présence fichiers documentation...")
try:
    required_files = [
        'DEMARRAGE_RAPIDE_ETAPE_2.md',
        'SOCIAL_AUTH_SETUP.md',
        'CHECKLIST_SOCIAL_AUTH.md',
        'FLUX_VISUEL_ETAPE_2.md',
        'ETAPE_2_RESUME.md',
        'INDEX_ETAPE_2.md',
        'LIRE_D_ABORD.txt',
        'examples_social_auth.py'
    ]
    
    missing_files = []
    for filename in required_files:
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    if missing_files:
        raise ValueError(f"Fichiers manquants: {', '.join(missing_files)}")
    
    print(f"    ✅ PASS: {len(required_files)} fichiers trouvés")
    for filename in required_files:
        size = os.path.getsize(filename)
        print(f"       - {filename} ({size} bytes)")
    tests_passed += 1
except Exception as e:
    print(f"    ❌ FAIL: {e}")
    tests_failed += 1

# Résumé
print("\n" + "=" * 70)
print(f"  RÉSUMÉ: {tests_passed} PASS, {tests_failed} FAIL")
print("=" * 70)
print()

if tests_failed == 0:
    print("✅ TOUS LES TESTS PASSENT!")
    print()
    print("Prochaines étapes:")
    print("  1. Créer une app Meta: https://developers.facebook.com")
    print("  2. Remplir le .env avec APP_ID et APP_SECRET")
    print("  3. Lancer: streamlit run streamlit_app.py")
    print()
    sys.exit(0)
else:
    print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
    print("Vérifiez les messages d'erreur ci-dessus")
    print()
    sys.exit(1)
