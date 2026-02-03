# 🏗️ NOUVELLE ARCHITECTURE MODULAIRE - v3.2.0

## ✅ Réorganisation Complète

Votre code a été réorganisé en **modules thématiques**:

```
src/
├── auth/           # Tout sur l'authentification
├── social/         # Tout sur les réseaux sociaux
├── analysis/       # Tout sur l'analyse (KPI, GPT, PPT, Email)
├── profile/        # Tout sur le profil + sélection KPI par secteur
├── backend/        # Services backend
├── ui/             # Composants UI réutilisables
└── config/         # Configuration + KPI par secteur + Prompts GPT
```

##  🎯 Nouveautés Principales

### 1. **Sélection KPI par Secteur** (`src/profile/kpi_selector.py`)
```python
from src.profile import get_kpis_for_sector, get_gpt_prompt_for_sector

# Récupérer les KPIs pour un secteur
kpis = get_kpis_for_sector("Influenceur")
# → ["Engagement", "Reach", "Impressions", "Followers Growth"]

# Récupérer le prompt GPT pour un secteur
prompt = get_gpt_prompt_for_sector("Salle de sport")
# → "Analyse les KPIs d'une salle de sport..."
```

### 2. **Prompts GPT Personnalisés** (`src/config/settings.py`)
Chaque secteur a maintenant son **prompt GPT optimisé**:
- **Influenceur**: Focus engagement, reach, croissance
- **Salle de sport**: Focus conversions, réservations, visites
- **Hôtellerie/Restauration**: Focus réservations, menu, appels

### 3. **Composants UI Réutilisables** (`src/ui/components.py`)
```python
from src.ui import create_card, create_metric_card

create_metric_card("Engagement", "12.5%", delta="+2.3%")
create_card("Titre", "Contenu", icon="📊")
```

---

## 🚀 Comment Utiliser

### Option A: Nouvelle architecture (recommandé)
```bash
streamlit run streamlit_app_new.py --server.port=8503
```

### Option B: Ancienne architecture (compatible)
```bash
streamlit run streamlit_app.py --server.port=8503
```

---

## 📂 Où Trouver Quoi

| Fonctionnalité | Dossier | Fichiers Clés |
|----------------|---------|---------------|
| **Login/Signup** | `src/auth/` | `login_page.py`, `signup_page.py` |
| **OAuth Réseaux** | `src/social/` | `oauth.py`, `linking_page.py` |
| **Analyse KPI** | `src/analysis/` | `kpi_fetcher.py`, `gpt_analyzer.py` |
| **Sélection KPI par secteur** | `src/profile/` | `kpi_selector.py` ⭐ |
| **Prompts GPT par secteur** | `src/config/` | `settings.py` ⭐ |
| **Génération PPT** | `src/analysis/` | `powerpoint_generator.py` |
| **Envoi Email** | `src/analysis/` | `email_sender.py` |
| **Composants UI** | `src/ui/` | `components.py`, `styles.py` |

---

## 📋 Status

- ✅ **Structure créée** (8 dossiers, 30+ fichiers)
- ✅ **Modules initialisés** (`__init__.py`)
- ✅ **Redirections actives** (compatibilité totale)
- ✅ **KPI par secteur** implémenté
- ✅ **Prompts GPT** personnalisés
- ✅ **Composants UI** créés
- ⏳ **Migration progressive** (en cours)

---

Voir [NOUVELLE_ARCHITECTURE_COMPLETE.md](NOUVELLE_ARCHITECTURE_COMPLETE.md) pour les détails complets.
