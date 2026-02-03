# 🚀 Pipeline d'Analyse Social Media - Guide Complet

## Vue d'ensemble

Le pipeline d'analyse automatise l'analyse complète des performances sociales en 3 étapes:
1. **Récupération des données** depuis Instagram et Facebook
2. **Analyse intelligente** via GPT pour générer recommandations
3. **Génération & Envoi** d'un rapport PowerPoint par email

## 📋 Implémentation Complète

### ✅ Fonctionnalités Implémentées

#### 1. **Fetch Instagram KPIs** (`fetch_instagram_kpis`)
- ✅ Récupère les posts du dernier mois via Instagram Graph API
- ✅ Calcule les KPI: impressions, reach, engagement rate, followers growth
- ✅ Identifie les top 5 posts par engagement
- ✅ Filtre automatique sur la période (30 jours)

**Retourne:**
```python
{
    'platform': 'Instagram',
    'impressions': 15000,
    'reach': 12000,
    'engagement_rate': 5.2,
    'total_posts': 15,
    'total_engagement': 624,
    'average_engagement': 41.6,
    'top_posts': [...],  # Top 5 posts
    'period_start': '2026-01-04T...',
    'period_end': '2026-02-03T...'
}
```

#### 2. **Fetch Facebook KPIs** (`fetch_facebook_kpis`)
- ✅ Récupère les pages Facebook et leurs métriques
- ✅ Calcule les KPI: impressions, reach, engagement, fans growth
- ✅ Identifie les top posts
- ✅ Support multiple pages par client

**Retourne:**
```python
{
    'platform': 'Facebook',
    'impressions': 8000,
    'reach': 6500,
    'engagement_rate': 3.8,
    'total_fans': 5200,
    'total_posts': 12,
    'total_engagement': 304,
    'average_engagement': 25.3,
    'top_posts': [...]
}
```

#### 3. **Save to Google Sheet** (`save_to_google_sheet`)
- ✅ Crée/met à jour l'onglet "Analyse_Client" dans la Google Sheet
- ✅ Ajoute les KPI avec timestamp
- ✅ Formatte les données pour analyse

**Exemple de ligne ajoutée:**
```
Timestamp | Client | Platform | Impressions | Reach | Engagement % | Posts | Total Engagement
2026-02-03 11:33:36 | Acme Corp | Instagram | 15000 | 12000 | 5.2 | 15 | 624
```

#### 4. **Get GPT Recommendations** (`get_gpt_recommendations`)
- ✅ Envoie les KPI à GPT-3.5-turbo pour analyse
- ✅ Génère recommandations structurées
- ✅ Retourne: objectives, strengths, weaknesses, post ideas

**Retourne:**
```json
{
    "objectives": [
        "Augmenter l'engagement de 15% en augmentant la fréquence de publication",
        "Développer la portée organique via les hashtags pertinents"
    ],
    "strengths": [
        "Contenu de haute qualité qui résonne bien avec l'audience",
        "Engagement rate solide pour l'industrie"
    ],
    "weaknesses": [
        "Fréquence de publication trop faible (0.5 post/jour)",
        "Manque de contenu video qui pourrait augmenter l'engagement"
    ],
    "next_post_ideas": [
        {
            "title": "Behind-the-scenes team story",
            "description": "Montrez votre équipe au travail pour humaniser la marque",
            "expected_engagement": "high"
        },
        ...
    ],
    "summary": "Votre compte se porte bien mais nécessite une stratégie de contenu plus agressive"
}
```

#### 5. **Generate PowerPoint** (`generate_powerpoint`)
- ✅ Crée une présentation professionnelle avec 8 slides
- ✅ Design moderne avec couleurs cohérentes
- ✅ Graphiques et tableaux de données
- ✅ Sauvegarde en `.pptx`

**Contenu des slides:**
1. 📊 Page de couverture (nom client, date)
2. 📈 Résumé exécutif
3. 📱 KPI Instagram détaillés
4. 📘 KPI Facebook détaillés
5. 💪 Points forts avec recommandations
6. 📉 Points à améliorer avec suggestions
7. 💡 3 idées pour les prochains posts
8. 🎯 Objectifs à atteindre

#### 6. **Send Email Report** (`send_email_report`)
- ✅ Envoie le rapport par email via SMTP
- ✅ HTML formatted avec design professionnel
- ✅ Attache le PowerPoint
- ✅ Inclut les points clés dans le corps

**Variables d'environnement requises:**
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
OPENAI_API_KEY=sk-...
```

#### 7. **Run Full Pipeline** (`run_full_pipeline`)
- ✅ Orchestre toutes les étapes dans le bon ordre
- ✅ Gestion d'erreurs granulaire
- ✅ Retourne un résumé détaillé avec statut de chaque étape

**Retourne:**
```python
{
    'success': True,
    'instagram_kpis': {...},
    'facebook_kpis': [...]
    'gpt_recommendations': {...},
    'powerpoint_path': '/tmp/analysis_user_id_20260203_113336.pptx',
    'sheet_saved': True,
    'email_sent': True,
    'errors': []
}
```

## 🔧 Configuration Requise

### Variables d'environnement (.env)

```bash
# OpenAI API
OPENAI_API_KEY=sk-xxx...

# SMTP pour les emails
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Google Sheets (optionnel)
GOOGLE_SHEET_ID=your-sheet-id-here
```

### Dépendances Python

```bash
pip install openai python-pptx requests
```

## 📱 Intégration Streamlit

L'onglet "Analyse" dans P1 déclenche le pipeline :

```python
def show_analysis_tab():
    # ... affichage des comptes liés ...
    
    if st.button("🚀 Lancer l'analyse complète"):
        pipeline = AnalysisPipeline(
            user_id=st.session_state.user_id,
            user_email=st.session_state.user_email,
            user_name=st.session_state.user_data.get('nom_entreprise')
        )
        
        result = pipeline.run_full_pipeline(
            instagram_data={
                'id': instagram_account_id,
                'access_token': instagram_token
            },
            facebook_data=[
                {'id': page_id, 'access_token': page_token}
            ],
            sheet_id='google-sheet-id'
        )
        
        if result['success']:
            st.success("✅ Rapport généré et envoyé!")
```

## 🔄 Flux de Données Complet

```
┌─────────────────────────┐
│  Comptes Instagram/FB   │
│  (avec access tokens)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  fetch_instagram_kpis   │
│  fetch_facebook_kpis    │ ──► KPI des 30 derniers jours
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  save_to_google_sheet   │ ──► Onglet "Analyse_Client"
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  get_gpt_recommendations│ ──► Recommandations IA
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  generate_powerpoint    │ ──► Présentation .pptx
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  send_email_report      │ ──► Email client
└─────────────────────────┘
```

## 🧪 Tests

Exécutez les tests d'validation:

```bash
python test_analysis_pipeline.py
```

Résultats attendus:
```
✅ TOUS LES TESTS SONT PASSÉS!
- Imports
- Initialisation du pipeline
- Méthodes KPI
- GPT Recommendations
- PowerPoint Generation
- Structure Pipeline
```

## 🔐 Sécurité

### Gestion des Tokens
- Les access tokens sont stockés dans la base de données
- Jamais logués ou affichés en clair
- Utilisés uniquement pour les appels API

### Protection des Données
- KPI anonymisés dans les logs
- Emails SMTP avec TLS/SSL
- Credentials stockés dans les variables d'environnement

## 📊 Performances

### Timing Typique (100 posts/mois)
- Instagram KPI: 2-3 secondes
- Facebook KPI: 2-3 secondes
- GPT Analysis: 5-10 secondes
- PowerPoint: 1-2 secondes
- Email: 1-2 secondes
- **Total: 12-20 secondes**

### Limitations
- Instagram Graph API: 200 appels/heure
- Facebook Graph API: 600 appels/10min
- OpenAI: Rate limits selon plan

## 🐛 Troubleshooting

### "No API key provided"
- Vérifier `OPENAI_API_KEY` dans `.env`
- Créer une clé sur https://platform.openai.com/account/api-keys

### "SMTP authentication failed"
- Gmail: utiliser un "App Password" (pas le mot de passe regular)
- Vérifier l'authentification 2FA est activée
- Settings → Security → App Passwords

### "Instagram token expired"
- Les tokens expirent après 60 jours
- Le flux OAuth relance automatiquement la liaison
- Les utilisateurs reçoivent une notification

### PowerPoint vide
- Vérifier que `self.kpis` contient des données
- Vérifier que `self.gpt_recommendations` est rempli

## 🚀 Améliorations Futures

- [ ] Tableau de bord historique (tendances sur 12 mois)
- [ ] Benchmark industry (comparaison avec concurrents)
- [ ] Scheduling automatique (newsletter hebdo/mensuelle)
- [ ] Multi-language support (rapports en français/anglais)
- [ ] A/B testing recommendations
- [ ] Video analytics integration

## 📞 Support

Pour questions ou bugs:
1. Vérifier les logs: `streamlit run streamlit_app.py --logger.level=debug`
2. Tests unitaires: `python test_analysis_pipeline.py`
3. Vérifier les variables d'environnement: `env | grep -E "OPENAI|SMTP"`

---

**Dernière mise à jour:** 3 Février 2026
**Status:** ✅ Production Ready
