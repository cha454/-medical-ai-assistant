# 🚀 Guide d'Intégration API - Assistant Médical IA

## 📋 Ce qui a été ajouté

J'ai créé un **système d'intégration API centralisé** pour ton projet :

### ✅ Nouveaux Fichiers

1. **`.env.example`** - Template de configuration des clés API
2. **`src/api_integration.py`** - Gestionnaire centralisé de toutes les APIs
3. **`src/api_routes.py`** - Nouveaux endpoints REST pour Flask
4. **`API_DOCUMENTATION.md`** - Documentation complète en anglais
5. **`test_api_integration.py`** - Script de test des intégrations
6. **`GUIDE_INTEGRATION_FR.md`** - Ce guide en français

### 🔧 Fichiers Modifiés

- **`app.py`** - Ajout des nouvelles routes API

---

## 🎯 Fonctionnalités Ajoutées

### 1. **Intégration LLM** (Intelligence Artificielle)
- Support de **4 providers** : OpenAI, Claude, Gemini, Mistral
- Génération de réponses intelligentes
- Chat conversationnel avec historique

### 2. **Service Email**
- **SendGrid** (recommandé pour Render)
- **SMTP** (Gmail, etc.)
- Envoi de résumés de consultation

### 3. **Recherche Web Médicale**
- **Wikipedia** (gratuit)
- **DuckDuckGo** (gratuit)
- **PubMed** (articles scientifiques gratuits)
- Cache intelligent (24h)

### 4. **Analyse d'Images**
- Classification de lésions cutanées
- Support TensorFlow
- Format: upload ou base64

### 5. **Endpoints Enrichis**
- `/api/enhanced/chat` - Chat avec LLM + recherche web
- `/api/enhanced/diagnose` - Diagnostic ML + LLM + web
- `/api/services/status` - Statut de tous les services

---

## 🚀 Installation Rapide

### Étape 1: Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 2: Configurer les clés API

```bash
# Copier le template
cp .env.example .env

# Éditer avec tes clés
notepad .env  # Windows
```

### Étape 3: Tester les intégrations

```bash
python test_api_integration.py
```

### Étape 4: Lancer l'application

```bash
python app.py
```

L'app sera sur `http://localhost:5000`

---

## 🔑 Configuration des Clés API

### Option 1: LLM (Recommandé)

Choisis **UN** provider :

#### OpenAI (ChatGPT)
```env
OPENAI_API_KEY=sk-...
```
- Site: https://platform.openai.com/api-keys
- Prix: ~$0.002 par 1000 tokens
- Modèle: GPT-4 ou GPT-3.5

#### Anthropic Claude
```env
ANTHROPIC_API_KEY=sk-ant-...
```
- Site: https://console.anthropic.com/
- Prix: ~$0.003 par 1000 tokens
- Modèle: Claude 3

#### Google Gemini
```env
GOOGLE_API_KEY=AIza...
```
- Site: https://makersuite.google.com/app/apikey
- **GRATUIT** jusqu'à 60 requêtes/minute
- Modèle: Gemini Pro

#### Mistral AI
```env
MISTRAL_API_KEY=...
```
- Site: https://console.mistral.ai/
- Prix: ~$0.001 par 1000 tokens
- Modèle: Mistral Medium

### Option 2: Email

#### SendGrid (Recommandé pour Render)
```env
SENDGRID_API_KEY=SG....
```
- Site: https://app.sendgrid.com/settings/api_keys
- **GRATUIT** : 100 emails/jour
- Fonctionne sur Render

#### SMTP (Gmail, etc.)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ton-email@gmail.com
SMTP_PASSWORD=ton-mot-de-passe-app
```
- ⚠️ Peut être bloqué sur Render
- Gmail: Utilise un "mot de passe d'application"

### Option 3: Recherche Web

**Aucune clé requise !** 
- Wikipedia, DuckDuckGo, PubMed sont gratuits
- Fonctionne immédiatement

---

## 📝 Exemples d'Utilisation

### Test 1: Vérifier le statut

```bash
curl http://localhost:5000/api/services/status
```

### Test 2: Chat enrichi

```bash
curl -X POST http://localhost:5000/api/enhanced/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Qu'est-ce que le diabète?\", \"language\": \"fr\", \"use_web_search\": true}"
```

### Test 3: Recherche web

```bash
curl -X POST http://localhost:5000/api/search/medical \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"hypertension\", \"language\": \"fr\"}"
```

### Test 4: Diagnostic enrichi

```bash
curl -X POST http://localhost:5000/api/enhanced/diagnose \
  -H "Content-Type: application/json" \
  -d "{\"symptoms\": [\"fièvre\", \"toux\"], \"language\": \"fr\"}"
```

---

## 🧪 Test avec Python

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# 1. Vérifier le statut
response = requests.get(f"{BASE_URL}/api/services/status")
print(response.json())

# 2. Chat enrichi
response = requests.post(f"{BASE_URL}/api/enhanced/chat", json={
    "message": "Qu'est-ce que le diabète?",
    "language": "fr",
    "use_web_search": True
})
print(response.json()['response'])

# 3. Recherche web
response = requests.post(f"{BASE_URL}/api/search/medical", json={
    "query": "hypertension",
    "language": "fr"
})
print(response.json())

# 4. Envoi email (si configuré)
response = requests.post(f"{BASE_URL}/api/email/send", json={
    "to_email": "test@example.com",
    "subject": "Test",
    "body": "Message de test"
})
print(response.json())
```

---

## 🌐 Utilisation depuis le Frontend

### JavaScript (Fetch API)

```javascript
// Chat enrichi avec recherche web
async function chatEnrichi(message) {
  const response = await fetch('/api/enhanced/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      message: message,
      language: 'fr',
      use_web_search: true
    })
  });
  
  const data = await response.json();
  console.log('Réponse:', data.response);
  
  if (data.web_search) {
    console.log('Info web:', data.web_search);
  }
}

// Diagnostic enrichi
async function diagnosticEnrichi(symptoms) {
  const response = await fetch('/api/enhanced/diagnose', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      symptoms: symptoms,
      language: 'fr'
    })
  });
  
  const data = await response.json();
  console.log('Résultats:', data.results);
  console.log('Explication LLM:', data.llm_explanation);
  console.log('Info web:', data.web_info);
}

// Utilisation
chatEnrichi("Qu'est-ce que le diabète?");
diagnosticEnrichi(['fièvre', 'toux', 'fatigue']);
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│           Frontend (chat.html)              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         Flask App (app.py)                  │
│  ┌──────────────────────────────────────┐   │
│  │  api_routes.py (Nouveaux endpoints)  │   │
│  └──────────────┬───────────────────────┘   │
└─────────────────┼───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│    api_integration.py (Gestionnaire)        │
│  ┌──────────┬──────────┬──────────┬──────┐  │
│  │   LLM    │  Email   │   Web    │ Image│  │
│  └──────────┴──────────┴──────────┴──────┘  │
└─────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         Services Externes                   │
│  • OpenAI / Claude / Gemini / Mistral       │
│  • SendGrid / SMTP                          │
│  • Wikipedia / DuckDuckGo / PubMed          │
│  • TensorFlow                               │
└─────────────────────────────────────────────┘
```

---

## 🎯 Cas d'Usage

### 1. Mode Basique (Sans clés API)
- ✅ Chatbot de base
- ✅ Classification ML
- ✅ Vérification médicaments
- ✅ Recherche web (gratuit)

### 2. Mode Avancé (Avec LLM)
- ✅ Réponses intelligentes
- ✅ Explications détaillées
- ✅ Chat contextuel
- ✅ Recherche web enrichie

### 3. Mode Complet (Tout configuré)
- ✅ LLM + Recherche web
- ✅ Envoi d'emails
- ✅ Analyse d'images
- ✅ Diagnostic enrichi

---

## 🔧 Dépannage

### Problème: "LLM non disponible"
**Solution:** Configure une clé API dans `.env`
```env
OPENAI_API_KEY=sk-...
# OU
GOOGLE_API_KEY=AIza...  # GRATUIT!
```

### Problème: "Service email non disponible"
**Solution:** Configure SendGrid (recommandé)
```env
SENDGRID_API_KEY=SG...
```

### Problème: "Module 'api_routes' not found"
**Solution:** Vérifie que les fichiers sont dans `src/`
```bash
ls src/api_integration.py
ls src/api_routes.py
```

### Problème: Erreur d'import
**Solution:** Relance l'app
```bash
python app.py
```

---

## 📚 Documentation Complète

- **API_DOCUMENTATION.md** - Tous les endpoints en détail
- **README.md** - Vue d'ensemble du projet
- **.env.example** - Template de configuration

---

## 🚀 Déploiement sur Render

### 1. Ajouter les variables d'environnement

Dans Render Dashboard → Environment:

```
SECRET_KEY=votre-cle-secrete-production
SENDGRID_API_KEY=SG...
OPENAI_API_KEY=sk-...
```

### 2. Les services gratuits fonctionnent automatiquement
- ✅ Recherche web (Wikipedia, DuckDuckGo, PubMed)
- ✅ Chatbot de base
- ✅ Classification ML

### 3. Redémarrer le service
```bash
# Render redémarre automatiquement après changement d'env
```

---

## 💡 Recommandations

### Pour Débuter (Gratuit)
1. **Google Gemini** pour le LLM (gratuit!)
2. **Recherche web** (déjà inclus, gratuit)
3. Pas d'email au début

### Pour Production
1. **OpenAI GPT-4** ou **Claude** pour le LLM
2. **SendGrid** pour les emails (100/jour gratuit)
3. **Recherche web** activée
4. **Analyse d'images** si nécessaire

---

## 📞 Support

Si tu as des questions:
1. Vérifie `API_DOCUMENTATION.md`
2. Lance `python test_api_integration.py`
3. Consulte les logs de l'app

---

## ✅ Checklist de Démarrage

- [ ] Copier `.env.example` vers `.env`
- [ ] Configurer au moins une clé API (recommandé: Google Gemini gratuit)
- [ ] Lancer `python test_api_integration.py`
- [ ] Vérifier que les services sont actifs
- [ ] Démarrer l'app avec `python app.py`
- [ ] Tester avec `curl http://localhost:5000/api/services/status`
- [ ] Utiliser l'interface web sur `http://localhost:5000`

---

**🎉 Félicitations ! Ton assistant médical est maintenant enrichi avec des APIs externes !**

**Made with ❤️ pour un meilleur accès aux soins de santé**
