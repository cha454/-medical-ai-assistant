# ⚡ Migration Ultra-Rapide - Render → Railway

## 🎯 EN 5 MINUTES CHRONO

### Étape 1 : Créer compte Railway (1 min)
```
1. Va sur https://railway.app
2. Clique "Start a New Project"
3. "Login with GitHub"
4. Autorise Railway
```

### Étape 2 : Déployer (2 min)
```
1. "New Project"
2. "Deploy from GitHub repo"
3. Cherche "medical-ai-assistant"
4. Clique dessus
5. Attendre (Railway installe tout automatiquement)
```

### Étape 3 : Variables (2 min)
```
1. Clique sur ton projet
2. Onglet "Variables"
3. Copie depuis Render → Colle dans Railway :

   GROQ_API_KEY = [copie depuis Render]
   GOOGLE_API_KEY = [copie depuis Render]
   NEWS_API_KEY = [copie depuis Render]
   OPENWEATHER_API_KEY = [copie depuis Render]
   SENDGRID_API_KEY = [copie depuis Render]
   SENDGRID_FROM_EMAIL = [copie depuis Render]
   SECRET_KEY = [copie depuis Render]
```

### Étape 4 : URL (30 sec)
```
1. Onglet "Settings"
2. Section "Domains"
3. "Generate Domain"
4. Copie l'URL
```

### Étape 5 : Tester (30 sec)
```
1. Ouvre l'URL
2. Teste le chat
3. C'est tout ! 🎉
```

---

## 📋 CHECKLIST

- [ ] Compte Railway créé
- [ ] Repo déployé
- [ ] Variables copiées
- [ ] URL générée
- [ ] App testée

---

## 🎉 RÉSULTAT

**Avant (Render) :**
- ⚠️ 512 MB RAM
- ⚠️ Sleep 15 minutes
- ⚠️ Lent

**Après (Railway) :**
- ✅ 8 GB RAM (16× plus !)
- ✅ Toujours actif
- ✅ Ultra-rapide

---

## 📚 GUIDES COMPLETS

- `ALTERNATIVES_HEBERGEMENT.md` - Tous les hébergeurs
- `MIGRATION_RAILWAY.md` - Guide détaillé Railway
- `HEBERGEURS_COMPARAISON.md` - Comparaison complète
- `COMMANDES_DEPLOIEMENT.md` - Toutes les commandes

---

## 🆘 PROBLÈME ?

**App ne démarre pas ?**
→ Vérifie les variables dans Railway → Variables

**LLM ne répond pas ?**
→ Vérifie que GROQ_API_KEY ou GOOGLE_API_KEY existe

**404 Not Found ?**
→ Attends 2-3 minutes (propagation DNS)

---

## 🚀 PRÊT ?

**GO → https://railway.app**

**Temps total : 5 minutes**
**Résultat : App 10× plus rapide ! 🎉**
