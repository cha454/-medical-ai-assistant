# 🔄 Passer d'OpenAI à Google Gemini (GRATUIT)

## 🔴 Problème Actuel

```
OpenAI Error: 429 - Rate limit reached
Limit: 100,000 tokens/minute
Used: 98,275 tokens
Attendre: 2-3 heures
```

**Ton compte OpenAI a atteint sa limite !**

---

## ✅ Solution : Utiliser Google Gemini (GRATUIT et ILLIMITÉ)

### Avantages de Gemini :
- ✅ **100% GRATUIT** (pas de carte bancaire requise)
- ✅ **Pas de limite stricte** comme OpenAI
- ✅ **Aussi performant** que GPT-4
- ✅ **Configuration en 5 minutes**

---

## 📝 Étapes pour Activer Gemini

### 1️⃣ Obtenir une Clé API Google Gemini (2 minutes)

1. Va sur : **https://makersuite.google.com/app/apikey**
2. Connecte-toi avec ton compte Google
3. Clique sur **"Create API Key"**
4. Sélectionne un projet Google Cloud (ou crée-en un nouveau)
5. **Copie la clé** (commence par `AIza...`)
   - Exemple : `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

---

### 2️⃣ Ajouter la Clé dans Render (2 minutes)

1. Va sur ton dashboard Render : **https://dashboard.render.com/**
2. Clique sur ton service **"medical-ai-assistant"**
3. Dans le menu de gauche, clique sur **"Environment"**
4. Clique sur **"Add Environment Variable"**
5. Remplis :
   - **Key** : `GOOGLE_API_KEY`
   - **Value** : Colle ta clé Gemini (celle que tu as copiée)
6. Clique sur **"Save Changes"**

---

### 3️⃣ Désactiver OpenAI Temporairement (1 minute)

**Option A : Supprimer la clé OpenAI**
1. Dans les variables d'environnement Render
2. Trouve `OPENAI_API_KEY`
3. Clique sur les **3 points** à droite
4. Clique sur **"Delete"**
5. Confirme

**Option B : Renommer la clé (pour la garder en backup)**
1. Trouve `OPENAI_API_KEY`
2. Clique sur **"Edit"**
3. Change le nom en `OPENAI_API_KEY_BACKUP`
4. Save

---

### 4️⃣ Redémarrer l'Application

1. Render va **redémarrer automatiquement** après avoir sauvegardé les changements
2. Attends **2-3 minutes**
3. Vérifie les logs pour voir :
   ```
   ✓ LLM Provider initialisé: google
   ✓ LLM activé: Google Gemini
   ```

---

## 🧪 Tester que Ça Marche

1. Va sur : **https://medical-ai-assistant-2k1a.onrender.com/chat**
2. Pose une question : **"Comment tu vas ?"**
3. Tu devrais recevoir une réponse naturelle du LLM
4. Vérifie les logs Render pour voir :
   ```
   📤 Envoi au LLM: Comment tu vas ?...
   📥 Réponse LLM reçue: True
   ```

---

## 📊 Comparaison OpenAI vs Gemini

| Critère | OpenAI GPT-4 | Google Gemini |
|---------|--------------|---------------|
| **Prix** | Payant (~$0.002/1K tokens) | **GRATUIT** |
| **Limite** | 100K tokens/min | Très élevée |
| **Carte bancaire** | Requise | **Non requise** |
| **Performance** | Excellent | **Excellent** |
| **Multilingue** | Oui | **Oui** |
| **Disponibilité** | Peut être limité | **Toujours disponible** |

---

## 🔧 Dépannage

### Problème : "Google API Error: 400"
**Solution** : Ta clé API est invalide. Vérifie que tu l'as bien copiée sans espaces.

### Problème : "Google API Error: 403"
**Solution** : L'API Gemini n'est pas activée. Va sur https://console.cloud.google.com/ et active "Generative Language API".

### Problème : L'IA répond toujours en mode basique
**Solution** : 
1. Vérifie que `GOOGLE_API_KEY` est bien dans les variables d'environnement Render
2. Vérifie que `OPENAI_API_KEY` est supprimée ou renommée
3. Redémarre manuellement le service (bouton "Manual Deploy")

---

## 💡 Conseil

**Garde ta clé OpenAI en backup** (renomme-la en `OPENAI_API_KEY_BACKUP`) au cas où tu voudrais revenir à OpenAI plus tard. Mais Gemini est vraiment excellent et gratuit, donc tu n'en auras probablement pas besoin !

---

## 🎉 Résultat Final

Avec Gemini activé :
- ✅ Réponses naturelles et intelligentes
- ✅ Pas de limite de tokens
- ✅ 100% gratuit
- ✅ Disponible 24/7

---

**Date** : 20 janvier 2026  
**Temps estimé** : 5 minutes  
**Difficulté** : Facile ⭐
