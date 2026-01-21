# 🔧 FIX: Google Gemini - Modèle Non Trouvé (404)

## 🚨 PROBLÈME ACTUEL

```
⚠️ Google Gemini (gemini-1.5-flash): Modèle non trouvé, essai suivant...
⚠️ Google Gemini (gemini-1.5-pro): Modèle non trouvé, essai suivant...
⚠️ Google Gemini (gemini-pro): Modèle non trouvé, essai suivant...
❌ Tous les modèles Google Gemini ont échoué
```

**Causes possibles :**
1. Clé API Google invalide ou expirée
2. Clé API pas activée pour Gemini
3. Quota dépassé
4. Noms de modèles changés

---

## ✅ SOLUTION 1 : VÉRIFIER/RÉGÉNÉRER CLÉ GOOGLE (2 MINUTES)

### Étape 1 : Vérifier la clé actuelle

1. Va sur **https://aistudio.google.com/apikey**
2. Login avec ton compte Google
3. Vérifie si ta clé existe et est active

### Étape 2 : Créer une NOUVELLE clé

1. Sur https://aistudio.google.com/apikey
2. Clique sur **Create API Key**
3. Sélectionne un projet (ou crée-en un nouveau)
4. Clique sur **Create API key in existing project**
5. **COPIE IMMÉDIATEMENT** la clé (elle commence par `AIzaSy...`)

### Étape 3 : Tester la clé AVANT de l'ajouter

**Test rapide avec curl :**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=TA_CLE_ICI" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Bonjour"}]}]}'
```

**Si ça marche, tu verras une réponse JSON.**
**Si erreur 404, la clé n'est pas activée pour Gemini.**

### Étape 4 : Activer l'API Gemini

1. Va sur **https://console.cloud.google.com/apis/library**
2. Cherche **"Generative Language API"**
3. Clique dessus
4. Clique sur **Enable** (Activer)
5. Attends 2-3 minutes

### Étape 5 : Ajouter dans Render

1. **Render.com** → Ton service → **Environment**
2. Trouve `GOOGLE_API_KEY` (ou `GOOGLE_API_KEY_BACKUP`)
3. Clique sur **Edit**
4. **Colle la nouvelle clé**
5. ⚠️ **VÉRIFIE qu'il n'y a pas d'espaces**
6. **Save Changes**
7. Attendre 2-3 minutes (redémarrage)

### Étape 6 : Vérifier les logs

Dans Render → Logs, tu devrais voir :
```
✓ LLM activé: Google Gemini
```

Et plus d'erreurs 404.

---

## ✅ SOLUTION 2 : PASSER À GROQ (PLUS SIMPLE)

**Si Google Gemini continue à échouer, passe à Groq :**

### Étape 1 : Créer une clé Groq

1. Va sur **https://console.groq.com/keys**
2. Login avec Google/GitHub
3. Clique sur **Create API Key**
4. Nom : `medical-ai-assistant-2026`
5. **COPIE la clé** (commence par `gsk_...`)

### Étape 2 : Tester la clé

```bash
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer TA_CLE_ICI"
```

Si ça marche, tu verras une liste de modèles.

### Étape 3 : Ajouter dans Render

1. **Render.com** → Environment
2. Trouve `GROQ_API_KEY`
3. **Edit** → Colle la nouvelle clé
4. **Save Changes**
5. Attendre 2-3 minutes

### Étape 4 : Désactiver Google (optionnel)

1. Trouve `GOOGLE_API_KEY`
2. **Edit** → Renommer en `GOOGLE_API_KEY_BACKUP`
3. **Save Changes**

**Résultat : Groq sera utilisé en priorité ! ✅**

---

## ✅ SOLUTION 3 : MIGRER VERS RAILWAY (RECOMMANDÉ)

**Pourquoi migrer maintenant ?**

**Render (Actuel) :**
- ⚠️ 512 MB RAM (insuffisant)
- ⚠️ Sleep 15 minutes
- ⚠️ Problèmes de clés API fréquents
- ⚠️ Lent

**Railway (Nouveau) :**
- ✅ 8 GB RAM (16× plus)
- ✅ Toujours actif
- ✅ $5 gratuit/mois
- ✅ Plus stable

**Guide : `MIGRATION_RAPIDE.md` (5 minutes)**

---

## 🔍 DIAGNOSTIC DÉTAILLÉ

### Vérifier quelle clé est active

Dans Render → Environment, vérifie :

```
✅ GOOGLE_API_KEY existe (sans _BACKUP) → Google actif
✅ GROQ_API_KEY existe (sans _BACKUP) → Groq actif
✅ OPENAI_API_KEY existe (sans _BACKUP) → OpenAI actif
```

**Ordre de priorité (dans llm_provider.py) :**
1. GLM (si `GLM_API_KEY`)
2. **Google Gemini** (si `GOOGLE_API_KEY`)
3. OpenAI (si `OPENAI_API_KEY`)
4. Anthropic (si `ANTHROPIC_API_KEY`)
5. Groq (si `GROQ_API_KEY`)
6. HuggingFace (si `HUGGINGFACE_API_KEY`)

**Actuellement :** Google est en priorité mais échoue → Passe au mode basique

---

## 🎯 RECOMMANDATION FINALE

### Option A : Fix rapide (2 minutes)
**Passer à Groq :**
1. Créer clé Groq : https://console.groq.com/keys
2. Ajouter dans Render : `GROQ_API_KEY`
3. Désactiver Google : Renommer `GOOGLE_API_KEY` → `GOOGLE_API_KEY_BACKUP`

**Avantages :**
- ✅ Rapide (2 minutes)
- ✅ Gratuit (100k tokens/jour)
- ✅ Très rapide

**Inconvénients :**
- ⚠️ Limite 100k tokens/jour (peut être atteint)

---

### Option B : Fix complet (5 minutes)
**Régénérer clé Google Gemini :**
1. https://aistudio.google.com/apikey
2. Créer nouvelle clé
3. Activer "Generative Language API"
4. Tester la clé
5. Ajouter dans Render

**Avantages :**
- ✅ Vraiment illimité
- ✅ Très performant
- ✅ Gratuit

**Inconvénients :**
- ⚠️ Plus long à configurer

---

### Option C : Migration Railway (5 minutes) - RECOMMANDÉ
**Migrer vers Railway :**
1. Suivre `MIGRATION_RAPIDE.md`
2. 8 GB RAM (16× plus)
3. Toujours actif
4. Plus stable

**Avantages :**
- ✅ Résout TOUS les problèmes
- ✅ 8 GB RAM
- ✅ Pas de sleep
- ✅ Plus stable

**Inconvénients :**
- ⚠️ Nécessite carte bancaire (mais gratuit si < $5/mois)

---

## 🆘 DÉPANNAGE

### Problème : Clé Google valide mais erreur 404

**Cause :** API Gemini pas activée

**Solution :**
1. https://console.cloud.google.com/apis/library
2. Cherche "Generative Language API"
3. Enable
4. Attends 2-3 minutes

### Problème : Quota dépassé

**Erreur :** `429 - Quota exceeded`

**Solution :**
- Attends 24h (quota se renouvelle)
- Ou passe à Groq temporairement

### Problème : Clé invalide

**Erreur :** `401 - Invalid API Key`

**Solution :**
- Régénère une nouvelle clé
- Vérifie qu'il n'y a pas d'espaces
- Teste la clé avant de l'ajouter

---

## 📋 CHECKLIST

### Pour fixer Google Gemini :
- [ ] Aller sur https://aistudio.google.com/apikey
- [ ] Créer nouvelle clé API
- [ ] Activer "Generative Language API"
- [ ] Tester la clé avec curl
- [ ] Ajouter dans Render
- [ ] Vérifier les logs

### Pour passer à Groq :
- [ ] Aller sur https://console.groq.com/keys
- [ ] Créer nouvelle clé API
- [ ] Tester la clé avec curl
- [ ] Ajouter dans Render (`GROQ_API_KEY`)
- [ ] Désactiver Google (renommer en `_BACKUP`)
- [ ] Vérifier les logs

### Pour migrer vers Railway :
- [ ] Lire `MIGRATION_RAPIDE.md`
- [ ] Créer compte Railway
- [ ] Déployer depuis GitHub
- [ ] Copier variables d'environnement
- [ ] Tester l'app

---

## 🎉 RÉSULTAT ATTENDU

**Après le fix :**
```
✓ LLM activé: Groq (Llama 3.1)
ou
✓ LLM activé: Google Gemini
```

**Plus d'erreurs 404 ! ✅**

**LLM répond correctement ! ✅**

---

## 💡 CONSEIL FINAL

**Pour toi, je recommande :**

**1. Fix immédiat (2 min) :** Passer à Groq
- Rapide et simple
- Fonctionne immédiatement

**2. Long terme (5 min) :** Migrer vers Railway
- Résout tous les problèmes
- 8 GB RAM
- Plus stable

**Action immédiate :**
1. Crée une clé Groq : https://console.groq.com/keys
2. Ajoute-la dans Render : `GROQ_API_KEY`
3. Désactive Google : Renommer `GOOGLE_API_KEY` → `GOOGLE_API_KEY_BACKUP`
4. Teste ! 🎉

**Puis quand tu as 5 minutes :**
→ Migre vers Railway avec `MIGRATION_RAPIDE.md`
