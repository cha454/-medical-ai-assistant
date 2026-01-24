# 🔧 Désactiver PostgreSQL Temporairement

## 🎯 Objectif

Faire démarrer l'application avec SQLite pendant qu'on résout le problème PostgreSQL.

## 📋 Étapes sur Railway

### 1. Supprimer la Variable DATABASE_URL

1. Va sur Railway Dashboard
2. Clique sur ton service **medical-ai-assistant**
3. Va dans **"Variables"**
4. Trouve **DATABASE_URL**
5. Clique sur les **3 points** (⋮)
6. Clique sur **"Remove"**
7. Confirme

### 2. Attendre le Redéploiement

Railway va redéployer automatiquement (2-3 minutes).

L'application va démarrer avec **SQLite** au lieu de PostgreSQL.

### 3. Vérifier

Dans les logs, tu dois voir :
```
✓ Base de données SQLite: /app/knowledge.db
✓ Base de connaissances initialisée
```

**L'application va démarrer sans erreur !** ✅

---

## ⚠️ Limitation

Avec SQLite sur Railway :
- ✅ L'application fonctionne
- ✅ Tu peux enseigner des connaissances
- ❌ Les connaissances se vident aux redémarrages

**C'est temporaire** le temps de résoudre le problème PostgreSQL.

---

## 🔄 Réactiver PostgreSQL Plus Tard

Une fois le problème résolu, tu pourras :
1. Réajouter la variable `DATABASE_URL`
2. Railway redéploiera
3. PostgreSQL fonctionnera

---

**Fais ça maintenant pour que l'application démarre !** 🚀
