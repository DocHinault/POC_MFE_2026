# 🎨 Flux visuel de l'application - ÉTAPE 2

## 🗺️ Navigation après connexion

```
┌─────────────────────────────────────────────────────────────┐
│                    Page P1 - Dashboard Principal             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [MG]    [📊 Dashboard] [🔗 Mes comptes] [⚙️ Paramètres]   [👤 User] [🚪 Déconnexion]
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Dashboard (par défaut)                                   │
│  ├─ Comptes liés: 2                                          │
│  ├─ Pages gérées: 3                                          │
│  ├─ Followers: 50,000                                        │
│  │                                                            │
│  ├─ 📸 Instagram (@myhandle)                                 │
│  │  ├─ 10,500 followers                                      │
│  │  └─ 145 posts                                             │
│  │                                                            │
│  └─ 📄 Pages Facebook                                        │
│     ├─ Ma Page 1 (5,200 fans)                                │
│     └─ Ma Page 2 (2,100 fans)                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
         │              │                    │
         ▼              ▼                    ▼
    [DASHBOARD]   [MES COMPTES]       [PARAMÈTRES]
```

---

## 🔗 Interface "Mes comptes"

### Quand aucun compte n'est lié:
```
┌─────────────────────────────────────────────────────────────┐
│  🔗 Lier vos comptes sociaux                                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Vos comptes liés:                                        │
│  ℹ️ Aucun compte social lié pour le moment                  │
│                                                               │
│  ➕ Ajouter un compte                                        │
│  ├─ 📸 Instagram  │  📄 Facebook                             │
│  │                                                            │
│  │  ### Connecter Instagram                                 │
│  │                                                            │
│  │  [🔐 Se connecter avec Instagram ────────────────]       │
│  │                                                            │
│  │  Après connexion:                                        │
│  │  1. Acceptez les permissions                             │
│  │  2. Sélectionnez votre compte                            │
│  │  3. Compte sera importé automatiquement                  │
│                                                               │
│  └─ Ou │                                                     │
│       [🔐 Se connecter avec Facebook ────────────────]       │
│                                                               │
│        ### Connecter Facebook                               │
│        Connectez vos pages Facebook                         │
│        Vous pouvez en ajouter plusieurs                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Quand des comptes sont liés:
```
┌─────────────────────────────────────────────────────────────┐
│  🔗 Lier vos comptes sociaux                                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Vos comptes liés:                                        │
│  ┌──────────────────┬──────────────────┐                    │
│  │ ✅ Instagram lié │ ✅ Facebook lié  │                    │
│  ├──────────────────┼──────────────────┤                    │
│  │ 👤 @myhandle     │ 👤 John Doe      │                    │
│  │ 📱 10,500 Foll.  │ 📧 john@...      │                    │
│  │ 📸 145 Posts     │ [🔌 Délier]      │                    │
│  │                  │                  │                    │
│  │ [🔌 Délier]      │                  │                    │
│  └──────────────────┴──────────────────┘                    │
│                                                               │
│  📄 Vos pages Facebook                                       │
│  ┌────────────────────────────────────┐                     │
│  │ 📄 Ma Page Business                │                     │
│  │ 👥 5,200 fans                      │ [🗑️]               │
│  └────────────────────────────────────┘                     │
│  ┌────────────────────────────────────┐                     │
│  │ 📄 Ma Page 2                       │                     │
│  │ 👥 2,100 fans                      │ [🗑️]               │
│  └────────────────────────────────────┘                     │
│                                                               │
│  ➕ Ajouter un compte                                        │
│  ... (tabs Instagram/Facebook)                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Flux de connexion OAuth

### 1. Utilisateur clique sur le bouton
```
┌─────────────────────────────────────────────┐
│  [🔐 Se connecter avec Instagram]           │
└─────────────────────────────────────────────┘
                     │
                     ▼
         Code génère l'URL OAuth
         (avec APP_ID, permissions, etc.)
```

### 2. Utilisateur est redirigé
```
                     │
                     ▼
        ┌────────────────────────┐
        │  Facebook Login Page    │
        │  (facebook.com)         │
        │                        │
        │  Email: _______        │
        │  Password: _______     │
        │                        │
        │  [Se connecter]        │
        └────────────────────────┘
```

### 3. Permissions à accepter
```
                     │
                     ▼
        ┌────────────────────────────┐
        │  Autorisations demandées    │
        │                            │
        │  MG Social Dashboard        │
        │  souhaite accéder à:       │
        │  ✓ Compte Instagram        │
        │  ✓ Pages Facebook          │
        │  ✓ Données publiques       │
        │                            │
        │  [Continuer] [Annuler]    │
        └────────────────────────────┘
```

### 4. Redirection vers l'app avec code
```
                     │
                     ▼
     http://localhost:8501/?code=ABC123DEF456...
                     │
                     ▼
        L'app échange le code contre un TOKEN
        (secret, utilisé par le backend)
                     │
                     ▼
        L'app récupère les données:
        - Comptes Instagram disponibles
        - Pages Facebook disponibles
```

### 5. Sélection des comptes à lier
```
        ┌────────────────────────────────────┐
        │  🔗 Sélectionnez les comptes      │
        │                                   │
        │  ### Instagram Business          │
        │                                   │
        │  👤 @myhandle              [Lier] │
        │  📱 10,500 followers              │
        │                                   │
        │  ### Pages Facebook              │
        │                                   │
        │  📄 Ma Page                 [Lier] │
        │  👥 5,200 fans                     │
        │                                   │
        │  📄 Ma Page 2               [Lier] │
        │  👥 2,100 fans                     │
        │                                   │
        │  [❌ Annuler]                      │
        └────────────────────────────────────┘
                     │
         (Utilisateur clique [Lier])
                     │
                     ▼
        Données sauvegardées dans la BDD
        Token d'accès stocké de manière sécurisée
                     │
                     ▼
        ┌────────────────────────────────────┐
        │  ✅ Compte Instagram lié!         │
        │                                   │
        │  Redirection vers Dashboard      │
        │  en 3 secondes...                 │
        └────────────────────────────────────┘
```

---

## 💾 Structure des données sauvegardées

```
User {
  id: "user_123",
  email: "user@example.com",
  nom_entreprise: "Ma Boîte",
  secteur: "Influenceur",
  
  linked_accounts: {
    
    instagram: {
      id: "123456789",
      username: "myhandle",
      name: "My Display Name",
      followers_count: 10500,
      media_count: 145,
      access_token: "IGQVJf...",  // Secret!
      linked_at: "2026-02-02 10:30:00"
    },
    
    facebook: {
      id: "987654321",
      name: "John Doe",
      email: "john@example.com",
      access_token: "EAABsZC...",  // Secret!
      linked_at: "2026-02-02 10:25:00"
    },
    
    facebook_pages: [
      {
        id: "111222333",
        name: "Ma Page Business",
        fan_count: 5200,
        followers_count: 3100,
        access_token: "EAABsZC...",  // Secret!
        linked_at: "2026-02-02 10:20:00"
      },
      {
        id: "444555666",
        name: "Ma Page 2",
        fan_count: 2100,
        followers_count: 1500,
        access_token: "EAABsZC...",
        linked_at: "2026-02-02 10:15:00"
      }
    ]
  }
}
```

---

## 📊 Dashboard après liaison

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Dashboard                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┬──────────────┬──────────────┐           │
│  │ Comptes liés: 2 │ Pages: 2     │ Followers:   │           │
│  │               │           │  17,800       │           │
│  └─────────────────┴──────────────┴──────────────┘           │
│                                                               │
│  📸 Instagram                                               │
│  ├─ Compte: @myhandle                                       │
│  ├─ Followers: 10,500                                       │
│  └─ Posts: 145                                              │
│                                                               │
│  ─────────────────────────────────────────────────────────  │
│                                                               │
│  📄 Pages Facebook                                          │
│  ├─ Page 1: Ma Page Business                                │
│  │  ├─ Fans: 5,200                                          │
│  │  └─ Followers: 3,100                                     │
│  │                                                            │
│  ├─ Page 2: Ma Page 2                                       │
│  │  ├─ Fans: 2,100                                          │
│  │  └─ Followers: 1,500                                     │
│  │                                                            │
│  └─ ℹ️ Contenu du dashboard à venir: analytiques en        │
│     temps réel, graphiques, rapports...                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Cycle complet de l'utilisateur

```
START
  │
  ├─ 1️⃣ Inscription
  │    └─ Email + Mot de passe
  │       │
  ├─ 2️⃣ Confirmation email (optionnel)
  │    └─ Code 6 chiffres
  │       │
  ├─ 3️⃣ Connexion
  │    └─ Email + Mot de passe
  │       │
  ├─ 4️⃣ Dashboard (vide)
  │    └─ "Aucun compte lié"
  │       │
  ├─ 5️⃣ Cliquer "🔗 Mes comptes"
  │    └─ Redirection vers page de liaison
  │       │
  ├─ 6️⃣ Cliquer "Connecter Instagram"
  │    ├─ Redirection vers Facebook login
  │    ├─ Connexion + permissions
  │    ├─ Sélection du compte
  │    └─ Sauvegarde des données
  │       │
  ├─ 7️⃣ Dashboard mis à jour
  │    ├─ Affiche stats Instagram
  │    └─ "✅ Instagram lié"
  │       │
  ├─ 8️⃣ (Optionnel) Connecter Facebook Pages
  │    └─ Même processus pour chaque page
  │       │
  ├─ 9️⃣ Cliquer "Déconnexion"
  │    └─ Session fermée
  │       │
  ✅ END
```

---

## 🔐 Sécurité du flux

```
Utilisateur
    │
    ├─ Clique [Connecter]
    │
    ├─ Redirigé vers FACEBOOK (HTTPS sécurisé)
    │   (L'app NE voit jamais le mot de passe)
    │
    ├─ Facebook envoie un CODE
    │   (éphémère, expire en 5 min)
    │
    ├─ Notre app échange CODE → TOKEN
    │   (uniquement avec APP_SECRET)
    │
    ├─ TOKEN stocké dans la BDD
    │   (jamais exposé à l'utilisateur)
    │
    ├─ TOKEN utilisé pour appels API
    │   (backend seulement, pas frontend)
    │
    └─ Utilisateur voit juste les données affichées
       (pas d'accès direct aux tokens)
```

---

## 📈 Évolution possible

### Phase 2 (Maintenant) ✅
- [x] Liaison Instagram
- [x] Liaison Facebook Pages
- [x] Dashboard basique

### Phase 3 (À venir)
- [ ] Graphiques temps réel
- [ ] Historique des followers
- [ ] Notifications d'événements
- [ ] Rapports PDF/Excel
- [ ] Intégration TikTok

### Phase 4 (Plus tard)
- [ ] IA pour recommandations
- [ ] Planification de posts
- [ ] Analyse du sentiment
- [ ] Collaboration d'équipe

---

**Fin du guide visuel!** 🎨

Vous avez maintenant une compréhension complète du flux.
Prêt à configurer l'app Meta? 👉 Voir `SOCIAL_AUTH_SETUP.md`
