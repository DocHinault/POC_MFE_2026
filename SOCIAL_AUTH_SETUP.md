# 📱 Guide complet : Liaison des comptes Instagram et Facebook

## Vue d'ensemble

Ce guide explique comment configurer et utiliser la fonctionnalité de liaison des comptes Instagram Business et Facebook Pages à votre application.

---

## ✅ ÉTAPE 1 : Créer une application Meta (Facebook)

### 1.1 Créer un compte développeur Meta
1. Allez sur https://developers.facebook.com/
2. Cliquez sur "Mes applications" en haut à droite
3. Cliquez sur "Créer une application"

### 1.2 Créer l'application
1. Choisissez "Consumer" comme type d'app
2. Donnez un nom à votre app (ex: "MG Social Media Dashboard")
3. Remplissez les informations de contact si demandé
4. Cliquez sur "Créer une application"

### 1.3 Configurer les produits
1. Sur le tableau de bord de l'app, cliquez sur "Ajouter des produits"
2. Cherchez "Facebook Login" et cliquez sur "Configurer"
3. Cherchez "Instagram Graph API" et cliquez sur "Configurer"

---

## ✅ ÉTAPE 2 : Configurer Facebook Login (OAuth)

### 2.1 Obtenir l'App ID et App Secret
1. Allez dans "Paramètres" > "Informations de base"
2. Copiez votre **App ID** et gardez-le précieusement
3. Cliquez sur "Afficher" à côté de "App Secret" et copiez-le
4. ⚠️ **Ne partagez jamais votre App Secret**

### 2.2 Configurer les URI de redirection OAuth
1. Allez dans "Facebook Login" > "Paramètres"
2. Dans "URI de redirection OAuth autorisés", entrez l'URL de votre application:
   - **En développement local:** `http://localhost:8501/`
   - **En production:** `https://votredomaine.com/`
3. Cliquez sur "Enregistrer les modifications"

### 2.3 Configurer les domaines autorisés
1. Allez dans "Paramètres" > "Informations de base"
2. Ajoutez votre domaine dans "Domaines autorisés"

---

## ✅ ÉTAPE 3 : Obtenir des permissions

### 3.1 Configurer les permissions requises
Les permissions demandées par défaut sont:
- `instagram_basic` - Accès basique à Instagram
- `instagram_business_basic` - Données de compte Business
- `pages_read_engagement` - Lecture des engagement Facebook
- `pages_manage_metadata` - Gestion des métadonnées
- `instagram_manage_insights` - Accès aux analytiques Instagram

Vérifiez dans `social_auth.py` ligne ~40 si vous devez ajouter/retirer des permissions.

### 3.2 Ajouter des testeurs
Tant que vous êtes en mode développement:
1. Allez dans "Rôles" > "Testeurs"
2. Ajoutez votre compte Facebook personnel comme testeur
3. Vous recevrez une invitation que vous devez accepter

---

## ✅ ÉTAPE 4 : Configurer le fichier `.env`

Mettez à jour votre fichier `.env` avec les clés obtenues :

```env
# ===== FACEBOOK OAUTH =====
FACEBOOK_APP_ID=votre_app_id_ici
FACEBOOK_APP_SECRET=votre_app_secret_ici

# URL de redirection (doit correspondre à votre configuration Meta)
OAUTH_REDIRECT_URI=http://localhost:8501/

# Optionnel - ID du compte Instagram Business
INSTAGRAM_BUSINESS_ACCOUNT_ID=
```

**Exemple complet :**
```env
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
OAUTH_REDIRECT_URI=http://localhost:8501/
```

---

## ✅ ÉTAPE 5 : Installer les dépendances

Assurez-vous que le package `requests` est installé :

```bash
pip install requests
```

Si ce n'est pas déjà dans `requirements.txt`, ajoutez-le :

```bash
echo "requests>=2.28.0" >> requirements.txt
pip install -r requirements.txt
```

---

## ✅ ÉTAPE 6 : Tester l'application

### 6.1 Lancer l'app
```bash
streamlit run streamlit_app.py
```

### 6.2 Créer un compte et se connecter
1. Inscrivez-vous avec votre email
2. Confirmez votre email (si email configuré)
3. Connectez-vous

### 6.3 Tester la liaison du compte
1. Cliquez sur "🔗 Mes comptes" dans le menu
2. Cliquez sur "Connecter Instagram" ou "Connecter Facebook"
3. Vous serez redirigé vers Facebook pour vous connecter
4. Autorisez l'application
5. Sélectionnez les comptes/pages à lier

---

## 📊 Comprendre le flux OAuth

```
1. Utilisateur clique "Connecter Instagram"
                    ↓
2. Redirigé vers Facebook login
                    ↓
3. Utilisateur se connecte à Facebook
                    ↓
4. Accepte les permissions
                    ↓
5. Redirigé vers http://localhost:8501/?code=XXXX
                    ↓
6. Notre app échange le code contre un token d'accès
                    ↓
7. Récupère les données du compte
                    ↓
8. Affiche le sélecteur de comptes/pages
                    ↓
9. Utilisateur sélectionne les comptes à lier
                    ↓
10. Données sauvegardées dans la base de données
```

---

## 🔍 Structures de données

### Instagram lié
```python
{
    'linked_accounts': {
        'instagram': {
            'id': '123456789',
            'username': 'myusername',
            'name': 'My Display Name',
            'followers_count': 10500,
            'media_count': 145,
            'access_token': 'IGQVJf...',
            'linked_at': '2026-02-02 10:30:00'
        }
    }
}
```

### Pages Facebook liées
```python
{
    'linked_accounts': {
        'facebook': {
            'id': '123456789',
            'name': 'User Name',
            'email': 'user@example.com',
            'access_token': 'EAABsZC...',
            'linked_at': '2026-02-02 10:30:00'
        },
        'facebook_pages': [
            {
                'id': '987654321',
                'name': 'My Business Page',
                'fans_count': 5200,
                'followers_count': 3100,
                'access_token': 'EAABsZC...',
                'linked_at': '2026-02-02 10:30:00'
            }
        ]
    }
}
```

---

## 🛠️ Dépannage

### Erreur : "Configuration manquante: FACEBOOK_APP_ID non configuré"
**Solution:** Vérifiez que `FACEBOOK_APP_ID` et `FACEBOOK_APP_SECRET` sont définis dans `.env`

### Erreur : "Erreur lors de l'échange du token"
**Solutions possibles:**
- Vérifiez que `FACEBOOK_APP_SECRET` est correct
- Vérifiez que l'URL de redirection correspond dans Meta App Settings
- Vérifiez que le code n'a pas expiré (5 minutes)

### Les pages Facebook n'apparaissent pas
**Solutions:**
- Assurez-vous d'être administrateur des pages
- Vérifiez que vous avez accepté les permissions
- Les permissions `pages_read_engagement` et `pages_manage_metadata` sont requises

### Le compte Instagram Business n'apparaît pas
**Solutions:**
- Vous devez avoir un compte **Instagram Business** (pas un compte personnel)
- Convertissez votre compte personnel en compte Business:
  1. Allez dans Paramètres > Compte
  2. Cliquez sur "Passer à un compte professionnel"
  3. Choisissez "Entreprise"
  4. Configurez votre profil
- Vérifiez que Facebook et Instagram sont liés dans Meta Business Suite

### Erreur "token_expired" ou "token_invalid"
**Solution:** Les tokens short-lived expirent en 1 heure. Dans `social_auth.py`, la méthode `refresh_long_lived_token()` convertit les tokens pour qu'ils valident 60 jours. Appelez-la après l'échange.

---

## 📈 Prochaines étapes

### Afficher les analytiques
Une fois les comptes liés, vous pouvez récupérer les données:

```python
from social_auth import SocialMediaAuthenticator

auth = SocialMediaAuthenticator()

# Pour Instagram
insights = auth.get_instagram_insights(
    instagram_id='123456789',
    access_token='IGQVJf...'
)

# Pour Facebook
page_insights = auth.get_page_insights(
    page_id='987654321',
    page_access_token='EAABsZC...',
    metric='page_views'
)
```

### Utiliser le Graph API Explorer
Pour tester les appels API manuellement:
1. Allez sur https://developers.facebook.com/tools/explorer/
2. Sélectionnez votre app
3. Testez les requêtes avant de les intégrer

---

## 📝 Fichiers modifiés/créés

- ✅ `social_auth.py` - Logique d'authentification OAuth
- ✅ `pages/page_social_linking.py` - Interface de liaison
- ✅ `pages.py` - Mise à jour du routage
- ✅ `.env` - Variables de configuration

---

## 🔐 Sécurité

### Recommandations
1. **Ne mettez jamais** votre `FACEBOOK_APP_SECRET` sur GitHub (utilisez `.env` + `.gitignore`)
2. **Stockez les tokens** de manière sécurisée dans votre base de données
3. **Validez les tokens** régulièrement et rafraîchissez-les
4. **HTTPS en production** - Facebook impose HTTPS en production
5. **Rate limiting** - Meta a des limites d'appels (voir la doc API)

### Checklist avant production
- [ ] Domaines configurés correctement dans Meta App Settings
- [ ] URL de redirection en HTTPS
- [ ] App soumise pour révision (si nécessaire selon votre cas)
- [ ] Logs d'erreur en place
- [ ] Token refresh automatique mis en place
- [ ] HTTPS/SSL configuré sur votre serveur

---

## 💡 Questions fréquentes

**Q: Puis-je lier plusieurs comptes Instagram?**
R: Actuellement non, le code sauvegarde un seul compte Instagram. Pour plusieurs, modifiez `social_auth.py` pour utiliser une liste comme pour Facebook Pages.

**Q: Les tokens expirent-ils?**
R: Les short-lived tokens expirent en 1 heure. Les long-lived tokens expirent en 60 jours. Utilisez la méthode `refresh_long_lived_token()`.

**Q: Puis-je avoir accès aux stories Instagram?**
R: Non, l'API Instagram n'expose pas les stories pour les raisons de confidentialité.

**Q: Quelles données puis-je récupérer?**
R: Dépend des permissions accordées. Les principales sont:
- Followers count
- Posts count (media_count)
- Engagement metrics (impressions, reach)
- Page views
- Story views

---

## 📞 Support

Pour des problèmes:
1. Consultez la [Documentation Meta](https://developers.facebook.com/docs)
2. Vérifiez les logs Streamlit pour plus de détails
3. Utilisez le [Graph API Explorer](https://developers.facebook.com/tools/explorer/) pour tester
4. Vérifiez que vos tokens ne sont pas expirés

---

**Besoin d'aide?** Consultez la documentation officielle Meta ou posez une question!
