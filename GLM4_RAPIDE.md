# ⚡ GLM-4 en 5 Minutes - Guide Ultra-Rapide

## 🎯 POURQUOI GLM-4 ?

✅ **GRATUIT** et **ILLIMITÉ**
✅ **DÉJÀ INTÉGRÉ** dans ton code
✅ **PRIORITÉ #1** (utilisé en premier)
✅ **Pas de carte bancaire**

---

## 🚀 ACTIVATION EN 5 ÉTAPES

### 1️⃣ Créer compte (2 min)
```
https://open.bigmodel.cn
→ Clique "注册" (S'inscrire)
→ Choisis GitHub (le plus simple)
→ Autorise
```

### 2️⃣ Obtenir clé API (1 min)
```
https://open.bigmodel.cn/usercenter/apikeys
→ Clique "创建新的 API Key"
→ Nom: medical-ai-assistant
→ COPIE la clé immédiatement
```

### 3️⃣ Tester la clé (1 min)
```python
import requests

api_key = "TA_CLE_ICI"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "glm-4-flash",
    "messages": [{"role": "user", "content": "Bonjour"}]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)  # Doit être 200
```

### 4️⃣ Ajouter dans Render (1 min)
```
Render.com → Environment
→ Add Environment Variable
→ Key: GLM_API_KEY
→ Value: [ta clé]
→ Save Changes
```

### 5️⃣ Désactiver les autres (optionnel)
```
GOOGLE_API_KEY → Renommer en GOOGLE_API_KEY_BACKUP
GROQ_API_KEY → Renommer en GROQ_API_KEY_BACKUP
→ Save Changes
```

---

## ✅ VÉRIFICATION

**Logs Render (après 2-3 min) :**
```
✓ LLM Provider initialisé: glm
✓ LLM activé: Zhipu AI GLM-4
```

**Teste sur ton site :**
```
https://medical-ai-assistant-2k1a.onrender.com/chat
→ Pose une question
→ LLM répond ! 🎉
```

---

## 📊 COMPARAISON RAPIDE

| LLM | Gratuit | Limite | Carte bancaire |
|-----|---------|--------|----------------|
| **GLM-4** | ✅ | ✅ Illimité | ❌ Non |
| Groq | ✅ | ⚠️ 100k/jour | ❌ Non |
| Gemini | ✅ | ✅ Illimité | ❌ Non |
| OpenAI | ❌ | ⚠️ Selon crédit | ✅ Oui |

**GLM-4 = Meilleur choix gratuit ! 🏆**

---

## 🆘 PROBLÈME ?

**Erreur 401 ?**
→ Vérifie la clé (pas d'espaces)
→ Régénère une nouvelle clé

**GLM-4 ne s'active pas ?**
→ Vérifie `GLM_API_KEY` dans Render
→ Désactive les autres LLM (renomme en `_BACKUP`)

**Besoin d'aide ?**
→ Lis `ACTIVER_GLM4_MAINTENANT.md` (guide complet)

---

## 🎉 RÉSULTAT

**Avant :**
```
❌ Google Gemini échoue
❌ Mode basique
```

**Après :**
```
✅ GLM-4 activé
✅ LLM gratuit et illimité
✅ Réponses rapides
```

---

## 🚀 GO !

**Temps : 5 minutes**
**Résultat : LLM gratuit et illimité ! 🎉**

**→ https://open.bigmodel.cn**
