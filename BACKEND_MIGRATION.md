# ⚡ Migration: Backend Python Local (Sans Apps Script)

## 🎉 Changement Principal

L'application **n'utilise plus Google Apps Script** pour l'authentification! Tout est maintenant **100% Python**.

**Avantages:**
- ✅ **Pas de timeout** (plus de 60 secondes!)
- ✅ **Instant** - Les requêtes répondent en <100ms
- ✅ **Contrôle total** - Code Python modifiable
- ✅ **Moins de dépendances** - Pas besoin de Apps Script
- ✅ **Sécurisé** - PBKDF2-SHA256 local

## 📁 Architecture Nouvelle

```
├── streamlit_app.py          # Point d'entrée (initialise le backend)
├── pages.py                  # Pages UI (utilise st.session_state.api)
├── local_backend.py          # Client API local
├── backend_service.py        # Logique métier
├── backend_auth.py           # PBKDF2, hashing, codes
├── backend_cache.py          # Cache en mémoire (codes, OAuth)
├── backend_database.py       # Accès Google Sheets
├── backend_email.py          # Envoi emails via Gmail
└── .env                      # Configuration (NOUVEAU format)
```

## 🔧 Configuration Requise

### 1. Google Sheets (Base de données)

```bash
# Créez un Google Cloud Project
# Activez Google Sheets API et Google Drive API
# Créez une Service Account
# Téléchargez le JSON des credentials
# Partagez votre Google Sheet avec l'email de la service account

# Dans .env:
GOOGLE_SHEETS_ID=votre-sheet-id
GOOGLE_APPLICATION_CREDENTIALS=/chemin/vers/credentials.json
```

### 2. Gmail (Envoi de codes)

```bash
# Activez 2FA sur votre compte Google
# Générez un App Password: https://myaccount.google.com/apppasswords

# Dans .env:
GMAIL_ADDRESS=votre-email@gmail.com
GMAIL_PASSWORD=app-password-16-caracteres
```

### 3. Clé de sécurité

```bash
# Générez une clé aléatoire:
python -c "import secrets; print(secrets.token_hex(32))"

# Copiez le résultat dans .env:
PEPPER_SECRET=votre-clé-ici
```

## 🚀 Lancer l'Application

```bash
# Installation des dépendances (si pas fait)
pip install -r requirements.txt

# Lancer Streamlit
streamlit run streamlit_app.py
```

## 📊 Flux d'Authentification

### Inscription (2 étapes):

1. **register_start(email, password, nom_entreprise, secteur)**
   - Valide l'email et mot de passe
   - Hache le mot de passe avec PBKDF2 (50k itérations)
   - Génère un code 6 chiffres
   - Sauvegarde temporairement dans le cache (15 minutes)
   - **Envoie l'email avec le code**

2. **register_verify(email, code)**
   - Récupère les données temporaires du cache
   - Vérifie le code
   - Crée le client dans Google Sheets
   - Nettoie le cache

### Connexion:

**login(email, password)**
- Récupère le client de Google Sheets
- Vérifie le mot de passe contre le hash PBKDF2
- Implémente le rate limiting (10 tentatives en 15 minutes)
- Retourne id_client si succès

## 🔒 Sécurité

- **Hashing**: PBKDF2-SHA256 avec 50 000 itérations
- **Salting**: Unique par utilisateur/code
- **Pepper**: Clé secrète supplémentaire (PEPPER_SECRET)
- **Rate Limiting**: 10 tentatives max en 15 minutes
- **Cache TTL**: Les codes expirent après 15 minutes
- **Email sécurisé**: Via App Password (pas d'accès direct)

## 🐛 Dépannage

### "DatabaseError" sur inscription
→ Vérifiez que votre Google Sheet existe et est partagée

### "Impossible d'envoyer l'email"
→ Vérifiez GMAIL_ADDRESS et GMAIL_PASSWORD dans .env

### "Cache vide" sur vérification
→ Le code a peut-être expiré (15 min max)

## 📝 Prochaines Étapes

- [ ] Phase 2: OAuth Facebook/Instagram
- [ ] Phase 3: Dashboard avec KPI
- [ ] Phase 4: Rapports et exports

## ✅ Avantages par rapport à Apps Script

| Aspect | Apps Script | Python Local |
|--------|------------|-------------|
| Latence register_start | 60-90s | <100ms |
| Maintenance | Compliquée | Simple (Python) |
| Debugging | Limité | Complet |
| Coût | Gratuit mais lent | Gratuit et rapide |
| Contrôle | Limité | Total |

