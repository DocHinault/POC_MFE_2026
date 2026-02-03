# 📖 BIENVENUE - POC_MFE_2026

## C'est quoi ?

Un **tableau de bord social media intelligent** qui :
- 📊 Récupère vos KPI Instagram & Facebook
- 🤖 Analyse vos performances avec l'IA (GPT)
- 📄 Génère un rapport PowerPoint professionnel
- 📧 Envoie le rapport par email automatiquement
- 💾 Sauvegarde les données sur Google Sheets

## ⚡ Démarrage en 2 minutes

### 1. Configuration (Une fois)
```bash
# Copier le fichier de configuration
cp .env.example .env

# Remplir les 4 variables essentielles:
# - OPENAI_API_KEY (pour l'IA)
# - SMTP_EMAIL et SMTP_PASSWORD (pour les emails)
# - FACEBOOK_APP_ID et FACEBOOK_APP_SECRET (pour la connexion)

# Lancer le script de démarrage
bash quickstart.sh
```

### 2. Lancer l'app
```bash
streamlit run streamlit_app.py --server.port=8503
```

### 3. Utiliser
```
1. Accédez à http://localhost:8503
2. Créez un compte
3. Liez votre Instagram et Facebook
4. Cliquez "Lancer l'analyse"
5. Reçevez votre rapport par email!
```

## 📋 Fichiers Importants

| Fichier | Description |
|---------|-------------|
| `streamlit_app.py` | App principale |
| `analysis_pipeline.py` | **Nouveau** - Pipeline d'analyse |
| `page_functions.py` | Toutes les pages (1400+ lignes) |
| `.env` | Configuration (à remplir!) |
| `requirements.txt` | Dépendances Python |

## 📚 Documentation

Pour **commencer rapidement** → [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)

Pour **comprendre le pipeline** → [ANALYSIS_PIPELINE_README.md](ANALYSIS_PIPELINE_README.md)

Pour **détails techniques** → [ETAPE_3_PIPELINE_COMPLET.md](ETAPE_3_PIPELINE_COMPLET.md)

Pour **structure du projet** → [INDEX_COMPLET.md](INDEX_COMPLET.md)

## 🔑 Variables d'Environnement Requises

```bash
# OpenAI API (pour l'analyse avec GPT)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Email (pour envoyer les rapports)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=votre-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # App Password (pas votre mdp!)

# Facebook (pour connecter Instagram/Facebook)
FACEBOOK_APP_ID=xxxxxxxxxxxxx
FACEBOOK_APP_SECRET=xxxxxxxxxxxxx
```

## ⚙️ Configuration Gmail

Pour utiliser **Gmail comme serveur SMTP**:

1. Aller sur: https://myaccount.google.com/
2. Security → 2-Step Verification (activer)
3. Security → App Passwords → Sélectionner "Mail" et "Windows Computer"
4. Copier le password (16 caractères)
5. Mettre dans `.env` comme `SMTP_PASSWORD`

## 🧪 Tests

Valider que tout fonctionne:
```bash
python3 final_validation.py      # Validation complète
python3 test_analysis_pipeline.py # Tests spécifiques au pipeline
```

## 🆘 Problèmes Courants

### "No API key provided"
→ Ajouter `OPENAI_API_KEY` dans `.env`

### "SMTP authentication failed"
→ Utiliser un **App Password** Gmail, pas votre mot de passe normal

### "Instagram token expired"
→ Relancer la liaison OAuth depuis l'onglet "Liaison"

### "PowerPoint ne s'ouvre pas"
→ Vérifier que vous avez Microsoft Office ou LibreOffice

## 📊 Ce qui se passe quand vous lancez l'analyse

```
Vous cliquez → Récupère vos posts Instagram/Facebook
"Lancer"     ↓
             → Analyse avec GPT pour recommandations
             ↓
             → Génère un PowerPoint de 8 slides
             ↓
             → Envoie tout par email
             ↓
             Vous recevez un rapport professionnel!
```

## 🎯 Cas d'Usage

### Pour une PME
```
Semaine 1: Lier compte Instagram et Facebook
Semaine 2: Lancer première analyse
Semaine 3: Reçoit rapport avec 3 idées de posts
Semaine 4: Implémente les recommandations
```

### Pour une Agence
```
Gérer 10 clients
Lancer 10 analyses en 1 clic
Générer 10 rapports
Facture comme "Social Media Audit"
```

## 🚀 Optimisations

Pour meilleure performance:
- Utiliser les **App Passwords** Gmail (plus rapide que les mots de passe normaux)
- Cacher le powerpoint généré (sauvegarde temps)
- Scheduler les analyses (éviter surcharge)

## 📞 Support

1. Vérifier la documentation (`EXECUTIVE_SUMMARY.md`)
2. Lancer les tests (`python3 final_validation.py`)
3. Vérifier les logs (`streamlit run ... --logger.level=debug`)

## ✨ Prochaines Améliorations

- [ ] Historique des analyses (12 mois)
- [ ] Dashboard de tendances
- [ ] Scheduling automatique (emails hebdo)
- [ ] Comparaison industry (benchmarking)
- [ ] Support TikTok & YouTube

## 📝 Notes

- L'app est **entièrement fonctionnelle**
- Tous les **tests passent** (100%)
- **Production-ready** (prêt à déployer)
- **Sécurisé** (tokens, SMTP TLS)

## 🎊 C'est Prêt!

Tout est configuré, testé et documenté.

Il vous suffit de:
1. Remplir `.env` avec vos clés
2. Lancer `streamlit run streamlit_app.py`
3. Créer un compte et profiter!

**Bon usage! 🚀**

---

Pour plus d'infos: voir [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
