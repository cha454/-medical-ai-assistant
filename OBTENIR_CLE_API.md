# 🔑 Comment Obtenir une Clé API (Guide Visuel)

## 🎯 Option 1: Google Gemini (RECOMMANDÉ - GRATUIT!)

### ✅ Avantages
- ✅ **100% GRATUIT**
- ✅ 60 requêtes par minute
- ✅ Très performant
- ✅ Pas de carte bancaire requise
- ✅ Configuration en 2 minutes

### 📝 Étapes

#### 1. Aller sur le site
🔗 **https://makersuite.google.com/app/apikey**

#### 2. Se connecter avec ton compte Google
- Utilise ton compte Gmail existant
- Ou crée un nouveau compte Google

#### 3. Créer une clé API
- Clique sur le bouton **"Create API Key"** (bleu)
- Ou **"Get API Key"**

#### 4. Choisir un projet
- Sélectionne un projet existant
- Ou clique **"Create API key in new project"**

#### 5. Copier la clé
- La clé ressemble à : `AIzaSyC...` (39 caractères)
- Clique sur l'icône 📋 pour copier

#### 6. Coller dans .env
Ouvre le fichier `.env` et colle ta clé :
```env
GOOGLE_API_KEY=AIzaSyC_ta_cle_ici
```

#### 7. Sauvegarder et tester
```bash
python test_api_integration.py
```

---

## 💰 Option 2: OpenAI (Payant mais puissant)

### 💵 Prix
- GPT-3.5: ~$0.002 par 1000 tokens
- GPT-4: ~$0.03 par 1000 tokens
- Nécessite une carte bancaire

### 📝 Étapes

#### 1. Créer un compte
🔗 **https://platform.openai.com/signup**

#### 2. Ajouter un moyen de paiement
- Menu → **Billing** → **Add payment method**
- Ajoute ta carte bancaire

#### 3. Créer une clé API
- Menu → **API Keys**
- Clique **"Create new secret key"**
- Donne un nom : "Medical AI Assistant"

#### 4. Copier la clé
- La clé ressemble à : `sk-proj-...` (51+ caractères)
- ⚠️ **IMPORTANT**: Copie-la maintenant, tu ne pourras plus la voir !

#### 5. Coller dans .env
```env
OPENAI_API_KEY=sk-proj-ta_cle_ici
```

---

## 🤖 Option 3: Anthropic Claude (Payant)

### 💵 Prix
- Claude 3 Haiku: ~$0.0008 par 1000 tokens
- Claude 3 Sonnet: ~$0.003 par 1000 tokens

### 📝 Étapes

#### 1. Créer un compte
🔗 **https://console.anthropic.com/**

#### 2. Ajouter des crédits
- Menu → **Billing**
- Minimum $5

#### 3. Créer une clé
- Menu → **API Keys**
- **"Create Key"**

#### 4. Copier et coller
```env
ANTHROPIC_API_KEY=sk-ant-ta_cle_ici
```

---

## 🚀 Option 4: Mistral AI (Payant - Français)

### 💵 Prix
- Mistral Small: ~$0.001 par 1000 tokens
- Mistral Medium: ~$0.0027 par 1000 tokens

### 📝 Étapes

#### 1. Créer un compte
🔗 **https://console.mistral.ai/**

#### 2. Ajouter des crédits
- Menu → **Billing**

#### 3. Créer une clé
- Menu → **API Keys**
- **"Create new key"**

#### 4. Copier et coller
```env
MISTRAL_API_KEY=ta_cle_ici
```

---

## 📧 BONUS: SendGrid (Email - GRATUIT)

### ✅ Avantages
- ✅ **100 emails/jour GRATUIT**
- ✅ Fonctionne sur Render
- ✅ Pas de carte bancaire pour le plan gratuit

### 📝 Étapes

#### 1. Créer un compte
🔗 **https://signup.sendgrid.com/**

#### 2. Vérifier ton email
- Clique sur le lien dans l'email reçu

#### 3. Créer une clé API
- Menu → **Settings** → **API Keys**
- **"Create API Key"**
- Nom: "Medical AI Assistant"
- Permissions: **"Full Access"**

#### 4. Copier la clé
- La clé ressemble à : `SG.xxx...`
- ⚠️ Copie-la maintenant !

#### 5. Coller dans .env
```env
SENDGRID_API_KEY=SG.ta_cle_ici
```

#### 6. Vérifier l'expéditeur
- Menu → **Settings** → **Sender Authentication**
- Ajoute ton email comme expéditeur vérifié

---

## ✅ Vérification de la Configuration

### 1. Vérifier que .env existe
```bash
dir .env
```

### 2. Tester les intégrations
```bash
python test_api_integration.py
```

### 3. Résultat attendu
```
✅ Services opérationnels: 2/4
✓ LLM: Google Gemini activé
✓ Recherche Web: Activé
⚠️ Email: Non configuré
⚠️ Analyse d'Images: Non disponible
```

### 4. Lancer l'application
```bash
python app.py
```

### 5. Tester l'API
```bash
curl http://localhost:5000/api/services/status
```

---

## 🔒 Sécurité

### ⚠️ IMPORTANT

1. **NE JAMAIS** commiter le fichier `.env` sur GitHub
2. Le fichier `.gitignore` doit contenir `.env`
3. Utilise `.env.example` pour partager la structure

### Vérifier .gitignore
```bash
type .gitignore | findstr .env
```

Si `.env` n'est pas dans `.gitignore`, ajoute-le :
```bash
echo .env >> .gitignore
```

---

## 🆘 Problèmes Courants

### Problème: "Invalid API Key"
**Solution:**
- Vérifie que tu as bien copié toute la clé
- Pas d'espaces avant/après
- La clé est active (pas révoquée)

### Problème: "Quota exceeded"
**Solution:**
- Google Gemini: Attends 1 minute (limite: 60/min)
- OpenAI: Vérifie ton crédit sur platform.openai.com

### Problème: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problème: Le fichier .env n'est pas lu
**Solution:**
- Vérifie qu'il est à la racine du projet
- Relance l'application
```bash
python app.py
```

---

## 📊 Comparaison des Options

| Provider | Prix | Gratuit | Performance | Recommandé |
|----------|------|---------|-------------|------------|
| **Google Gemini** | Gratuit | ✅ Oui | ⭐⭐⭐⭐ | ✅ **OUI** |
| OpenAI GPT-4 | $0.03/1K | ❌ Non | ⭐⭐⭐⭐⭐ | Pour production |
| OpenAI GPT-3.5 | $0.002/1K | ❌ Non | ⭐⭐⭐⭐ | Bon rapport qualité/prix |
| Claude 3 | $0.003/1K | ❌ Non | ⭐⭐⭐⭐⭐ | Très bon |
| Mistral | $0.001/1K | ❌ Non | ⭐⭐⭐ | Français |

---

## 🎯 Recommandation Finale

### Pour Débuter (Gratuit)
```env
GOOGLE_API_KEY=ta_cle_ici
```
✅ Parfait pour tester et développer

### Pour Production (Payant)
```env
OPENAI_API_KEY=ta_cle_ici
SENDGRID_API_KEY=ta_cle_ici
```
✅ Meilleure qualité + emails

---

## 📞 Besoin d'Aide ?

1. Vérifie `GUIDE_INTEGRATION_FR.md`
2. Lance `python test_api_integration.py`
3. Consulte `API_DOCUMENTATION.md`

---

**🎉 Bon courage ! Tu vas y arriver !**
