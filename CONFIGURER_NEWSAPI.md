# 📰 Configurer NewsAPI - Actualités Gratuites

## 🎯 Pourquoi NewsAPI ?

NewsAPI permet d'afficher les dernières actualités dans votre assistant :
- ✅ **100 requêtes/jour GRATUIT**
- ✅ Actualités de 150+ pays
- ✅ 7 catégories (santé, sport, tech, science, business, etc.)
- ✅ Recherche par mots-clés
- ✅ Actualités en temps réel

---

## 📋 Étapes de Configuration (5 minutes)

### Étape 1 : Créer un Compte NewsAPI

1. Allez sur https://newsapi.org/register
2. Remplissez le formulaire :
   - **First Name** : Votre prénom
   - **Email** : Votre email
   - **Password** : Choisissez un mot de passe
3. Cochez "I'm not a robot"
4. Cliquez sur **"Submit"**

### Étape 2 : Vérifier Votre Email

1. Ouvrez votre boîte email
2. Cherchez l'email de NewsAPI
3. Cliquez sur le lien de vérification

### Étape 3 : Obtenir Votre Clé API

1. Une fois connecté, vous verrez votre **API Key** sur la page d'accueil
2. Elle ressemble à : `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`
3. **Copiez cette clé** (cliquez sur l'icône de copie)

### Étape 4 : Ajouter la Clé dans Render

1. Allez sur https://render.com
2. Connectez-vous à votre compte
3. Cliquez sur votre service **medical-ai-assistant-2k1a**
4. Menu de gauche → **Environment**
5. Cliquez sur **"Add Environment Variable"**
6. Remplissez :
   - **Key** : `NEWS_API_KEY`
   - **Value** : Collez votre clé API (ex: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)
7. Cliquez sur **"Save Changes"**
8. Attendez 2-3 minutes (redémarrage automatique)

### Étape 5 : Vérifier l'Activation

1. Allez dans **"Logs"** (menu de gauche)
2. Cherchez cette ligne :
   ```
   ✓ Service actualités activé
   ```
3. Testez sur votre site : "Actualités santé"

---

## 🎉 Exemples d'Utilisation

Une fois configuré, vous pouvez demander :

### Actualités Générales
```
"Quelles sont les dernières actualités ?"
"Actualités du jour"
"Dernières nouvelles"
```

### Actualités par Catégorie
```
"Actualités santé"
"News sport"
"Actualités tech"
"Infos science"
"Actualités business"
```

### Actualités par Pays
```
"Actualités France"
"News USA"
"Actualités UK"
```

### Recherche Spécifique
```
"Actualités sur le climat"
"News sur l'IA"
"Infos sur le COVID"
```

---

## 📊 Limites du Plan Gratuit

| Fonctionnalité | Plan Gratuit |
|----------------|--------------|
| Requêtes/jour | 100 |
| Requêtes/mois | 3000 |
| Pays disponibles | 150+ |
| Catégories | 7 |
| Historique | 1 mois |
| Support | Email |

**💡 Astuce :** 100 requêtes/jour = largement suffisant pour un usage personnel !

---

## 🔍 Catégories Disponibles

1. **Santé** (health) - Actualités médicales et santé
2. **Sport** (sports) - Actualités sportives
3. **Tech** (technology) - Technologie et innovation
4. **Science** (science) - Découvertes scientifiques
5. **Business** (business) - Économie et affaires
6. **Divertissement** (entertainment) - Culture et spectacles
7. **Général** (general) - Actualités générales

---

## 🌍 Pays Disponibles

Quelques exemples :
- 🇫🇷 France (fr)
- 🇺🇸 USA (us)
- 🇬🇧 UK (gb)
- 🇩🇪 Allemagne (de)
- 🇪🇸 Espagne (es)
- 🇮🇹 Italie (it)
- 🇨🇦 Canada (ca)
- Et 140+ autres pays !

---

## ⚙️ Configuration Locale (Développement)

Si vous testez en local, ajoutez la clé dans `.env` :

```env
# NewsAPI (GRATUIT - 100 requêtes/jour)
NEWS_API_KEY=votre_cle_api_ici
```

**⚠️ Important :** Ne committez JAMAIS le fichier `.env` sur GitHub !

---

## 🆘 Problèmes Courants

### Problème 1 : "Service non configuré"
**Cause :** La clé API n'est pas dans Render  
**Solution :** Suivez l'Étape 4 ci-dessus

### Problème 2 : "Aucune actualité trouvée"
**Cause :** Recherche trop spécifique ou pays non supporté  
**Solution :** Essayez une recherche plus générale

### Problème 3 : "API Error 401"
**Cause :** Clé API invalide ou expirée  
**Solution :** Vérifiez que vous avez copié la bonne clé

### Problème 4 : "API Error 429"
**Cause :** Limite de 100 requêtes/jour atteinte  
**Solution :** Attendez demain ou passez au plan payant

### Problème 5 : Email de vérification non reçu
**Cause :** Email dans les spams  
**Solution :** Vérifiez votre dossier spam/courrier indésirable

---

## 💰 Plans Payants (Optionnel)

Si vous avez besoin de plus de requêtes :

| Plan | Prix | Requêtes/mois |
|------|------|---------------|
| Gratuit | 0€ | 3,000 |
| Business | 449€/mois | 250,000 |
| Enterprise | Sur devis | Illimité |

**💡 Pour un usage personnel, le plan gratuit suffit largement !**

---

## 📚 Documentation Officielle

- Site officiel : https://newsapi.org
- Documentation : https://newsapi.org/docs
- Sources disponibles : https://newsapi.org/sources
- Support : support@newsapi.org

---

## ✅ Checklist de Configuration

- [ ] Compte créé sur NewsAPI
- [ ] Email vérifié
- [ ] Clé API copiée
- [ ] Clé ajoutée dans Render (`NEWS_API_KEY`)
- [ ] Service redémarré (2-3 minutes)
- [ ] Logs vérifiés (✓ Service actualités activé)
- [ ] Test effectué ("Actualités santé")

---

## 🎯 Résumé Ultra-Rapide

1. https://newsapi.org/register → Créer compte
2. Vérifier email
3. Copier clé API
4. Render → Environment → Add `NEWS_API_KEY`
5. Save → Attendre 3 minutes → Tester !

**⏱️ Temps total : 5 minutes**

---

**🚀 Une fois configuré, votre assistant pourra afficher les dernières actualités en temps réel !**
