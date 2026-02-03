# 🎯 INSTRUCTIONS EXACTES - Étape 2

## Ce que j'ai créé ✅
Votre application peut maintenant permettre aux utilisateurs de lier leurs comptes Instagram et Facebook. Le code est 100% prêt.

## Ce que vous devez faire

### 1️⃣ Créer une application Meta (5 minutes)

**Allez sur:** https://developers.facebook.com

**Étapes:**
1. En haut à droite → Cliquez "Mes applications"
2. Cliquez le bouton "Créer une application"
3. Une popup apparaît:
   - Type: Sélectionnez **"Consumer"**
   - Nom: Tapez **"MG Social Media Dashboard"**
   - Email: Votre email
   - Catégorie: Choisissez **"Business"**
4. Cliquez "Créer l'application"
5. Confirmez votre identité si demandé

---

### 2️⃣ Obtenir vos clés d'accès (1 minute)

1. Vous êtes maintenant sur le tableau de bord de votre app
2. En haut à gauche, sélectionnez votre app s'il y a plusieurs
3. Cliquez sur "Paramètres" (en bas à gauche)
4. Cliquez sur "Informations de base"
5. Vous voyez deux valeurs importantes:
   - **App ID** (environ 16 chiffres) → Exemple: `123456789012345`
   - **App Secret** (long texte) → Cliquez "Afficher" pour voir
6. **Copiez ces deux valeurs** et gardez-les devant vous

⚠️ **IMPORTANT:** Le App Secret est comme un mot de passe. Ne le partagez JAMAIS!

---

### 3️⃣ Configurer la redirection OAuth (2 minutes)

Toujours dans Meta App Dashboard:

1. À gauche, cherchez et cliquez sur **"Facebook Login"**
2. Si ce n'est pas encore ajouté, cliquez "Ajouter"
3. Cliquez sur "Paramètres" (sous Facebook Login)
4. Cherchez la section **"URI de redirection OAuth autorisés"**
5. Dans le champ de texte, tapez: `http://localhost:8501/`
6. Cliquez le bouton "Enregistrer les modifications"
7. Attendez la confirmation

---

### 4️⃣ Remplir le fichier .env (1 minute)

Ouvrez le fichier `.env` à la racine du projet (même dossier que `streamlit_app.py`):

**Cherchez ces lignes:**
```env
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
OAUTH_REDIRECT_URI=http://localhost:8501/
```

**Remplacez les valeurs vides:**
- `FACEBOOK_APP_ID=` → Collez votre App ID
- `FACEBOOK_APP_SECRET=` → Collez votre App Secret
- `OAUTH_REDIRECT_URI=` → Gardez `http://localhost:8501/` (c'est bon)

**Exemple complet:**
```env
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
OAUTH_REDIRECT_URI=http://localhost:8501/
```

**Sauvegardez le fichier!** (Ctrl+S)

---

### 5️⃣ Lancer l'application (30 secondes)

Ouvrez un terminal dans le dossier du projet et tapez:
```bash
streamlit run streamlit_app.py
```

L'application démarre sur `http://localhost:8501` → Elle s'ouvre automatiquement

---

### 6️⃣ Tester la liaison (5 minutes)

**Étape 1 - Inscription:**
1. Cliquez "📝 Inscription"
2. Remplissez les champs:
   - Email: Votre email
   - Mot de passe: Quelque chose de fort
   - Autres champs: Remplissez-les
3. Cliquez "S'inscrire"

**Étape 2 - Confirmation d'email:**
1. Un code vous est envoyé par email
2. Entrez le code dans l'app
3. Cliquez "Confirmer"

**Étape 3 - Connexion:**
1. Cliquez "🔑 Connexion"
2. Entrez votre email et mot de passe
3. Cliquez "Se connecter"

**Étape 4 - Tester la liaison:**
1. Vous voyez le Dashboard (vide)
2. En haut du menu, cliquez **"🔗 Mes comptes"**
3. Vous voyez "Aucun compte social lié"
4. Cliquez sur l'onglet **"Instagram"** ou **"Facebook"**
5. Cliquez le bouton **"🔐 Se connecter avec Instagram"** (ou Facebook)
6. Vous êtes redirigé vers Facebook.com pour vous connecter
7. Entrez vos identifiants Facebook
8. Acceptez les permissions (un bouton "Continuer")
9. Vous êtes redirigé vers l'app
10. Votre compte apparaît à l'écran
11. Cliquez "Lier" à côté de votre compte
12. Message: **"✅ Compte Instagram lié avec succès!"**
13. Allez dans "📊 Dashboard"
14. Vous voyez vos statistiques Instagram! 🎉

---

## 🎉 C'est tout!

Vous avez maintenant une application complète de liaison des comptes sociaux!

### ✅ Vérification rapide

- [ ] App Meta créée
- [ ] App ID + App Secret copiés
- [ ] URL de redirection configurée dans Meta App
- [ ] .env rempli avec les clés
- [ ] Application lancée sans erreur
- [ ] Utilisateur créé et connecté
- [ ] Compte Instagram/Facebook lié
- [ ] Dashboard affiche les stats

Si tout est coché → **Vous êtes prêt!** 🚀

---

## 📚 Besoin d'aide?

**Si l'app ne démarre pas:**
- Vérifier que streamlit est installé: `pip install streamlit`
- Vérifier le terminal pour les erreurs
- Vérifier que le .env est bien rempli (pas d'espaces)

**Si la connexion Facebook échoue:**
- Vérifier que le App ID et App Secret sont corrects
- Vérifier que `http://localhost:8501/` est bien dans Meta App Settings
- Vérifier que vous êtes connecté à Facebook avec un vrai compte

**Si vous êtes bloqué:**
- Lire le fichier `SOCIAL_AUTH_SETUP.md` (section Dépannage)
- Lire le fichier `CHECKLIST_SOCIAL_AUTH.md`

---

## 🚀 Prochaines étapes (optionnel)

Une fois que c'est stable, vous pouvez ajouter:
- Graphiques temps réel
- Rapports PDF
- Alertes
- TikTok
- Et bien d'autres...

Pour maintenant, vous avez une **application de production** complète! ✅

---

**Questions?** → Consultez les fichiers de documentation fournis.
**Prêt?** → Lancer l'app et tester! 🎉
