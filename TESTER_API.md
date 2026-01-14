# 🧪 Tester l'API - Guide Rapide

## 🚀 Démarrer l'Application

```bash
python app.py
```

L'app sera sur : `http://localhost:5000`

---

## 📊 1. Vérifier le Statut des Services

### Commande
```bash
curl http://localhost:5000/api/services/status
```

### Résultat Attendu
```json
{
  "success": true,
  "services": {
    "llm": {"status": "unavailable", "provider": "N/A"},
    "email": {"status": "active", "provider": "sendgrid"},
    "web_search": {"status": "active", "provider": "N/A"},
    "image_analyzer": {"status": "unavailable", "provider": "N/A"}
  },
  "available_services": ["email", "web_search"],
  "total_active": 2
}
```

---

## 💬 2. Tester le Chat

### Commande
```bash
curl -X POST http://localhost:5000/api/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"J'ai de la fièvre et de la toux\", \"language\": \"fr\"}"
```

### Résultat Attendu
```json
{
  "response": "Je comprends que vous avez de la fièvre et de la toux...",
  "collected_symptoms": ["fièvre", "toux"],
  "session_id": "uuid...",
  "llm_active": false
}
```

---

## 🔍 3. Tester la Recherche Web

### Commande
```bash
curl -X POST http://localhost:5000/api/search/medical ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"diabète\", \"language\": \"fr\"}"
```

### Résultat Attendu
```json
{
  "success": true,
  "results": {
    "query": "diabète",
    "sources": [
      {
        "source": "Wikipedia",
        "title": "Diabète",
        "extract": "Le diabète est...",
        "url": "https://...",
        "reliability": "high"
      }
    ]
  }
}
```

---

## 📧 4. Tester l'Envoi d'Email

### Commande
```bash
curl -X POST http://localhost:5000/api/email/send ^
  -H "Content-Type: application/json" ^
  -d "{\"to_email\": \"noir1777@gmail.com\", \"subject\": \"Test API\", \"body\": \"Ceci est un test\"}"
```

### Résultat Attendu
```json
{
  "success": true,
  "message": "Email envoyé à noir1777@gmail.com via SendGrid"
}
```

---

## 🩺 5. Tester l'Analyse de Symptômes

### Commande
```bash
curl -X POST http://localhost:5000/api/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"symptoms\": [\"fièvre\", \"toux\", \"fatigue\"]}"
```

### Résultat Attendu
```json
{
  "emergency": false,
  "results": [
    {
      "disease": "grippe",
      "confidence": 85.5,
      "description": "Infection virale...",
      "severity": "modérée"
    }
  ]
}
```

---

## 💊 6. Tester la Vérification de Médicaments

### Commande
```bash
curl -X POST http://localhost:5000/api/drugs/check ^
  -H "Content-Type: application/json" ^
  -d "{\"drugs\": [\"ibuprofène\", \"aspirine\"]}"
```

### Résultat Attendu
```json
{
  "safe": false,
  "interactions": [
    {
      "drug1": "ibuprofène",
      "drug2": "aspirine",
      "severity": "modérée à élevée",
      "warning": "Interaction détectée..."
    }
  ]
}
```

---

## 🌟 7. Tester le Chat Enrichi (avec recherche web)

### Commande
```bash
curl -X POST http://localhost:5000/api/enhanced/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Qu'est-ce que le diabète?\", \"language\": \"fr\", \"use_web_search\": true}"
```

### Résultat Attendu
```json
{
  "success": true,
  "response": "Le diabète est une maladie chronique...",
  "source": "chatbot",
  "web_search": "📚 Informations trouvées sur le web...",
  "sources": ["chatbot", "web"]
}
```

---

## 🎯 8. Tester le Diagnostic Enrichi

### Commande
```bash
curl -X POST http://localhost:5000/api/enhanced/diagnose ^
  -H "Content-Type: application/json" ^
  -d "{\"symptoms\": [\"fièvre\", \"toux\"], \"language\": \"fr\"}"
```

### Résultat Attendu
```json
{
  "success": true,
  "emergency": false,
  "results": [...],
  "web_info": "📚 Informations trouvées...",
  "sources": ["ml_classifier", "web"]
}
```

---

## 🧪 Test avec Python

Créez un fichier `test_api.py` :

```python
import requests

BASE_URL = "http://localhost:5000"

# 1. Vérifier le statut
response = requests.get(f"{BASE_URL}/api/services/status")
print("Statut:", response.json())

# 2. Chat
response = requests.post(f"{BASE_URL}/api/chat", json={
    "message": "J'ai mal à la tête",
    "language": "fr"
})
print("Chat:", response.json()['response'])

# 3. Recherche web
response = requests.post(f"{BASE_URL}/api/search/medical", json={
    "query": "hypertension",
    "language": "fr"
})
print("Recherche:", response.json())

# 4. Email (si configuré)
response = requests.post(f"{BASE_URL}/api/email/send", json={
    "to_email": "test@example.com",
    "subject": "Test",
    "body": "Message de test"
})
print("Email:", response.json())
```

Lancez :
```bash
python test_api.py
```

---

## 📖 Documentation Complète

Pour tous les endpoints disponibles, consultez : **API_DOCUMENTATION.md**

---

## 🎉 Résumé

### Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/health` | GET | Santé de l'API |
| `/api/services/status` | GET | Statut des services |
| `/api/chat` | POST | Chat de base |
| `/api/enhanced/chat` | POST | Chat enrichi |
| `/api/analyze` | POST | Analyse symptômes |
| `/api/enhanced/diagnose` | POST | Diagnostic enrichi |
| `/api/drugs/check` | POST | Vérification médicaments |
| `/api/email/send` | POST | Envoi email |
| `/api/search/medical` | POST | Recherche web |

---

**🚀 Ton API est prête à être testée !**
