# Documentation Technique - MG POC V1

## 📋 Vue d'ensemble

MG - POC V1 est une application Streamlit pour la gestion et l'analyse des performances des réseaux sociaux (Facebook, Instagram) adaptée à différents secteurs d'activité.

## 🏗️ Architecture

### Arborescence du Projet

```
POC_MFE_2026/
├── 📄 streamlit_app.py          # Point d'entrée principal
├── 📄 auth.py                   # Module d'authentification
├── 📄 pages.py                  # Module des pages/UI
├── 📄 config.py                 # Configuration et constantes
├── 📄 constants.py              # Messages et constantes
├── 📄 google_sheets.py          # Intégration Google Sheets
├── 📄 api_examples.py           # Exemples d'intégration API (Phase 2)
├── 📄 requirements.txt          # Dépendances Python
├── 📄 .env.example              # Template variables d'environnement
├── 📄 test_config.py            # Tests de configuration
├── 📄 test_units.py             # Tests unitaires
├── 📄 start.sh                  # Script de démarrage Linux/Mac
├── 📄 start.bat                 # Script de démarrage Windows
├── 📄 README.md                 # Documentation utilisateur
├── 📄 CONFIGURATION.md          # Guide de configuration des API
├── 📄 ROADMAP.md                # Feuille de route développement
├── 📄 TECHNICAL.md              # Cette documentation
└── 📄 LICENSE                   # Licence du projet
```

## 🔑 Modules Principaux

### streamlit_app.py
**Point d'entrée** - Routeur principal de l'application

- Configure la page Streamlit
- Initialise l'état de session
- Dirige vers la bonne page selon l'authentification

```python
# Flux:
- Non authentifié → Page Auth (connexion/inscription)
- Authentifié → Page P1 (dashboard)
```

### auth.py
**Module d'authentification** - Gestion des utilisateurs et sécurité

**Fonctions principales:**
- `hash_password()` - Hash PBKDF2 avec salt
- `verify_password()` - Vérification du mot de passe
- `validate_email_format()` - Validation du format email
- `generate_confirmation_code()` - Code de confirmation (6 chars)
- `send_confirmation_email()` - Envoi d'email (SMTP)
- `is_valid_password()` - Critères de sécurité
- `initialize_session_state()` - Initialisation Streamlit

**Critères de mot de passe:**
- Minimum 8 caractères
- Au moins 1 majuscule
- Au moins 1 chiffre

### pages.py
**Module des pages UI** - Interfaces utilisateur

**Pages disponibles:**
1. `page_auth()` - Choix connexion/inscription
2. `page_login()` - Formulaire de connexion
3. `page_registration()` - Formulaire d'inscription
4. `page_confirmation()` - Vérification code email
5. `page_p1()` - Dashboard principal (actuellement vide)

**Features:**
- Validation des champs
- Messages d'erreur clairs
- Vérification des doublons d'email
- Lien vers réseaux sociaux

### config.py
**Configuration** - Variables et paramètres globaux

**Contient:**
- Variables d'environnement
- Listes de secteurs
- Mapping des KPIs par secteur
- Configurations API (Facebook, Instagram)

### google_sheets.py
**Intégration Google Sheets** - Stockage des utilisateurs

**Fonctions:**
- `get_google_sheets_client()` - Connexion à Google Sheets
- `check_email_exists()` - Vérification de doublon
- `save_user_to_sheets()` - Sauvegarde nouvel utilisateur
- `get_user_data()` - Récupération données utilisateur

**Structure Google Sheet:**
```
Colonne A: Nom Entreprise
Colonne B: Email
Colonne C: Secteur
Colonne D: Facebook
Colonne E: Instagram
Colonne F: Date Inscription
Colonne G: Confirmé
Colonne H: ID Session
```

### api_examples.py
**Exemples API** - Code pour Phase 2 (développement futur)

Contient des fonctions d'exemple pour:
- Facebook Insights API
- Instagram Business API
- Agrégation des métriques
- Notifications

## 🔐 Sécurité

### Hachage de Mots de Passe
```
PBKDF2-SHA256
- Salt: 16 bytes (32 hex chars)
- Iterations: 100,000
- Format: "salt$hash"
```

### Validation
- Email: Format standard validé
- Mot de passe: Critères explicites
- Confirmation: Code unique 6 caractères

### Variables Sensibles
- `.env` non versionné (dans .gitignore)
- Google credentials: `credentials.json`
- Tokens: À chiffrer en Phase 2

## 📊 Flux d'Authentification

### Inscription
```
1. Page Auth (choix)
   ↓
2. Page Registration (formulaire)
   - Validation email
   - Vérification doublon
   - Validation mot de passe
   - Connexion FB/IG
   ↓
3. Génération code + Email
   ↓
4. Page Confirmation (code)
   ↓
5. Sauvegarde Google Sheets
   ↓
6. Redirection Page P1
```

### Connexion
```
1. Page Auth (choix)
   ↓
2. Page Login (formulaire)
   - Email
   - Mot de passe
   ↓
3. Vérification dans Google Sheets
   ↓
4. Si OK → Page P1
   Si erreur → Message d'erreur
```

## 🎯 Secteurs et KPIs

### Influenceur
```python
["Engagement", "Reach", "Impressions", "Followers Growth"]
```

### Salle de Sport
```python
["Member Inquiries", "Class Bookings", "Membership Views", "Location Visits"]
```

### Hôtellerie/Restauration
```python
["Reservations", "Menu Views", "Call Clicks", "Website Visits"]
```

## 🚀 Lancement et Déploiement

### Développement Local
```bash
# Clone et installation
git clone <repo>
cd POC_MFE_2026
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec les configurations

# Lancement
streamlit run streamlit_app.py
# OU
./start.sh          # Linux/Mac
start.bat           # Windows
```

### Tests
```bash
# Configuration
python test_config.py

# Unitaires
python test_units.py
```

## 📦 Dépendances Principales

```
streamlit>=1.28.0              # Framework UI
google-auth-oauthlib>=1.1.0    # OAuth Google
google-api-python-client>=2.100 # Google API
gspread>=5.12.0                # Google Sheets
python-dotenv>=1.0.0           # Variables d'env
email-validator>=2.1.0         # Validation email
```

*Voir requirements.txt pour la liste complète*

## 📝 Variables d'Environnement

```env
# Google Sheets
GOOGLE_SHEETS_ID=              # ID du Google Sheet
GOOGLE_CREDENTIALS_PATH=credentials.json

# Facebook
FACEBOOK_APP_ID=               # App ID
FACEBOOK_APP_SECRET=           # App Secret

# Instagram
INSTAGRAM_BUSINESS_ACCOUNT_ID= # Business Account ID

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=                  # Email source
SENDER_PASSWORD=               # App password
```

## 🔧 État de Session Streamlit

```python
st.session_state = {
    'authenticated': False,      # Utilisateur connecté?
    'user_email': None,         # Email de l'utilisateur
    'user_data': None,          # Données complètes
    'page': 'auth',             # Page actuelle
    'auth_mode': None,          # 'login', 'signup', 'confirm'
    'confirmation_code': None,  # Code de confirmation
    'temp_user_data': {}        # Données temporaires inscription
}
```

## 🐛 Dépannage

### "Module non trouvé"
```bash
pip install -r requirements.txt
```

### "Google Sheets connexion échouée"
- Vérifier `credentials.json` existe
- Vérifier clé de service est active
- Vérifier Sheet est partagé avec service account

### "Email non envoyé"
- Vérifier SMTP_SERVER et SMTP_PORT
- Vérifier identifiants email
- Vérifier App Password (si Gmail)

## 📚 Ressources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram Business API](https://developers.instagram.com/docs)

## 🔮 Prochaines Phases

Voir `ROADMAP.md` pour le détail complet

**Phase 2:** Intégration API (Facebook, Instagram)
**Phase 3:** Dashboard avec KPIs
**Phase 4:** Rapports et export
**Phase 5:** Gestion multi-utilisateurs

## 📄 Licence

Voir `LICENSE` pour les détails
