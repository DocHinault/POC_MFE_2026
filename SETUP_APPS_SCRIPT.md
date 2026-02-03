# 🔧 CONFIGURATION - APPS SCRIPT API

## ✅ **ÉTAPES POUR CONFIGURER L'APPLICATION AVEC VOTRE APPS SCRIPT**

### **ÉTAPE 1: Obtenir l'URL du Web App (Apps Script)**

1. **Allez dans votre Apps Script** (https://script.google.com/)
2. Sélectionnez votre projet
3. Cliquez sur **"Déploiement"** en haut à droite
4. Cliquez sur **"Gérer les déploiements"**
5. Créez un nouveau déploiement:
   - Type: **Web app**
   - Exécuter en tant que: **Votre compte**
   - Qui a accès: **N'importe qui**
   - Cliquez sur **"Déployer"**
6. Copiez l'URL générée (format: `https://script.google.com/macros/s/SCRIPT_ID/usw`)

### **ÉTAPE 2: Obtenir/Créer la clé API**

1. Dans votre Apps Script, allez à **"Extensions"** → **"Apps Script API"**
2. Activez le service si besoin
3. Allez à **Propriétés du projet** (engrenage)
4. Notez votre **ID de script**

Pour créer une API_KEY:
- Dans votre Apps Script, allez à l'éditeur
- Ajoutez une fonction de configuration:

```javascript
function setApiKey() {
  var key = Utilities.getUuid(); // Génère une clé aléatoire
  PropertiesService.getScriptProperties().setProperty('API_KEY', key);
  Logger.log('API Key définie: ' + key);
}
```

5. Exécutez cette fonction (cliquez sur le bouton ▶️ "Run")
6. Regardez les logs pour voir la clé générée

### **ÉTAPE 3: Configurer les propriétés du Apps Script**

1. Dans votre Apps Script, cliquez sur **"Propriétés du projet"** (engrenage)
2. Allez à l'onglet **"Propriétés du script"**
3. Ajoutez ces propriétés (pour tests, modifiez si besoin):

| Propriété | Valeur | Description |
|-----------|--------|-------------|
| `API_KEY` | *votre_clé_uuid* | Clé secrète pour authentifier les appels API |
| `PEPPER_SECRET` | *clé_aléatoire_32_chars* | Clé pour salter les mots de passe |
| `META_APP_ID` | *votre_app_id* | ID Facebook/Instagram App |
| `META_APP_SECRET` | *votre_app_secret* | Secret Facebook/Instagram App |
| `PBKDF2_ITERATIONS` | `100000` | Itérations PBKDF2 (optionnel) |
| `WEBAPP_URL` | *url_du_webapp* | URL complète du Apps Script (optionnel) |

**Conseil:** Pour `PEPPER_SECRET`, générez une chaîne aléatoire de 32 caractères

### **ÉTAPE 4: Configurer le fichier `.env` dans le projet Python**

Éditez le fichier `.env` à la racine du projet:

```env
# ===== APPS SCRIPT API =====
APPS_SCRIPT_URL=https://script.google.com/macros/s/YOUR_SCRIPT_ID/usw
API_KEY=votre_clé_api_ici

# ===== FACEBOOK/INSTAGRAM (optionnel pour Phase 2) =====
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
```

**⚠️ IMPORTANT:**
- Remplacez `YOUR_SCRIPT_ID` par votre ID réel
- Ne commitez JAMAIS `.env` sur GitHub!
- Gardez la clé API secrète!

### **ÉTAPE 5: Tester la connexion**

1. Lancez l'application:
```bash
streamlit run streamlit_app.py
```

2. Aller sur la page et tester:
   - **Inscription** avec un email
   - Vous devez recevoir un **code par email**
   - Vérifier le code
   - Être redirigé vers le dashboard

### **ÉTAPE 6: Vérifie Google Sheets**

Allez dans votre Google Sheets "POC REPORTING DB":
- Cliquez sur l'onglet **"CLIENTS"**
- Vous devriez voir votre nouveau client ajouté automatiquement!

Colonnes visibles:
- **ID_CLIENT**: UUID généré
- **EMAIL**: Email d'inscription
- **MDP**: Hash sécurisé du mot de passe
- **ID_FB**: ID Facebook (vide si non lié)
- **ID_INSTA**: ID Instagram (vide si non lié)
- **NOM_ENTREPRISE**: Nom rempli
- **SECTEUR**: Secteur choisi
- **CREE_LE**: Date/heure de création

---

## 🔍 **DÉPANNAGE**

### **Erreur: "APPS_SCRIPT_URL ou API_KEY non configuré"**
→ Vérifiez que le fichier `.env` existe et contient les bonnes valeurs

### **Erreur: "API_ERROR" ou connexion impossible**
→ Vérifiez l'URL du Web App (ne doit pas finir par `/edit`, mais `/usw`)

### **Le code ne s'envoie pas par email**
→ Assurez-vous que l'Apps Script peut envoyer des emails (GmailApp.sendEmail)

### **"EMAIL_EXISTS" à l'inscription**
→ Cet email est déjà dans le Google Sheet. Utilisez un autre email ou supprimez la ligne.

### **"INVALID_CREDENTIALS" à la connexion**
→ Vérifiez que l'email et le mot de passe sont corrects

---

## 🔐 **SÉCURITÉ**

✅ **Ce qui est sécurisé:**
- Mots de passe hashés avec PBKDF2-SHA256
- API Key requise pour chaque appel
- Validation stricte des champs
- Rate limiting (max 10 tentatives en 15 min)
- Codes de confirmation éphémères (15 min)

⚠️ **À améliorer:**
- HTTPS obligatoire en production
- Rotation régulière de la clé API
- Monitoring des tentatives de login échouées
- Audit des accès

---

## 📱 **STRUCTURE DE VOTRE GOOGLE SHEETS**

**Onglet "CLIENTS":**
```
A          B      C      D      E         F              G      H
ID_CLIENT  EMAIL  MDP    ID_FB  ID_INSTA  NOM_ENTREPRISE SECTEUR CREE_LE
uuid       ...    hash$  ...    ...       ...            ...     2026-02-02 18:30:00
```

---

## 🚀 **PROCHAINES ÉTAPES**

Après cette configuration:

1. **Tester l'authentification** ✅
2. **Ajouter OAuth Facebook/Instagram** (Phase 2)
3. **Créer le dashboard** (Phase 3)
4. **Générer des rapports** (Phase 4)

---

## ❓ **QUESTIONS?**

- Consultez le code de votre Apps Script
- Regardez les logs (Apps Script Editor → Exécutions)
- Vérifiez les permissions Google Sheets

Bonne chance! 🎉
