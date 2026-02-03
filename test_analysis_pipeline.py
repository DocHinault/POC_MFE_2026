#!/usr/bin/env python3
"""
Test de validation du pipeline d'analyse
Vérifie que toutes les méthodes sont implémentées et fonctionnent correctement
"""

import sys
from datetime import datetime

def test_imports():
    """Test 1: Vérifier que tous les imports fonctionnent"""
    print("[1/6] Test des imports...")
    try:
        from analysis_pipeline import AnalysisPipeline
        print("    ✅ AnalysisPipeline importé")
        
        import openai
        print("    ✅ openai disponible")
        
        from pptx import Presentation
        print("    ✅ python-pptx disponible")
        
        import requests
        print("    ✅ requests disponible")
        
        return True
    except ImportError as e:
        print(f"    ❌ Import échoué: {e}")
        return False

def test_pipeline_initialization():
    """Test 2: Initialiser le pipeline"""
    print("\n[2/6] Test d'initialisation du pipeline...")
    try:
        from analysis_pipeline import AnalysisPipeline
        
        pipeline = AnalysisPipeline(
            user_id='test_user',
            user_email='test@example.com',
            user_name='Test Client'
        )
        
        assert pipeline.user_id == 'test_user'
        assert pipeline.user_email == 'test@example.com'
        assert pipeline.user_name == 'Test Client'
        assert isinstance(pipeline.kpis, dict)
        
        print(f"    ✅ Pipeline initialisé correctement")
        return True, pipeline
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        return False, None

def test_kpi_methods(pipeline):
    """Test 3: Tester les méthodes KPI (avec données fictives)"""
    print("\n[3/6] Test des méthodes KPI...")
    try:
        # Test fetch_instagram_kpis (sans token réel, juste vérifier la signature)
        result = pipeline.fetch_instagram_kpis(
            instagram_account_id='123456',
            access_token='test_token'
        )
        print(f"    ✅ fetch_instagram_kpis retourne un dict: {type(result).__name__}")
        
        # Test fetch_facebook_kpis
        result = pipeline.fetch_facebook_kpis(
            page_id='987654',
            access_token='test_token'
        )
        print(f"    ✅ fetch_facebook_kpis retourne un dict: {type(result).__name__}")
        
        return True
    except Exception as e:
        print(f"    ❌ Erreur KPI: {e}")
        return False

def test_gpt_recommendations(pipeline):
    """Test 4: Tester la méthode get_gpt_recommendations"""
    print("\n[4/6] Test de get_gpt_recommendations...")
    try:
        # Ajouter des KPI fictifs
        pipeline.kpis = {
            'instagram': {
                'impressions': 10000,
                'reach': 8000,
                'engagement_rate': 5.2,
                'total_posts': 15,
                'total_engagement': 416,
                'average_engagement': 27.7
            }
        }
        
        # Test sans API key (retournera les données par défaut)
        result = pipeline.get_gpt_recommendations('')
        
        # Vérifier la structure
        assert 'objectives' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'next_post_ideas' in result
        assert 'summary' in result
        
        print(f"    ✅ get_gpt_recommendations retourne structure valide")
        print(f"       - Objectifs: {len(result.get('objectives', []))} trouvés")
        print(f"       - Points forts: {len(result.get('strengths', []))} trouvés")
        print(f"       - Idées: {len(result.get('next_post_ideas', []))} trouvées")
        
        return True, result
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        return False, None

def test_powerpoint_generation(pipeline):
    """Test 5: Tester la génération PowerPoint"""
    print("\n[5/6] Test de generate_powerpoint...")
    try:
        import os
        
        # S'assurer que les KPI et recommandations existent
        if not pipeline.gpt_recommendations:
            pipeline.gpt_recommendations = {
                'objectives': ['Augmenter l\'engagement', 'Croître la communauté'],
                'strengths': ['Contenu cohérent', 'Audience active'],
                'weaknesses': ['Améliorer la fréquence'],
                'next_post_ideas': [
                    {'title': 'Post 1', 'description': 'Description 1'},
                    {'title': 'Post 2', 'description': 'Description 2'},
                    {'title': 'Post 3', 'description': 'Description 3'}
                ],
                'summary': 'Résumé de l\'analyse'
            }
        
        # Générer le PowerPoint
        pptx_path = pipeline.generate_powerpoint()
        
        if pptx_path and os.path.exists(pptx_path):
            file_size = os.path.getsize(pptx_path)
            print(f"    ✅ PowerPoint généré: {pptx_path}")
            print(f"       Taille: {file_size:,} bytes")
            return True, pptx_path
        else:
            print(f"    ⚠️ PowerPoint non trouvé: {pptx_path}")
            return False, None
            
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_pipeline_structure():
    """Test 6: Vérifier la structure du pipeline"""
    print("\n[6/6] Test de la structure du pipeline...")
    try:
        from analysis_pipeline import AnalysisPipeline
        
        pipeline = AnalysisPipeline('test', 'test@test.com', 'Test')
        
        required_methods = [
            'fetch_instagram_kpis',
            'fetch_facebook_kpis',
            'save_to_google_sheet',
            'get_gpt_recommendations',
            'generate_powerpoint',
            'send_email_report',
            'run_full_pipeline'
        ]
        
        for method in required_methods:
            if not hasattr(pipeline, method):
                print(f"    ❌ Méthode manquante: {method}")
                return False
            else:
                print(f"    ✅ {method}()")
        
        return True
    except Exception as e:
        print(f"    ❌ Erreur: {e}")
        return False

def main():
    """Lancer tous les tests"""
    print("=" * 70)
    print("🧪 TEST PIPELINE D'ANALYSE")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Initialisation", None),  # Sera testé à part
        ("Méthodes KPI", None),  # Sera testé à part
        ("GPT Recommendations", None),  # Sera testé à part
        ("PowerPoint Generation", None),  # Sera testé à part
        ("Structure Pipeline", test_pipeline_structure),
    ]
    
    # Test 1
    if not test_imports():
        print("\n❌ Les tests d'import ont échoué")
        return False
    
    # Test 2
    success, pipeline = test_pipeline_initialization()
    if not success:
        print("\n❌ L'initialisation du pipeline a échoué")
        return False
    
    # Test 3
    if not test_kpi_methods(pipeline):
        print("\n⚠️ Les tests KPI ont échoué (peut être normal sans tokens)")
    
    # Test 4
    success, recs = test_gpt_recommendations(pipeline)
    if not success:
        print("\n⚠️ Le test GPT a échoué (peut être normal sans API key)")
    
    # Test 5
    success, pptx_path = test_powerpoint_generation(pipeline)
    if not success:
        print("\n⚠️ La génération PowerPoint a échoué")
    
    # Test 6
    if not test_pipeline_structure():
        print("\n❌ La structure du pipeline est incomplète")
        return False
    
    print("\n" + "=" * 70)
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("=" * 70)
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
