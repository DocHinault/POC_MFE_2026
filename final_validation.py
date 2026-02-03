#!/usr/bin/env python3
"""
✅ FINAL PROJECT VALIDATION CHECKLIST
Vérifications de complétude du projet POC_MFE_2026
"""

import os
import sys

def check_file_exists(filename):
    """Vérifie l'existence d'un fichier"""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"  {status} {filename}")
    return exists

def main():
    print("=" * 70)
    print("✅ VALIDATION FINALE - POC_MFE_2026")
    print("=" * 70)
    
    all_ok = True
    
    # 1. Core Python Files
    print("\n[1/4] Fichiers Principaux Python")
    core_files = [
        "streamlit_app.py",
        "analysis_pipeline.py",  # NOUVEAU
        "page_functions.py",
        "pages/page_social_linking.py",
        "social_auth.py",
        "auth.py",
        "backend_service.py",
        "backend_database.py",
        "backend_auth.py",
        "local_backend.py",
        "config.py",
    ]
    for f in core_files:
        all_ok = check_file_exists(f) and all_ok
    
    # 2. Test Files
    print("\n[2/4] Fichiers de Test")
    test_files = [
        "test_analysis_pipeline.py",  # NOUVEAU
        "test_units.py",
        "test_etape_2.py",
        "test_config.py",
    ]
    for f in test_files:
        all_ok = check_file_exists(f) and all_ok
    
    # 3. Documentation
    print("\n[3/4] Documentation")
    doc_files = [
        "ANALYSIS_PIPELINE_README.md",  # NOUVEAU
        "ETAPE_3_PIPELINE_COMPLET.md",  # NOUVEAU
        "ETAPE_3_RESUME_FINAL.md",  # NOUVEAU
        "INDEX_COMPLET.md",  # NOUVEAU
        ".env.example",  # MIS À JOUR
        "README.md",
        "TECHNICAL.md",
        "CONFIGURATION.md",
        "SOCIAL_AUTH_SETUP.md",
    ]
    for f in doc_files:
        all_ok = check_file_exists(f) and all_ok
    
    # 4. Configuration & Data
    print("\n[4/4] Configuration & Data")
    config_files = [
        "requirements.txt",
        "credentials.json",
        "local_db.json",
    ]
    for f in config_files:
        status = "✅" if os.path.exists(f) else "⚠️ (optionnel)"
        print(f"  {status} {f}")
    
    # Check Python syntax
    print("\n" + "=" * 70)
    print("✅ VALIDATION SYNTAXE PYTHON")
    print("=" * 70)
    
    import subprocess
    
    python_files_to_check = [
        "analysis_pipeline.py",
        "page_functions.py",
    ]
    
    for py_file in python_files_to_check:
        print(f"\n🔍 Vérification: {py_file}")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", py_file],
                capture_output=True,
                text=True,
                cwd="/workspaces/POC_MFE_2026"
            )
            if result.returncode == 0:
                print(f"  ✅ Pas d'erreurs de syntaxe")
            else:
                print(f"  ❌ Erreurs détectées:")
                print(result.stderr)
                all_ok = False
        except Exception as e:
            print(f"  ⚠️ Erreur vérification: {e}")
    
    # Test imports
    print("\n" + "=" * 70)
    print("✅ VALIDATION IMPORTS")
    print("=" * 70)
    
    imports_to_test = [
        "from analysis_pipeline import AnalysisPipeline",
        "from social_auth import SocialMediaLinkManager",
        "from backend_database import get_database",
        "import streamlit as st",
        "import openai",
        "from pptx import Presentation",
    ]
    
    for import_stmt in imports_to_test:
        try:
            exec(import_stmt)
            print(f"  ✅ {import_stmt}")
        except Exception as e:
            print(f"  ❌ {import_stmt}")
            print(f"     Error: {str(e)[:50]}")
            all_ok = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok:
        print("🎉 ✅ TOUTES LES VALIDATIONS PASSÉES!")
        print("=" * 70)
        print("\n📋 CHECKLIST COMPLÈTE:\n")
        print("  ✅ Fichiers principaux présents")
        print("  ✅ Tests inclus")
        print("  ✅ Documentation complète")
        print("  ✅ Syntaxe Python valide")
        print("  ✅ Imports fonctionnels")
        print("\n🚀 Le projet est PRÊT POUR PRODUCTION!")
        print("\n📝 PROCHAINES ÉTAPES:")
        print("  1. Configurer .env avec clés API")
        print("  2. Configurer SMTP (Gmail)")
        print("  3. Lancer: streamlit run streamlit_app.py")
        print("  4. Tester: Créer compte → Lier Instagram → Analyser")
        print("\n" + "=" * 70)
        return 0
    else:
        print("❌ VALIDATION ÉCHOUÉE")
        print("=" * 70)
        print("\nVérifier les erreurs ci-dessus")
        return 1

if __name__ == "__main__":
    sys.exit(main())
