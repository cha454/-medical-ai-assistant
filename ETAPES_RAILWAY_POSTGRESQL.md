# 🚂 3 Étapes pour Activer PostgreSQL sur Railway

## 📌 Pourquoi ?

Ta base de connaissances se vide à chaque actualisation car SQLite n'est pas persistant sur Railway.

**Solution** : Ajouter PostgreSQL (gratuit et persistant).

---

## 🎯 Étape 1 : Ajouter PostgreSQL

1. Va sur https://railway.app
2. Ouvre ton projet **medical-ai-assistant**
3. Clique sur **"+ New"** (bouton en haut à droite)
4. Sélectionne **"Database"**
5. Choisis **"PostgreSQL"**
6. Attends 30 secondes ⏳

✅ **Résultat** : Une nouvelle carte "PostgreSQL" apparaît dans ton projet

---

## 🎯 Étape 2 : Vérifier la Configuration

1. Clique sur ton service **medical-ai-assistant** (pas PostgreSQL)
2. Va dans l'onglet **"Variables"**
3. Cherche **DATABASE_URL**

✅ **Résultat** : Tu dois voir une variable `DATABASE_URL` avec une valeur qui commence par `postgresql://`

**Si tu ne la vois pas** :
- Clique sur la carte **PostgreSQL**
- Va dans **"Connect"**
- Copie la variable `DATABASE_URL`
- Retourne sur **medical-ai-assistant** → Variables
- Clique **"+ New Variable"**
- Colle `DATABASE_URL` et sa valeur

---

## 🎯 Étape 3 : Redéployer

1. Reste sur ton service **medical-ai-assistant**
2. Va dans l'onglet **"Deployments"**
3. Clique sur **"Redeploy"** (bouton en haut à droite)
4. Attends 2-3 minutes ⏳

✅ **Résultat** : L'application redémarre avec PostgreSQL

---

## ✅ Vérification : Ça Marche ?

### 1. Vérifier les Logs

1. Va dans l'onglet **"Logs"**
2. Cherche cette ligne :
   ```
   ✓ Utilisation de PostgreSQL (Railway)
   ```

✅ Si tu vois ça, c'est bon ! 🎉

❌ Si tu vois `SQLite`, retourne à l'étape 1.

### 2. Tester la Persistance

1. Va sur ton site : https://medical-ai-assistant-production.up.railway.app/teach
2. Enseigne quelque chose :
   ```
   Mbolo signifie bonjour en Fang
   ```
3. Va sur `/knowledge` → ✅ La connaissance apparaît
4. Appuie sur **F5** (actualiser) → ✅ La connaissance est TOUJOURS là
5. Va sur `/chat` et demande :
   ```
   Comment dit-on bonjour en Fang ?
   ```
6. ✅ L'IA répond : **"Mbolo"**

---

## 🎉 C'est Tout !

Si tous les tests passent, ta base de connaissances est maintenant **persistante** ! 🚀

Les connaissances survivent maintenant à :
- ✅ Actualisation de la page
- ✅ Redémarrage de l'application
- ✅ Redéploiement
- ✅ Mises à jour du code

---

## 🐛 Problème ?

### La base se vide toujours

**Checklist** :
- [ ] PostgreSQL créé ? (carte visible dans Railway)
- [ ] `DATABASE_URL` existe ? (Variables)
- [ ] Logs montrent "PostgreSQL" ? (Logs)
- [ ] Application redéployée ? (Deployments)

### Erreur dans les logs

**"No module named 'psycopg2'"** → Attends la fin du déploiement

**"could not connect to server"** → PostgreSQL pas créé (retour étape 1)

---

## 📚 Plus d'Infos

- `CORRECTIONS_24_JAN_2026.md` - Guide rapide
- `SOLUTION_PERSISTANCE_POSTGRESQL.md` - Guide complet technique

---

**Date** : 24 Janvier 2026  
**Temps estimé** : 5 minutes  
**Difficulté** : ⭐ Facile
