# ✅ CHECKLIST - Mise en place de la liaison Instagram/Facebook

## 🎯 Étape 0 : Prérequis
- [ ] Python 3.8+ installé
- [ ] L'application fonctionne (étape 1 terminée)
- [ ] Vous avez un compte Facebook personnel
- [ ] Vous avez accès à une page Facebook OU un compte Instagram Business

---

## 🔐 Étape 1 : Créer votre application Meta (Facebook)

### 1.1 Inscription développeur
- [ ] Aller sur https://developers.facebook.com
- [ ] Créer un compte développeur si vous n'en avez pas
- [ ] Vérifier votre email

### 1.2 Créer une application
- [ ] Cliquer sur "Mes applications"
- [ ] Cliquer sur "Créer une application"
- [ ] Type d'app: **Consumer**
- [ ] Nom: Ex "MG Social Media Dashboard"
- [ ] Catégorie: "Business"
- [ ] Créer l'application

### 1.3 Obtenir les clés
- [ ] Aller dans Paramètres > Informations de base
- [ ] Copier **App ID** (vous en aurez besoin)
- [ ] Cliquer sur "Afficher" pour voir **App Secret**
- [ ] Copier **App Secret** (⚠️ gardez-le secret!)

**Sauvegardez ces deux valeurs dans un endroit sûr!**

---

## 🔧 Étape 2 : Configurer les produits dans Meta App

### 2.1 Ajouter Facebook Login
- [ ] Depuis le tableau de bord, cliquer "Ajouter des produits"
- [ ] Chercher "Facebook Login"
- [ ] Cliquer sur "Ajouter"
- [ ] Aller dans Facebook Login > Paramètres
- [ ] Noter les URI autorisés requis

### 2.2 Ajouter Instagram Graph API (optionnel mais recommandé)
- [ ] Cliquer "Ajouter des produits"
- [ ] Chercher "Instagram Graph API"
- [ ] Cliquer sur "Ajouter"

---

## 📍 Étape 3 : Configurer les URI de redirection OAuth

### 3.1 En mode développement (local)
- [ ] Aller dans Facebook Login > Paramètres
- [ ] Ajouter à "URI de redirection OAuth autorisés": `http://localhost:8501/`
- [ ] Sauvegarder

### 3.2 Pour production (plus tard)
- [ ] Remplacer par votre URL réelle: `https://votredomaine.com/`
- [ ] Ajouter à Paramètres > Informations de base > Domaines autorisés

---

## 👤 Étape 4 : Configurer les testeurs (mode développement)

- [ ] Aller dans Rôles > Testeurs
- [ ] Ajouter votre compte Facebook comme testeur
- [ ] Accepter l'invitation (vous la recevrez dans vos notifications Facebook)
- [ ] Attendre 24h maximum pour que le statut de testeur soit actif

---

## ⚙️ Étape 5 : Mettre à jour le fichier `.env`

```bash
# Copier le App ID et App Secret obtenus
FACEBOOK_APP_ID=votre_app_id
FACEBOOK_APP_SECRET=votre_app_secret

# La redirection pour votre environnement
OAUTH_REDIRECT_URI=http://localhost:8501/
```

- [ ] Éditez le fichier `.env` à la racine du projet
- [ ] Remplacez les valeurs d'exemple par vos vraies clés
- [ ] Sauvegardez

**Format complet à avoir dans .env:**
```env
# === Existants ===
PEPPER_SECRET=6f2ca2683ebec33251cb066842e4ace3759e
GMAIL_ADDRESS=hinaultpro@gmail.com
GMAIL_PASSWORD=sagxvryyxubhejcb
GOOGLE_SHEETS_ID=1Txmci-udBMYPc3zthf9JcDvFehKV5wURDVv2vDx5W2U
GOOGLE_APPLICATION_CREDENTIALS=credentials.json

# === Nouveaux ===
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
OAUTH_REDIRECT_URI=http://localhost:8501/
INSTAGRAM_BUSINESS_ACCOUNT_ID=
```

---

## 📦 Étape 6 : Vérifier les dépendances

```bash
# Vérifier que requests est installé
pip list | grep requests

# Si absent, installer
pip install requests>=2.31.0

# Ou réinstaller depuis requirements.txt
pip install -r requirements.txt
```

- [ ] Commande: `pip list | grep requests`
- [ ] Résultat: `requests (2.31.0 ou plus recent)`
- [ ] ✅ Si c'est ok, continuer

---

## 🚀 Étape 7 : Tester l'application

### 7.1 Lancer l'app
```bash
streamlit run streamlit_app.py
```

- [ ] L'application démarre sans erreur
- [ ] URL locale: `http://localhost:8501`

### 7.2 Créer un compte et se connecter
- [ ] Inscription avec email
- [ ] Confirmation d'email
- [ ] Connexion
- [ ] Accès au dashboard

### 7.3 Tester la liaison Instagram
- [ ] Cliquer sur "🔗 Mes comptes"
- [ ] Cliquer sur "Connecter Instagram"
- [ ] Vous êtes redirigé vers Facebook
- [ ] Connectez-vous avec votre compte Facebook
- [ ] Acceptez les permissions
- [ ] Redirigé vers l'app avec vos comptes disponibles
- [ ] Sélectionner votre compte Instagram Business
- [ ] Message "✅ Compte Instagram lié"

### 7.4 Tester la liaison Facebook Pages
- [ ] Cliquer sur "Ajouter un compte"
- [ ] Cliquer sur "Connecter Facebook"
- [ ] Accepter les permissions
- [ ] Sélectionner vos pages
- [ ] Message "✅ Page Facebook liée"

### 7.5 Vérifier le dashboard
- [ ] Retour au "📊 Dashboard"
- [ ] Voir vos comptes liés avec les statistiques
- [ ] Followers count, nombre de posts, etc.

---

## 🐛 Dépannage

### Erreur : "FACEBOOK_APP_ID not configured"
- [ ] Vérifier que `.env` contient `FACEBOOK_APP_ID=votre_id`
- [ ] Vérifier qu'il n'y a pas d'espaces autour du `=`
- [ ] Redémarrer l'application

### Erreur : "OAuth URI not authorized"
- [ ] Vérifier dans Meta App > Facebook Login > Paramètres
- [ ] Ajouter exactement: `http://localhost:8501/`
- [ ] Sauvegarder

### Erreur : "Instagram account not found"
- [ ] Convertir votre compte en compte Business (Instagram > Paramètres > Passer à un compte professionnel)
- [ ] Choisir "Entreprise"
- [ ] Lier Facebook et Instagram dans Meta Business Suite

### Erreur : "Vous êtes pas testeur"
- [ ] Aller dans Meta App > Rôles > Testeurs
- [ ] Vérifier que votre compte Facebook est listés comme testeur
- [ ] Accepter l'invitation (notification Facebook)
- [ ] Attendre 24h

### Impossible de continuer après connexion Facebook
- [ ] Vérifier les logs Streamlit (terminal)
- [ ] Vérifier que l'App Secret est correct
- [ ] Tester avec Graph API Explorer: https://developers.facebook.com/tools/explorer/
- [ ] Vérifier que les permissions sont acceptées

---

## 📋 Fichiers modifiés/créés

Les fichiers suivants ont été ajoutés/modifiés:

- ✅ **social_auth.py** (NOUVEAU) - Logique d'authentification OAuth
- ✅ **pages/page_social_linking.py** (NOUVEAU) - Interface de liaison
- ✅ **pages.py** - Mise à jour du routage (ajout menu navigation)
- ✅ **.env** - Variables Facebook/Instagram
- ✅ **examples_social_auth.py** (NOUVEAU) - Exemples d'utilisation
- ✅ **SOCIAL_AUTH_SETUP.md** (NOUVEAU) - Documentation détaillée
- ✅ **CHECKLIST_SOCIAL_AUTH.md** (CE FICHIER)

---

## 🎯 Qu'est-ce qui se passe maintenant?

Après avoir complété cette checklist:

1. **L'utilisateur peut se connecter à son compte Instagram Business**
2. **L'utilisateur peut lier ses pages Facebook**
3. **Les données sont stockées dans la base de données**
4. **Le dashboard affiche les statistiques (followers, posts, etc.)**

---

## 📈 Prochaines étapes (non incluses dans ce setup)

- [ ] Afficher les graphiques d'analytiques en temps réel
- [ ] Créer des rapports personnalisés par secteur
- [ ] Mettre en cache les données pour moins d'appels API
- [ ] Intégrer TikTok (nécessite TikTok Graph API)
- [ ] Notifications en temps réel des mentions
- [ ] Export des rapports en PDF

---

## 📞 Support

Si vous bloquez quelque part:

1. **Lire la documentation Meta**: https://developers.facebook.com/docs
2. **Consulter SOCIAL_AUTH_SETUP.md** pour plus de détails
3. **Vérifier les logs de l'application** (terminal)
4. **Utiliser le Graph API Explorer** pour tester les requêtes: https://developers.facebook.com/tools/explorer/

---

## ✨ Bravo!

Une fois cette checklist complétée, votre application aura:
- ✅ Authentification utilisateur sécurisée
- ✅ Liaison des comptes Instagram Business
- ✅ Liaison des pages Facebook
- ✅ Dashboard affichant les statistiques
- ✅ Gestion des comptes liés

Vous êtes prêt pour la prochaine étape! 🚀
