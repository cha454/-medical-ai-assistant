# 🚀 Démarrage Rapide - Configuration API

## ⚡ En 3 Minutes Chrono !

### Étape 1️⃣ : Obtenir une Clé API Google Gemini (GRATUIT)

```
🔗 Ouvre ce lien dans ton navigateur:
https://makersuite.google.com/app/apikey

👆 Clique sur "Create API Key"
📋 Copie la clé (commence par AIza...)
```

### Étape 2️⃣ : Configurer le Fichier .env

**Option A - Automatique (Windows):**
```bash
setup_api.bat
```

**Option B - Manuel:**
```bash
# Ouvrir le fichier
notepad .env

# Coller ta clé à la ligne:
GOOGLE_API_KEY=AIza_ta_cle_ici

# Sauvegarder (Ctrl+S)
```

### Étape 3️⃣ : Tester

```bash
python test_api_integration.py
```

**Résultat attendu:**
```
✅ Services opérationnels: 2/4
✓ LLM: Google Gemini activé
✓ Recherche Web: Activé
```

---

## 🎯 C'est Tout !

### Lancer l'Application

```bash
python app.py
```

### Accéder à l'Interface

```
🌐 http://localhost:5000
```

### Tester l'API

```bash
curl http://localhost:5000/api/services/status
```

---

## 📚 Guides Détaillés

| Guide | Description |
|-------|-------------|
| **OBTENIR_CLE_API.md** | 🔑 Comment obtenir toutes les clés API (avec captures) |
| **GUIDE_INTEGRATION_FR.md** | 📖 Guide complet d'intégration |
| **API_DOCUMENTATION.md** | 📋 Documentation de tous les endpoints |

---

## 🆘 Problème ?

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Invalid API Key"
- Vérifie que tu as copié toute la clé
- Pas d'espaces avant/après dans .env

### "LLM non disponible"
- Vérifie que .env contient bien ta clé
- Relance l'app: `python app.py`

---

## 💡 Astuce

Tu peux utiliser l'app **SANS clé API** !
- ✅ Chatbot de base fonctionne
- ✅ Classification ML fonctionne
- ✅ Recherche web fonctionne
- ❌ Pas de réponses IA avancées

---

**🎉 Bon développement !**
