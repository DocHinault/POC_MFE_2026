"""
Script de test complet de l'application
À exécuter pour vérifier que tout fonctionne correctement
"""

def test_password_hashing():
    """Test le hachage et la vérification des mots de passe"""
    from auth import hash_password, verify_password
    
    print("Test 1: Hachage des mots de passe")
    password = "TestPassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed), "Vérification du mot de passe échouée"
    assert not verify_password("WrongPassword", hashed), "Faux mot de passe accepté"
    
    print("✅ Test de hachage réussi")


def test_email_validation():
    """Test la validation des emails"""
    from auth import validate_email_format
    
    print("\nTest 2: Validation des emails")
    
    valid_emails = ["test@example.com", "user@domain.co.uk"]
    invalid_emails = ["invalid@", "@invalid.com", "no-at-sign.com"]
    
    for email in valid_emails:
        assert validate_email_format(email), f"Email valide rejeté: {email}"
    
    for email in invalid_emails:
        assert not validate_email_format(email), f"Email invalide accepté: {email}"
    
    print("✅ Test de validation d'email réussi")


def test_password_criteria():
    """Test les critères de sécurité du mot de passe"""
    from auth import is_valid_password
    
    print("\nTest 3: Critères de sécurité du mot de passe")
    
    # Mot de passe valide
    valid, msg = is_valid_password("ValidPass123")
    assert valid, f"Mot de passe valide rejeté: {msg}"
    
    # Trop court
    valid, msg = is_valid_password("Short1")
    assert not valid, "Mot de passe trop court accepté"
    
    # Pas de majuscule
    valid, msg = is_valid_password("lowercase123")
    assert not valid, "Mot de passe sans majuscule accepté"
    
    # Pas de chiffre
    valid, msg = is_valid_password("NoNumber")
    assert not valid, "Mot de passe sans chiffre accepté"
    
    print("✅ Test des critères de sécurité réussi")


def test_confirmation_code():
    """Test la génération du code de confirmation"""
    from auth import generate_confirmation_code
    
    print("\nTest 4: Code de confirmation")
    
    code1 = generate_confirmation_code()
    code2 = generate_confirmation_code()
    
    assert len(code1) == 6, "Code de longueur incorrecte"
    assert code1 != code2, "Codes identiques générés"
    assert code1.isupper(), "Code non en majuscule"
    
    print(f"✅ Test du code de confirmation réussi (exemples: {code1}, {code2})")


def test_session_state():
    """Test l'initialisation de l'état de session"""
    import streamlit as st
    from auth import initialize_session_state
    
    print("\nTest 5: État de session")
    
    initialize_session_state()
    
    assert 'authenticated' in st.session_state
    assert 'user_email' in st.session_state
    assert 'page' in st.session_state
    assert st.session_state.authenticated == False
    assert st.session_state.page == "auth"
    
    print("✅ Test de l'état de session réussi")


def test_imports():
    """Test l'importation de tous les modules"""
    print("\nTest 6: Importation des modules")
    
    modules = ['config', 'auth', 'pages', 'google_sheets', 'constants', 'api_examples']
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except Exception as e:
            print(f"  ❌ {module}: {e}")
            raise


def test_constants():
    """Test les constantes"""
    from constants import MESSAGES
    from config import SECTEURS, KPI_MAPPING
    
    print("\nTest 7: Constantes")
    
    assert len(MESSAGES) > 0, "Messages vides"
    assert len(SECTEURS) == 3, "Nombre de secteurs incorrect"
    assert all(secteur in KPI_MAPPING for secteur in SECTEURS), "KPI mapping incomplet"
    
    print(f"✅ Test des constantes réussi ({len(SECTEURS)} secteurs)")


if __name__ == "__main__":
    print("=" * 60)
    print("MG - POC V1 - Tests Unitaires")
    print("=" * 60)
    
    try:
        test_imports()
        test_password_hashing()
        test_email_validation()
        test_password_criteria()
        test_confirmation_code()
        test_constants()
        test_session_state()
        
        print("\n" + "=" * 60)
        print("🎉 Tous les tests sont passés avec succès!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test échoué: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        exit(1)
