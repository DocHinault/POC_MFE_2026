✅ CHECKLIST DE LANCEMENT - MG POC V1

═══════════════════════════════════════════════════════════════════════════════

📋 PRE-LANCEMENT (AVANT DE DÉMARRER)

PRÉREQUIS SYSTÈME:
  [ ] Python 3.8+ installé
  [ ] pip installé
  [ ] 100MB d'espace disque disponible
  [ ] Connexion Internet (pour les dépendances)

CLONAGE DU PROJET:
  [ ] Dossier /workspaces/POC_MFE_2026 accessible
  [ ] Tous les fichiers .py présents
  [ ] Tous les fichiers .md présents
  [ ] requirements.txt présent

═══════════════════════════════════════════════════════════════════════════════

🔧 INSTALLATION (5 minutes)

ÉTAPE 1: INSTALLER LES DÉPENDANCES
  [ ] Exécuter: pip install -r requirements.txt
  [ ] Tous les packages installés sans erreur
  [ ] Pas de warnings critiques

ÉTAPE 2: VÉRIFIER L'INSTALLATION
  [ ] Exécuter: python test_config.py
  [ ] Tous les tests passent (✅)
  [ ] Import des modules réussis

ÉTAPE 3: (OPTIONNEL) CONFIGURER GOOGLE SHEETS
  [ ] Créer fichier .env: cp .env.example .env
  [ ] Remplir les variables GOOGLE_SHEETS_ID
  [ ] Ajouter le fichier credentials.json
  [ ] Tester la connexion (voir CONFIGURATION.md)

═══════════════════════════════════════════════════════════════════════════════

🎬 LANCEMENT (2 façons)

MÉTHODE 1: LIGNE DE COMMANDE
  [ ] Terminal ouvert dans le dossier du projet
  [ ] Exécuter: streamlit run streamlit_app.py
  [ ] Message de démarrage visible
  [ ] Application accessible à http://localhost:8501

MÉTHODE 2: SCRIPT DE DÉMARRAGE
  [ ] Sur Linux/Mac: ./start.sh
  [ ] Sur Windows: start.bat (double-clic ou cmd)
  [ ] Vérification des dépendances
  [ ] Application accessible à http://localhost:8501

═══════════════════════════════════════════════════════════════════════════════

✨ TEST DE FONCTIONNALITÉ (10 minutes)

PAGE D'ACCUEIL:
  [ ] Voir titre "MG - POC V1 - Social Media Reporting"
  [ ] Boutons "Inscription" et "Connexion" visibles
  [ ] Navigation correcte

TEST D'INSCRIPTION:
  [ ] Cliquer sur "Inscription"
  [ ] Remplir:
    [ ] Nom de l'entreprise
    [ ] Secteur (vérifier dropdown)
    [ ] Email valide (ex: test@example.com)
    [ ] Mot de passe (8+ chars, 1 maj, 1 chiffre)
    [ ] Confirmation mot de passe
  [ ] Vérifier boutons Facebook/Instagram
  [ ] Clicker "Créer un compte"
  [ ] Voir page de confirmation
  [ ] Code de confirmation généré (voir console)
  [ ] Entrer le code et confirmer
  [ ] Être redirigé vers Page P1

PAGE P1 (DASHBOARD):
  [ ] Voir information de l'entreprise
  [ ] Voir le secteur choisi
  [ ] Bouton "Déconnexion" visible
  [ ] Affichage "Page en développement"

DÉCONNEXION:
  [ ] Cliquer "Déconnexion"
  [ ] Revenir à la page d'authentification
  [ ] État de session réinitialisé

TEST DE CONNEXION:
  [ ] Cliquer "Connexion"
  [ ] Entrer l'email créé précédemment
  [ ] Entrer le mot de passe
  [ ] Être redirigé vers Page P1
  [ ] Voir les mêmes informations

VALIDATION DES FORMULAIRES:
  [ ] Email invalide → message d'erreur
  [ ] Mot de passe trop court → message d'erreur
  [ ] Mots de passe non identiques → message d'erreur
  [ ] Email déjà utilisé → message d'erreur

═══════════════════════════════════════════════════════════════════════════════

🔒 TESTS DE SÉCURITÉ

MOT DE PASSE:
  [ ] Minimum 8 caractères requis
  [ ] Au moins 1 majuscule requis
  [ ] Au moins 1 chiffre requis
  [ ] Hachage du mot de passe réalisé
  [ ] Pas de stockage du mot de passe en clair

EMAIL:
  [ ] Format validé (xxx@yyy.zzz)
  [ ] Doublon détecté (si Google Sheets configuré)
  [ ] Case-insensitive pour les vérifications

CODE DE CONFIRMATION:
  [ ] Généré aléatoirement
  [ ] 6 caractères
  [ ] Unique pour chaque inscription
  [ ] Vérifié strictement à la confirmation

═══════════════════════════════════════════════════════════════════════════════

📊 TESTS UNITAIRES (OPTIONNEL)

EXÉCUTER LES TESTS:
  [ ] Exécuter: python test_units.py
  [ ] 7 tests unitaires doivent passer
  [ ] Tous les modules importés correctement
  [ ] Les fonctions d'authentification fonctionnent
  [ ] Les validations fonctionnent

═══════════════════════════════════════════════════════════════════════════════

🌐 TESTS D'INTÉGRATION GOOGLE SHEETS (SI CONFIGURÉ)

CONFIGURATION:
  [ ] Fichier credentials.json est présent
  [ ] Variables d'environnement correctes dans .env
  [ ] Clés de service actives dans Google Cloud

FONCTIONNALITÉ:
  [ ] Inscription sauvegarde dans Google Sheets
  [ ] Vérification de doublon fonctionne
  [ ] Récupération des données utilisateur fonctionne
  [ ] Feuille "Utilisateurs" créée automatiquement

═══════════════════════════════════════════════════════════════════════════════

🐛 DÉPANNAGE COURANT

SI ERREUR "Module not found":
  [ ] Exécuter: pip install -r requirements.txt
  [ ] Vérifier version Python >= 3.8
  [ ] Vérifier internet pour télécharger les packages

SI ERREUR "Port 8501 already in use":
  [ ] Tuer les processus Streamlit: pkill -f streamlit
  [ ] Lancer sur un autre port: streamlit run --server.port 8502 streamlit_app.py

SI ERREUR "Google Sheets":
  [ ] Vérifier credentials.json existe
  [ ] Vérifier permissions du fichier
  [ ] Vérifier GOOGLE_SHEETS_ID dans .env

SI ERREUR "Email not sent":
  [ ] C'est normal en mode démo (pas d'SMTP)
  [ ] Configurer Gmail si vous voulez vraiment envoyer
  [ ] Voir CONFIGURATION.md

═══════════════════════════════════════════════════════════════════════════════

✅ CHECKLIST FINALE

AVANT DE CONSIDÉRER COMME "PRÊT POUR LA PRODUCTION":

CODE:
  [ ] Tous les fichiers .py sont présents
  [ ] test_units.py passe tous les tests
  [ ] test_config.py valide la configuration

DOCUMENTATION:
  [ ] README.md lu et compris
  [ ] TECHNICAL.md consulté pour architecture
  [ ] INDEX.md peut servir de guide

CONFIGURATION:
  [ ] .env configuré (si utilisation réelle)
  [ ] credentials.json placé (si Google Sheets)
  [ ] requirements.txt installé

FONCTIONNALITÉS:
  [ ] Page d'authentification fonctionne
  [ ] Inscription fonctionne
  [ ] Connexion fonctionne
  [ ] Page P1 accessible
  [ ] Déconnexion fonctionne

═══════════════════════════════════════════════════════════════════════════════

📞 EN CAS DE PROBLÈME

RESSOURCES:
  1. Lire le fichier correspondant dans /docs:
     - README.md pour utilisation générale
     - TECHNICAL.md pour architecture
     - CONFIGURATION.md pour API
     - QUICKSTART.md pour démo

  2. Vérifier les commentaires du code dans les fichiers .py

  3. Exécuter les tests pour identifier le problème
     - python test_config.py
     - python test_units.py

  4. Vérifier la configuration
     - .env existe et est complét
     - credentials.json est présent
     - requirements.txt installé

═══════════════════════════════════════════════════════════════════════════════

🎯 OBJECTIFS DE CETTE VERSION (v1.0.0)

✅ ATTEINTS:
  • Authentification complète
  • Validation des formulaires
  • Sécurité des mots de passe
  • Intégration Google Sheets
  • Architecture modulaire
  • Documentation exhaustive
  • Tests inclus

🔮 POUR LES VERSIONS FUTURES:
  • API Facebook et Instagram
  • Dashboard avec KPIs
  • Rapports automatisés
  • Gestion multi-utilisateurs

═══════════════════════════════════════════════════════════════════════════════

✨ DÉMARRAGE FINAL

Quand vous êtes prêt:

1. Terminal dans /workspaces/POC_MFE_2026
2. pip install -r requirements.txt
3. streamlit run streamlit_app.py
4. Ouvrir http://localhost:8501

L'application démarrera directement sur la page d'authentification!

═══════════════════════════════════════════════════════════════════════════════

Date: Février 2026
Version: 1.0.0
Status: ✅ PRÊT POUR UTILISATION
