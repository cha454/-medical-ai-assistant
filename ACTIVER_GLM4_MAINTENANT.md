# 🚀 Activer GLM-4 (Zhipu AI) - GRATUIT et ILLIMITÉ

## ✅ GLM-4 EST DÉJÀ INTÉGRÉ !

**Bonne nouvelle :** Le code pour GLM-4 est déjà dans ton application ! Il suffit juste d'ajouter la clé API.

---

## 🎯 POURQUOI GLM-4 ?

### Avantages de GLM-4 :
- ✅ **GRATUIT** (vraiment gratuit, pas de limite cachée)
- ✅ **ILLIMITÉ** (pas de quota journalier)
- ✅ **TRÈS RAPIDE** (glm-4-flash)
- ✅ **EXCELLENT** en chinois ET en français
- ✅ **PRIORITÉ #1** dans ton code (utilisé en premier)
- ✅ **Pas de carte bancaire** nécessaire

### Comparaison :

| LLM | Gratuit | Limite | Vitesse | Qualité |
|-----|---------|--------|---------|---------|
| **GLM-4** | ✅ Oui | ✅ Illimité | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| Groq | ✅ Oui | ⚠️ 100k tokens/jour | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| Google Gemini | ✅ Oui | ✅ Illimité | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| OpenAI | ❌ Payant | ⚠️ Selon crédit | ⚡⚡ | ⭐⭐⭐⭐⭐ |

**GLM-4 = Excellent choix gratuit et illimité ! 🏆**

---

## 🚀 ACTIVATION EN 5 MINUTES

### Étape 1 : Créer un compte Zhipu AI (2 min)

1. Va sur **https://open.bigmodel.cn/**
2. Clique sur **注册** (S'inscrire) en haut à droite
3. Tu peux t'inscrire avec :
   - Email
   - Téléphone (chinois ou international)
   - WeChat
   - GitHub

**Recommandation :** Utilise GitHub (le plus simple)

4. Clique sur **GitHub** pour t'inscrire
5. Autorise Zhipu AI
6. Complète ton profil (nom, email)

### Étape 2 : Obtenir la clé API (1 min)

1. Une fois connecté, va sur **https://open.bigmodel.cn/usercenter/apikeys**
2. Ou clique sur ton profil → **API Keys**
3. Clique sur **创建新的 API Key** (Créer nouvelle clé API)
4. Donne un nom : `medical-ai-assistant`
5. Clique sur **确定** (Confirmer)
6. **COPIE IMMÉDIATEMENT** la clé (elle ne sera plus visible après)

**Format de la clé :**
```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx
```
(Environ 50 caractères avec un point au milieu)

### Étape 3 : Tester la clé (1 min) - IMPORTANT

**Test avec curl (Windows PowerShell) :**
```powershell
$headers = @{
    "Authorization" = "Bearer TA_CLE_ICI"
    "Content-Type" = "application/json"
}

$body = @{
    model = "glm-4-flash"
    messages = @(
        @{
            role = "user"
            content = "Bonjour"
        }
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://open.bigmodel.cn/api/paas/v4/chat/completions" -Method Post -Headers $headers -Body $body
```

**Ou test avec Python :**
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
    "messages": [
        {"role": "user", "content": "Bonjour"}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
```

**Si ça marche, tu verras une réponse JSON avec du texte.**
**Si erreur 401, la clé est invalide → recommence l'étape 2.**

### Étape 4 : Ajouter dans Render (1 min)

1. Va sur **Render.com** → Ton service
2. Onglet **Environment**
3. Clique sur **Add Environment Variable**
4. **Key :** `GLM_API_KEY`
5. **Value :** [Colle ta clé API]
6. ⚠️ **VÉRIFIE qu'il n'y a pas d'espaces avant/après**
7. Clique sur **Save Changes**

### Étape 5 : Désactiver les autres LLM (optionnel)

Pour que GLM-4 soit utilisé en priorité, désactive les autres :

1. Trouve `GOOGLE_API_KEY` (si existe)
2. Clique **Edit**
3. Renomme en `GOOGLE_API_KEY_BACKUP`
4. Répète pour `GROQ_API_KEY` → `GROQ_API_KEY_BACKUP`
5. **Save Changes**

**Ordre de priorité (dans le code) :**
1. **GLM-4** (si `GLM_API_KEY` existe) ← Priorité #1 !
2. Google Gemini (si `GOOGLE_API_KEY` existe)
3. OpenAI (si `OPENAI_API_KEY` existe)
4. Anthropic (si `ANTHROPIC_API_KEY` existe)
5. Groq (si `GROQ_API_KEY` existe)
6. HuggingFace (si `HUGGINGFACE_API_KEY` existe)

### Étape 6 : Vérifier (30 sec)

1. Attends 2-3 minutes (Render redémarre)
2. Va dans **Logs**
3. Tu devrais voir :
   ```
   ✓ LLM Provider initialisé: glm
   ✓ LLM activé: Zhipu AI GLM-4
   ```
4. Teste sur ton site : https://medical-ai-assistant-2k1a.onrender.com/chat
5. Pose une question
6. Le LLM devrait répondre ! 🎉

---

## 🔧 CONFIGURATION AVANCÉE

### Modèles GLM disponibles :

Dans `src/llm_provider.py`, ligne 206, tu peux changer le modèle :

```python
data = {
    "model": "glm-4-flash",  # ← Change ici
    "messages": messages,
    "max_tokens": 2000,
    "temperature": 0.7,
    "top_p": 0.9
}
```

**Modèles disponibles :**
- `glm-4-flash` - Le plus rapide (recommandé) ⚡⚡⚡
- `glm-4` - Plus puissant mais plus lent ⚡⚡
- `glm-4-plus` - Le meilleur mais payant 💰
- `glm-4-air` - Équilibré ⚡⚡

**Recommandation : Garde `glm-4-flash` (gratuit et rapide)**

### Augmenter les tokens :

Si tu veux des réponses plus longues :

```python
"max_tokens": 2000,  # ← Change à 3000 ou 4000
```

### Ajuster la créativité :

```python
"temperature": 0.7,  # ← 0.0 = précis, 1.0 = créatif
```

---

## 🆘 DÉPANNAGE

### Problème : Erreur 401 - Invalid API Key

**Cause :** Clé API invalide ou mal copiée

**Solution :**
1. Vérifie qu'il n'y a pas d'espaces avant/après la clé
2. Vérifie que la clé est complète (environ 50 caractères)
3. Régénère une nouvelle clé sur https://open.bigmodel.cn/usercenter/apikeys
4. Teste la clé AVANT de l'ajouter dans Render

### Problème : Erreur 429 - Rate Limit

**Cause :** Trop de requêtes (rare avec le plan gratuit)

**Solution :**
- Attends quelques minutes
- Le plan gratuit a des limites raisonnables mais généreuses

### Problème : Erreur 500 - Server Error

**Cause :** Problème temporaire du serveur Zhipu AI

**Solution :**
- Réessaie dans quelques minutes
- Vérifie le status : https://status.bigmodel.cn (si existe)

### Problème : GLM-4 ne s'active pas

**Vérifications :**
1. Render → Environment → `GLM_API_KEY` existe ?
2. Pas de `_BACKUP` dans le nom ?
3. Logs Render → `✓ LLM Provider initialisé: glm` ?
4. Si non, vérifie que les autres clés sont désactivées (avec `_BACKUP`)

---

## 📊 COMPARAISON DÉTAILLÉE

### GLM-4 vs Autres LLM

| Critère | GLM-4 | Groq | Google Gemini | OpenAI |
|---------|-------|------|---------------|--------|
| **Gratuit** | ✅ Oui | ✅ Oui | ✅ Oui | ❌ Payant |
| **Limite tokens/jour** | ✅ Illimité | ⚠️ 100k | ✅ Illimité | ⚠️ Selon crédit |
| **Vitesse** | ⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| **Qualité français** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Qualité chinois** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Carte bancaire** | ❌ Non | ❌ Non | ❌ Non | ✅ Oui |
| **Inscription** | ⭐⭐ Moyen | ⭐ Facile | ⭐ Facile | ⭐⭐ Moyen |

**Verdict : GLM-4 = Excellent choix gratuit et illimité ! 🏆**

---

## 🎯 RECOMMANDATION FINALE

### Pour toi :

**1. Active GLM-4 MAINTENANT (5 min)**
- Gratuit et illimité
- Très rapide
- Excellent en français

**2. Garde Google Gemini en backup**
- Renomme en `GOOGLE_API_KEY_BACKUP`
- Réactive si GLM-4 a un problème

**3. Migre vers Railway quand tu as le temps (5 min)**
- 8 GB RAM (16× plus que Render)
- Toujours actif
- Plus stable

---

## 📋 CHECKLIST

### Activation GLM-4 :
- [ ] Compte Zhipu AI créé
- [ ] Clé API obtenue
- [ ] Clé testée avec curl/Python
- [ ] Clé ajoutée dans Render (`GLM_API_KEY`)
- [ ] Autres LLM désactivés (renommés en `_BACKUP`)
- [ ] Render redémarré (2-3 min)
- [ ] Logs vérifiés : `✓ LLM activé: Zhipu AI GLM-4`
- [ ] App testée : LLM répond correctement

---

## 🎉 RÉSULTAT ATTENDU

**Avant :**
```
⚠️ Google Gemini (gemini-1.5-flash): Modèle non trouvé
⚠️ Google Gemini (gemini-1.5-pro): Modèle non trouvé
❌ Tous les modèles Google Gemini ont échoué
❌ Passage au mode basique
```

**Après :**
```
✓ LLM Provider initialisé: glm
✓ LLM activé: Zhipu AI GLM-4
✓ GLM-4: Réponse reçue
```

**Ton LLM fonctionne parfaitement ! 🎉**

---

## 📞 SUPPORT

### Zhipu AI
- **Site :** https://open.bigmodel.cn
- **Docs :** https://open.bigmodel.cn/dev/api
- **API Keys :** https://open.bigmodel.cn/usercenter/apikeys

### Guides
- **Ce guide :** `ACTIVER_GLM4_MAINTENANT.md`
- **Guide GLM-4 :** `GUIDE_GLM4.md` (si existe)
- **Migration Railway :** `MIGRATION_RAPIDE.md`

---

## 💡 CONSEIL FINAL

**GLM-4 est le meilleur choix gratuit pour toi :**
- ✅ Vraiment gratuit et illimité
- ✅ Très rapide (glm-4-flash)
- ✅ Excellent en français
- ✅ Pas de carte bancaire
- ✅ Priorité #1 dans ton code

**Action immédiate :**
1. Va sur https://open.bigmodel.cn
2. Inscris-toi avec GitHub
3. Crée une clé API
4. Ajoute dans Render : `GLM_API_KEY`
5. Teste ! 🎉

**Temps total : 5 minutes**
**Résultat : LLM gratuit et illimité ! 🚀**
