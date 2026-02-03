"""Script de test pour vérifier les dépendances et la configuration"""
import sys
import importlib

def test_imports():
    """Test l'importation de toutes les dépendances"""
    required_packages = [
        'streamlit',
        'google.auth',
        'gspread',
        'email_validator',
        'dotenv'
    ]
    
    print("🔍 Vérification des dépendances...")
    all_good = True
    
    for package in required_packages:
        try:
            module = importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            all_good = False
    
    return all_good

def test_local_imports():
    """Test l'importation des modules locaux"""
    print("\n🔍 Vérification des modules locaux...")
    local_modules = [
        'config',
        'auth',
        'pages',
        'google_sheets',
        'constants'
    ]
    
    all_good = True
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_good = False
    
    return all_good

def test_env_file():
    """Test la présence du fichier .env"""
    import os
    print("\n🔍 Vérification de la configuration...")
    
    if os.path.exists('.env'):
        print("✅ Fichier .env trouvé")
        return True
    else:
        print("⚠️  Fichier .env non trouvé (copie .env.example -> .env)")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("MG - POC V1 - Configuration Test")
    print("=" * 50)
    
    deps_ok = test_imports()
    local_ok = test_local_imports()
    env_ok = test_env_file()
    
    print("\n" + "=" * 50)
    if deps_ok and local_ok:
        print("✅ Tous les tests sont passés!")
        if not env_ok:
            print("⚠️  Veuillez configurer le fichier .env")
        sys.exit(0)
    else:
        print("❌ Certains tests ont échoué")
        print("Veuillez exécuter: pip install -r requirements.txt")
        sys.exit(1)
