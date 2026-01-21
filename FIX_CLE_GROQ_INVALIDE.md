# 🔧 FIX: Clé API Groq Invalide (Erreur 401)

## 🚨 PROBLÈME ACTUEL

```
Groq Error: 401 - {"error":{"message":"Invalid API Key"}}
```

**Cause:** La nouvelle clé Groq que tu as générée est invalide ou mal configurée.

---

## ✅ SOLUTION IMMÉDIATE (2 MINUTES) - PASSER À GOOGLE GEMINI

**Google Gemini = VRAIMENT ILLIMITÉ** (pas de limite tokens/jour comme Groq)

### Étape 1: Désactiver Groq dans Render

1. Va sur **Render.com** → Ton service
2. Onglet **Environment**
3. Trouve `GROQ_API_KEY`
4. Clique sur **Edit** (crayon)
5. Renomme en: `GROQ_API_KEY_BACKUP`
6. **Save Changes**

### Étape 2: Activer Google Gemini

1. Toujours dans **Environment**
2. Trouve `GOOGLE_API_KEY_BACKUP`
3. Clique sur **Edit** (crayon)
4. Renomme en: `GOOGLE_API_KEY`
5. **Save Changes**

### Étape 3: Attendre le redémarrage

- Render va redémarrer automatiquement (2-3 minutes)
- Va dans **Logs** pour vérifier
- Tu devrais voir: `✓ LLM activé: Google Gemini`

### ✅ AVANTAGES GOOGLE GEMINI:
- ✅ **Vraiment illimité** (pas de limite tokens/jour)
- ✅ **Gratuit** (60 requêtes/minute)
- ✅ **Très rapide** (gemini-1.5-flash)
- ✅ **Excellent** pour conversations longues
- ✅ **Pas de quota journalier** (contrairement à Groq)

---

## 🔄 ALTERNATIVE: Recréer une clé Groq valide

Si tu veux vraiment utiliser Groq, voici comment créer une clé valide:

### Étape 1: Supprimer l'ancienne clé

1. Va sur https://console.groq.com/keys
2. Trouve ta clé actuelle
3. Clique sur **Delete** (poubelle)
4. Confirme la suppression

### Étape 2: Créer une NOUVELLE clé

1. Clique sur **Create API Key**
2. Donne un nom: `medical-ai-assistant-2026`
3. Clique sur **Create**
4. **COPIE IMMÉDIATEMENT** la clé (elle ne sera plus visible après)

### Étape 3: Vérifier la clé copiée

⚠️ **ATTENTION - Erreurs courantes:**
- ❌ Espaces avant/après la clé
- ❌ Retour à la ligne dans la clé
- ❌ Caractères manquants (copie incomplète)
- ❌ Clé expirée ou révoquée

✅ **Format correct:**
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Commence par `gsk_`
- Environ 56 caractères
- Pas d'espaces, pas de retours à la ligne

### Étape 4: Tester la clé AVANT de l'ajouter dans Render

**Option A: Test en ligne (recommandé)**
```bash
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer TA_CLE_ICI"
```

Si ça marche, tu verras une liste de modèles.
Si erreur 401, la clé est invalide → recommence l'étape 2.

**Option B: Test avec Python**
```python
import requests

api_key = "TA_CLE_ICI"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)

if response.status_code == 200:
    print("✅ Clé valide!")
else:
    print(f"❌ Erreur {response.status_code}: {response.text}")
```

### Étape 5: Ajouter dans Render

1. **Render.com** → Ton service → **Environment**
2. Trouve `GROQ_API_KEY` (ou `GROQ_API_KEY_BACKUP`)
3. Clique sur **Edit**
4. **Colle la nouvelle clé** (Ctrl+V)
5. ⚠️ **VÉRIFIE qu'il n'y a pas d'espaces avant/après**
6. **Save Changes**
7. Attendre 2-3 minutes (redémarrage)
8. Vérifier les **Logs**: `✓ LLM activé: Groq (Llama 3.1)`

---

## 🎯 RECOMMANDATION FINALE

**Je te conseille FORTEMENT de passer à Google Gemini:**

### Pourquoi Gemini > Groq ?

| Critère | Groq | Google Gemini |
|---------|------|---------------|
| **Limite tokens/jour** | ❌ 100,000 (atteint rapidement) | ✅ Illimité |
| **Limite requêtes** | ⚠️ Peut être bloqué | ✅ 60/minute (largement suffisant) |
| **Stabilité** | ⚠️ Erreurs 429 fréquentes | ✅ Très stable |
| **Qualité** | ✅ Excellent | ✅ Excellent |
| **Vitesse** | ✅ Très rapide | ✅ Très rapide |
| **Gratuit** | ✅ Oui | ✅ Oui |
| **Problèmes de clé** | ⚠️ Fréquents | ✅ Rares |

**Verdict:** Google Gemini est plus fiable pour un usage intensif.

---

## 📊 VÉRIFIER QUEL LLM EST ACTIF

### Dans les logs Render:

```
✓ LLM activé: Groq (Llama 3.1)          ← Groq actif
✓ LLM activé: Google Gemini             ← Gemini actif
✓ LLM activé: OpenAI GPT-4              ← OpenAI actif
```

### Ordre de priorité (dans `llm_provider.py`):

1. **GLM** (si `GLM_API_KEY` existe)
2. **Google Gemini** (si `GOOGLE_API_KEY` existe)
3. **OpenAI** (si `OPENAI_API_KEY` existe)
4. **Anthropic** (si `ANTHROPIC_API_KEY` existe)
5. **Groq** (si `GROQ_API_KEY` existe)
6. **HuggingFace** (si `HUGGINGFACE_API_KEY` existe)

**Actuellement dans Render:**
- `GROQ_API_KEY` = invalide (erreur 401)
- `GOOGLE_API_KEY_BACKUP` = valide mais désactivé (suffixe `_BACKUP`)
- `OPENAI_API_KEY_BACKUP` = valide mais désactivé (suffixe `_BACKUP`)

**Solution:** Renommer `GOOGLE_API_KEY_BACKUP` → `GOOGLE_API_KEY`

---

## 🆘 BESOIN D'AIDE ?

### Si Google Gemini ne marche pas:

1. Vérifie que `GOOGLE_API_KEY` existe (sans `_BACKUP`)
2. Vérifie les logs: `✓ LLM activé: Google Gemini`
3. Si erreur 404, la clé est peut-être expirée → régénère-la sur https://aistudio.google.com/apikey

### Si Groq continue à échouer:

1. Vérifie que la clé commence bien par `gsk_`
2. Teste la clé avec curl AVANT de l'ajouter dans Render
3. Assure-toi qu'il n'y a pas d'espaces ou de retours à la ligne
4. Si ça ne marche toujours pas → passe à Gemini (plus fiable)

---

## 📝 RÉSUMÉ - ACTION IMMÉDIATE

**Pour résoudre MAINTENANT (2 minutes):**

```
1. Render.com → Environment
2. GROQ_API_KEY → Renommer en GROQ_API_KEY_BACKUP
3. GOOGLE_API_KEY_BACKUP → Renommer en GOOGLE_API_KEY
4. Save Changes
5. Attendre 2-3 minutes
6. Vérifier logs: ✓ LLM activé: Google Gemini
7. Tester sur le site: https://medical-ai-assistant-2k1a.onrender.com/chat
```

**Résultat:** LLM illimité, stable et gratuit ! 🎉
