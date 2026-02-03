# 📋 Index Complet du Projet - MG POC V1

## 🎯 Fichiers Principaux (Cœur de l'Application)

| Fichier | Description | Statut |
|---------|-------------|--------|
| `streamlit_app.py` | **Point d'entrée** - Routeur principal et configuration initiale | ✅ Complète |
| `auth.py` | Module **authentification** - Hachage, validation, génération codes | ✅ Complète |
| `pages.py` | Module **pages UI** - Inscription, connexion, confirmation, dashboard | ✅ Complète |
| `google_sheets.py` | **Intégration Google Sheets** - Stockage et récupération utilisateurs | ✅ Complète |
| `config.py` | **Configuration** - Variables d'env, secteurs, KPI mapping | ✅ Complète |
| `constants.py` | **Constantes** - Messages d'erreur et patterns | ✅ Complète |

## 📚 Documentation

| Fichier | Audience | Contenu |
|---------|----------|---------|
| `README.md` | Utilisateurs | Guide de démarrage rapide |
| `QUICKSTART.md` | Développeurs | Démo mode et flux de test |
| `TECHNICAL.md` | Développeurs | Architecture technique détaillée |
| `CONFIGURATION.md` | Administrateurs | Configuration des API externes |
| `ROADMAP.md` | Projet Manager | Feuille de route et phases |
| `INDEX.md` | Tous | **Ce fichier** - Index du projet |

## 🧪 Tests et Vérifications

| Fichier | Objectif | Lancer avec |
|---------|----------|------------|
| `test_config.py` | Vérifier configuration et dépendances | `python test_config.py` |
| `test_units.py` | Tests unitaires des fonctions | `python test_units.py` |

## 🔌 Intégrations (Exemples et Phase 2)

| Fichier | Description | Statut |
|---------|-------------|--------|
| `api_examples.py` | Exemples code Facebook/Instagram API | 📋 Prêt pour Phase 2 |

## ⚙️ Configuration et Déploiement

| Fichier | Utilisation |
|---------|-----------|
| `requirements.txt` | Dépendances Python - `pip install -r requirements.txt` |
| `.env.example` | Template variables d'environnement - `cp .env.example .env` |
| `.env` | Variables d'environnement (À créer, non versionné) |
| `.streamlit/config.toml` | Configuration Streamlit (theme, ports, etc.) |

## 🚀 Scripts de Démarrage

| Fichier | Système | Commande |
|---------|---------|----------|
| `start.sh` | Linux/Mac | `./start.sh` ou `bash start.sh` |
| `start.bat` | Windows | `start.bat` ou double-clic |

## 📁 Répertoires

| Répertoire | Contenu |
|-----------|---------|
| `.devcontainer/` | Configuration pour GitHub Codespaces |
| `.streamlit/` | Configuration Streamlit |
| `.git/` | Historique Git |
| `.github/` | Actions GitHub |
| `__pycache__/` | Cache Python (auto-généré) |

## 🔐 Fichiers Secrets (Non versionné)

```
credentials.json       # Google Service Account (créer manuellement)
.env                  # Variables d'environnement (créer à partir de .env.example)
```

## 📊 Structure de Données

### Google Sheets Structure
```
Feuille "Utilisateurs":
Col A | Col B  | Col C     | Col D    | Col E      | Col F | Col G | Col H
------|--------|-----------|----------|------------|-------|-------|-------
Nom   | Email  | Secteur   | Facebook | Instagram  | Date  | Conf  | Session
Ent.  |        |           |          |            |       |       | ID
```

### Session State (Streamlit)
```python
{
    'authenticated': bool,
    'user_email': str,
    'user_data': dict,
    'page': str,
    'auth_mode': str,
    'confirmation_code': str,
    'temp_user_data': dict
}
```

## 🎯 Flux Principal de l'Application

```
streamlit_app.py (ROUTEUR)
    ↓
[Authentifié?]
    ├─ NON → page_auth()
    │        ├─ page_login()
    │        ├─ page_registration()
    │        └─ page_confirmation()
    │
    └─ OUI → page_p1() [Dashboard]
```

## 📦 Dépendances Principales

### Framework
- **streamlit** ≥ 1.28.0 - Framework web interactif

### Google Cloud
- **google-auth-oauthlib** ≥ 1.1.0
- **google-auth-httplib2** ≥ 0.2.0
- **google-api-python-client** ≥ 2.100.0
- **gspread** ≥ 5.12.0

### Utilitaires
- **python-dotenv** ≥ 1.0.0 - Variables d'environnement
- **requests** ≥ 2.31.0 - Requêtes HTTP
- **email-validator** ≥ 2.1.0 - Validation email

### Sécurité
- **bcrypt** ≥ 4.1.0 - Hachage utile en Phase 2
- **PyJWT** ≥ 2.8.0 - JSON Web Tokens pour Phase 2

### Social Media (Phase 2)
- **facebook-sdk** ≥ 3.0.0 - Facebook API
- **instagrapi** ≥ 2.0.0 - Instagram scaping (alternative à API officielle)

## ✅ Checklist Installation

- [ ] `git clone` du projet
- [ ] `pip install -r requirements.txt`
- [ ] `cp .env.example .env`
- [ ] Configuration des variables d'environnement (optionnel)
- [ ] `python test_config.py` pour vérifier
- [ ] `streamlit run streamlit_app.py` pour lancer

## 🎓 Guide de Lecture Recommandé

**Pour les nouveaux développeurs:**
1. `README.md` - Vue d'ensemble
2. `QUICKSTART.md` - Démo et flux de test
3. `TECHNICAL.md` - Architecture et modules
4. Code source - `streamlit_app.py` puis autres modules

**Pour la configuration:**
1. `CONFIGURATION.md` - Détails des API
2. `.env.example` - Variables requises
3. Sections correspondantes dans `TECHNICAL.md`

**Pour l'extension:**
1. `ROADMAP.md` - Prochaines phases
2. `api_examples.py` - Exemples Phase 2
3. `pages.py` - Comment ajouter des pages

## 📝 Conventions du Code

### Nommage
- **Fichiers:** snake_case.py
- **Fonctions:** snake_case()
- **Classes:** PascalCase
- **Constantes:** UPPER_CASE

### Documentation
- Docstrings pour tous les modules
- Commentaires pour la logique complexe
- Type hints recommandés

### Structure
- Imports en haut
- Code à la suite
- Tests à la fin si nécessaire

## 🐛 Dépannage Rapide

| Problème | Solution |
|----------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Google Sheets error" | Vérifier `credentials.json` et `.env` |
| "Port 8501 en utilisation" | `streamlit run --server.port 8502 streamlit_app.py` |
| "Import error local" | Vérifier fichiers `.py` existent |

## 🔗 Liens Utiles

- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram Business API](https://developers.instagram.com/docs)

## 📊 Métriques du Projet

- **Fichiers Python:** 6 (+ exemples)
- **Fichiers de config:** 5
- **Fichiers de documentation:** 4
- **Tests:** 2 fichiers
- **Lignes de code:** ~1000 (cœur)
- **Lignes de doc:** ~2000

## 📅 Historique des Versions

**v1.0.0** (Actuel)
- ✅ Authentification complète
- ✅ Google Sheets intégration
- ✅ Pages structurées
- 🟡 API externe non intégrées
- 🟡 Dashboard P1 vide

**v2.0.0** (Planifié)
- Facebook/Instagram API
- KPI Dashboard
- Rapports

## 👥 Rôles dans le Projet

| Rôle | Fichiers clés | Actions principales |
|------|---|---|
| **Développeur Frontend** | `pages.py`, `streamlit_app.py` | Ajouter pages, améliorer UI |
| **Développeur Backend** | `auth.py`, `google_sheets.py` | Logique, BD, sécurité |
| **DevOps/Déploiement** | `requirements.txt`, `start.sh/bat` | Build, déploiement, CI/CD |
| **Intégrations API** | `api_examples.py`, `config.py` | Facebook, Instagram, réseaux |

## 📞 Support et Questions

Consulter:
1. Les fichiers de documentation (`README.md`, `TECHNICAL.md`)
2. Les commentaires du code
3. `CONFIGURATION.md` pour les API
4. `ROADMAP.md` pour les phases futures

---

**Dernière mise à jour:** février 2026
**Version:** 1.0.0
**Auteur:** Équipe MG
