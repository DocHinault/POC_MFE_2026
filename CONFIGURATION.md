# Configuration des Intégrations API

## Google Sheets

### Étapes de configuration

1. **Créer un projet Google Cloud**
   - Aller sur [Google Cloud Console](https://console.cloud.google.com/)
   - Créer un nouveau projet

2. **Activer l'API Google Sheets**
   - Dans le projet, aller à "APIs et services"
   - Cliquer sur "Activer des APIs et des services"
   - Chercher "Google Sheets API"
   - Cliquer sur "Activer"

3. **Créer une clé de service**
   - Aller à "Identifiants" dans le menu de gauche
   - Cliquer sur "Créer des identifiants" > "Compte de service"
   - Remplir les informations requises
   - Cliquer sur "Créer et continuer"

4. **Créer une clé JSON**
   - Dans la page du compte de service, aller à l'onglet "Clés"
   - Cliquer sur "Ajouter une clé" > "Créer une clé"
   - Choisir "JSON"
   - Télécharger le fichier JSON
   - Placer le fichier dans le répertoire du projet et le nommer `credentials.json`

5. **Créer un Google Sheet**
   - Aller sur [Google Sheets](https://sheets.google.com/)
   - Créer une nouvelle feuille de calcul
   - Copier l'ID du Sheet (visible dans l'URL)
   - L'ajouter à la variable `GOOGLE_SHEETS_ID` dans `.env`

6. **Partager le Sheet avec le compte de service**
   - Obtenir l'email du compte de service depuis le fichier JSON
   - Partager le Sheet avec cet email

## Facebook API

### Étapes de configuration

1. **Créer une application Facebook**
   - Aller sur [Facebook Developers](https://developers.facebook.com/)
   - Créer une nouvelle application
   - Choisir "Type d'application" > "Commerce"

2. **Obtenir les identifiants**
   - Aller à "Paramètres" > "Général"
   - Copier l'ID de l'application (App ID)
   - Copier la clé secrète de l'application (App Secret)
   - Les ajouter à `.env`

3. **Configurer les URLs de redirection**
   - Aller à "Paramètres" > "Utilisation de l'authentification Facebook"
   - Ajouter les URLs de redirection valides
   - Exemple: `http://localhost:8501/callback`

## Instagram Business API

### Étapes de configuration

1. **Convertir un compte Instagram en compte professionnel**
   - Si pas encore fait, convertir le compte Instagram en compte professionnel

2. **Obtenir un access token**
   - Aller à [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   - Sélectionner votre application Facebook
   - Générer un access token avec les permissions:
     - `instagram_business_content_publishing`
     - `instagram_business_manage_messages`
     - `pages_read_engagement`

3. **Obtenir l'ID du compte Business**
   - Utiliser Graph API Explorer pour faire une requête:
     - Query: `GET /me/instagram_business_accounts`
     - Copier l'ID retourné
   - L'ajouter à `INSTAGRAM_BUSINESS_ACCOUNT_ID` dans `.env`

## Configuration Email (Gmail)

### Avec un compte Gmail personnel

1. **Activer l'authentification à deux facteurs**
   - Aller à [Google Account Security](https://myaccount.google.com/security)
   - Activer la vérification en deux étapes

2. **Générer un mot de passe d'application**
   - Une fois l'authentification à deux facteurs activée
   - Aller à [App passwords](https://myaccount.google.com/apppasswords)
   - Sélectionner "Mail" et "Windows Computer"
   - Google génère un mot de passe de 16 caractères
   - Copier ce mot de passe dans `.env` comme `SENDER_PASSWORD`

3. **Configuration dans `.env`**
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=votre-email@gmail.com
   SENDER_PASSWORD=votre-mot-de-passe-app-16-caracteres
   ```

## Variables d'environnement complètes

Créez un fichier `.env` à la racine du projet avec :

```env
# Google Sheets
GOOGLE_SHEETS_ID=VOTRE_ID_SHEETS_ICI
GOOGLE_CREDENTIALS_PATH=credentials.json

# Facebook
FACEBOOK_APP_ID=VOTRE_APP_ID_ICI
FACEBOOK_APP_SECRET=VOTRE_APP_SECRET_ICI

# Instagram
INSTAGRAM_BUSINESS_ACCOUNT_ID=VOTRE_ACCOUNT_ID_ICI

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=votre-email@gmail.com
SENDER_PASSWORD=votre-mot-de-passe-app-16-caracteres
```

## Dépannage

### "Erreur lors de la connexion à Google Sheets"
- Vérifier que le fichier `credentials.json` existe
- Vérifier que le fichier a les bonnes permissions
- Vérifier que la clé de service est active dans Google Cloud

### "Authentification Facebook échouée"
- Vérifier que l'URL de redirection est correcte
- Vérifier que l'App ID et App Secret sont corrects
- S'assurer que l'application est en mode développement ou production

### "Email non envoyé"
- Vérifier les identifiants Gmail
- Si utilisation d'un mot de passe d'application, vérifier qu'il est correct
- S'assurer que "Accès des applis moins sécurisées" est activé (si pas d'auth à deux facteurs)

## Tests

Après la configuration, vous pouvez tester les connexions :

```bash
python test_config.py
```

Cela vérifiera :
- ✅ L'importation de toutes les dépendances
- ✅ La présence des fichiers de configuration
- ✅ La validité basique des configurations

Pour tester les API :
```bash
python -c "from google_sheets import get_google_sheets_client; print(get_google_sheets_client())"
```
