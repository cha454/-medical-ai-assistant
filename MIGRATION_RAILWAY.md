# 🚀 Migration Render → Railway (5 minutes)

## 🎯 POURQUOI RAILWAY ?

| Render (Actuel) | Railway (Nouveau) |
|-----------------|-------------------|
| 512 MB RAM | **8 GB RAM** (16× plus !) |
| Sleep après 15min | **Toujours actif** |
| Lent | **Très rapide** |
| Limites strictes | **$5 gratuit/mois** |

**Résultat : Ton app sera 10× plus rapide et stable !**

---

## ⚡ MIGRATION EN 5 MINUTES

### Étape 1 : Créer un compte (1 minute)

1. Va sur **https://railway.app**
2. Clique sur **Start a New Project**
3. **Login with GitHub**
4. Autorise Railway

### Étape 2 : Déployer (2 minutes)

1. Clique sur **New Project**
2. **Deploy from GitHub repo**
3. Cherche **medical-ai-assistant**
4. Clique dessus
5. Railway va automatiquement :
   - ✅ Détecter Python/Flask
   - ✅ Installer `requirements.txt`
   - ✅ Lancer l'app

### Étape 3 : Variables d'environnement (2 minutes)

1. Clique sur ton projet
2. Onglet **Variables**
3. Copie tes variables depuis Render :

**Va sur Render.com → Environment → Copie ces valeurs :**

```
GROQ_API_KEY = [copie depuis Render]
GOOGLE_API_KEY = [copie depuis Render]
NEWS_API_KEY = [copie depuis Render]
OPENWEATHER_API_KEY = [copie depuis Render]
SENDGRID_API_KEY = [copie depuis Render]
SENDGRID_FROM_EMAIL = [copie depuis Render]
SECRET_KEY = [copie depuis Render]
```

**Ajoute-les une par une dans Railway :**
- Clique **+ New Variable**
- Nom : `GROQ_API_KEY`
- Valeur : [colle la valeur]
- Répète pour chaque variable

### Étape 4 : Obtenir l'URL (30 secondes)

1. Onglet **Settings**
2. Section **Domains**
3. Clique **Generate Domain**
4. Tu auras : `https://medical-ai-assistant-production.up.railway.app`

### Étape 5 : Tester (30 secondes)

1. Clique sur l'URL
2. Teste le chat
3. Vérifie que tout fonctionne

**C'est tout ! Ton app est migrée ! 🎉**

---

## 📋 LISTE DES VARIABLES À COPIER

Voici toutes les variables que tu dois copier de Render vers Railway :

### Variables obligatoires :
- ✅ `GROQ_API_KEY` (ou `GOOGLE_API_KEY`)
- ✅ `SECRET_KEY`

### Variables optionnelles (mais recommandées) :
- ⭐ `GOOGLE_API_KEY` (LLM illimité)
- ⭐ `NEWS_API_KEY` (actualités)
- ⭐ `OPENWEATHER_API_KEY` (météo)
- ⭐ `SENDGRID_API_KEY` (emails)
- ⭐ `SENDGRID_FROM_EMAIL` (expéditeur)

### Variables de backup (si tu les as) :
- `GROQ_API_KEY_BACKUP`
- `GOOGLE_API_KEY_BACKUP`
- `OPENAI_API_KEY_BACKUP`

---

## 🔧 CONFIGURATION AUTOMATIQUE

Railway détecte automatiquement :

### 1. Python/Flask
```
✅ Détecte requirements.txt
✅ Installe toutes les dépendances
✅ Configure Python 3.10+
```

### 2. Port
```
✅ Détecte le port dans app.py
✅ Configure automatiquement $PORT
✅ Expose le service sur HTTPS
```

### 3. Commande de démarrage
```
✅ Détecte gunicorn dans requirements.txt
✅ Lance : gunicorn app:app
✅ Configure workers automatiquement
```

**Tu n'as RIEN à configurer manuellement !**

---

## 📊 VÉRIFIER LE DÉPLOIEMENT

### 1. Onglet Deployments

Tu devrais voir :
```
✅ Building...
✅ Deploying...
✅ Active (vert)
```

Si erreur (rouge), clique dessus pour voir les logs.

### 2. Onglet Logs

Tu devrais voir :
```
✓ LLM Provider initialisé: groq
✓ LLM activé: Groq (Llama 3.1)
✓ Email: SendGrid activé
✓ Service météo OpenWeather activé
✓ Service actualités activé
✓ Base de données initialisée
```

### 3. Tester l'URL

Ouvre l'URL et teste :
- ✅ Page d'accueil s'affiche
- ✅ Chat fonctionne
- ✅ LLM répond
- ✅ Météo fonctionne
- ✅ Actualités fonctionnent

---

## 🎨 OPTIMISATIONS (OPTIONNEL)

### 1. Créer `railway.json`

Pour optimiser les performances :

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Avantages :**
- 4 workers (meilleure performance)
- Timeout 120s (pour requêtes longues)
- Redémarrage automatique si crash

### 2. Créer `Procfile`

Pour contrôler la commande de démarrage :

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

### 3. Optimiser `requirements.txt`

Ajoute des versions spécifiques pour éviter les bugs :

```txt
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
# ... reste inchangé
```

**Note :** Ces optimisations sont optionnelles, Railway fonctionne parfaitement sans !

---

## 🔄 REDÉPLOIEMENT AUTOMATIQUE

Railway redémarre automatiquement à chaque push GitHub !

### Comment ça marche :

1. Tu modifies ton code localement
2. Tu push sur GitHub :
   ```bash
   git add .
   git commit -m "Amélioration"
   git push
   ```
3. Railway détecte le push
4. Redéploie automatiquement (2-3 minutes)
5. Ton app est à jour !

**Pas besoin de toucher à Railway !**

---

## 💰 COÛTS RAILWAY

### Plan gratuit :
- **$5 de crédit/mois** (renouvelé automatiquement)
- **8 GB RAM**
- **8 GB Disk**
- **Pas de limite de temps**

### Usage typique de ton app :
- **RAM :** ~200-500 MB (largement dans les limites)
- **CPU :** Faible (sauf pendant les requêtes LLM)
- **Coût estimé :** $2-3/mois

**Résultat : Tu resteras dans le plan gratuit ! 🎉**

### Si tu dépasses $5/mois :
- Railway te prévient par email
- Tu peux ajouter une carte bancaire
- Coût supplémentaire : ~$0.10-0.50/mois

---

## 🆘 DÉPANNAGE

### Problème : Build échoue

**Solution :**
1. Vérifie que `requirements.txt` est à jour
2. Vérifie les logs de build
3. Assure-toi que Python 3.10+ est compatible

### Problème : App ne démarre pas

**Solution :**
1. Vérifie les variables d'environnement
2. Vérifie que `SECRET_KEY` est défini
3. Vérifie les logs : onglet **Logs**

### Problème : LLM ne répond pas

**Solution :**
1. Vérifie que `GROQ_API_KEY` ou `GOOGLE_API_KEY` est défini
2. Vérifie les logs : `✓ LLM activé: ...`
3. Teste la clé API manuellement

### Problème : 404 Not Found

**Solution :**
1. Vérifie que le domaine est généré
2. Attends 2-3 minutes (propagation DNS)
3. Essaie en navigation privée

---

## 📞 SUPPORT RAILWAY

### Documentation :
- **Docs :** https://docs.railway.app
- **Guides :** https://docs.railway.app/guides

### Communauté :
- **Discord :** https://discord.gg/railway (très réactif !)
- **Forum :** https://help.railway.app

### Status :
- **Status page :** https://status.railway.app

---

## 🎯 APRÈS LA MIGRATION

### 1. Mettre à jour tes favoris
- Remplace l'URL Render par l'URL Railway
- Partage la nouvelle URL

### 2. Tester toutes les fonctionnalités
- ✅ Chat avec LLM
- ✅ Recherche web
- ✅ Météo
- ✅ Actualités
- ✅ Calculatrice
- ✅ Conversion devises
- ✅ Email (si configuré)

### 3. Surveiller les performances
- Onglet **Metrics** → Voir RAM/CPU
- Onglet **Logs** → Voir les erreurs
- Onglet **Deployments** → Voir l'historique

### 4. (Optionnel) Supprimer Render
- **Render.com** → Settings → Delete Service
- Ou garde-le en backup

---

## ✅ CHECKLIST FINALE

- [ ] Compte Railway créé
- [ ] Repo GitHub connecté
- [ ] App déployée (statut Active)
- [ ] Toutes les variables d'environnement ajoutées
- [ ] Domaine généré
- [ ] URL testée et fonctionnelle
- [ ] Chat testé
- [ ] LLM répond correctement
- [ ] Météo fonctionne
- [ ] Actualités fonctionnent
- [ ] Logs vérifiés (pas d'erreurs)
- [ ] Favoris mis à jour
- [ ] Ancienne URL Render notée (backup)

---

## 🎉 RÉSULTAT

**Avant (Render) :**
```
⚠️ 512 MB RAM
⚠️ Sleep après 15 minutes
⚠️ Lent au réveil (30-60 secondes)
⚠️ Limites strictes
```

**Après (Railway) :**
```
✅ 8 GB RAM (16× plus !)
✅ Toujours actif (0 seconde d'attente)
✅ Démarrage instantané
✅ Performances excellentes
✅ $5 gratuit/mois (largement suffisant)
```

**Ton assistant médical IA est maintenant ultra-rapide et stable ! 🚀**

---

## 📝 NOTES IMPORTANTES

### Railway vs Render :

| Critère | Render | Railway |
|---------|--------|---------|
| RAM | 512 MB | **8 GB** |
| Sleep | Oui (15min) | **Non** |
| Vitesse | Lent | **Très rapide** |
| Gratuit | Limité | **$5/mois** |
| Interface | Basique | **Moderne** |
| Logs | Basiques | **Temps réel** |
| Support | Email | **Discord actif** |

**Verdict : Railway est 10× meilleur ! 🏆**

---

## 🚀 PRÊT À MIGRER ?

**Temps total : 5 minutes**

1. https://railway.app → Login with GitHub
2. New Project → Deploy from GitHub
3. Sélectionne medical-ai-assistant
4. Ajoute les variables d'environnement
5. Generate Domain
6. Teste l'URL

**C'est tout ! Profite de ton app ultra-rapide ! 🎉**
