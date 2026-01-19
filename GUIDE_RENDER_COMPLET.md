# 🚀 Guide Complet de Déploiement sur Render

## 📋 Prérequis

Avant de déployer, assurez-vous d'avoir :
- ✅ Un compte GitHub avec votre code pushé
- ✅ Un compte Render (gratuit sur https://render.com)
- ✅ Les clés API nécessaires (voir ci-dessous)

---

## 🔑 Obtenir les Clés API

### 1. OpenWeather (Météo) - GRATUIT ⭐

**Pourquoi ?** Pour afficher la météo dans le chat

**Comment obtenir :**
1. Allez sur https://openweathermap.org/api
2. Cliquez sur "Sign Up" (créer un compte)
3. Confirmez votre email
4. Allez dans "API Keys" dans votre profil
5. Copiez la clé par défaut (ou créez-en une nouvelle)

**Limite gratuite :** 1000 appels/jour (largement suffisant)

---

### 2. Google Gemini (IA) - GRATUIT ⭐ RECOMMANDÉ

**Pourquoi ?** Pour les réponses intelligentes et recherches poussées

**Comment obtenir :**
1. Allez sur https://makersuite.google.com/app/apikey
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez la clé (commence par `AIza...`)

**Limite gratuite :** Très généreuse, parfait pour commencer

---

### 3. OpenAI (IA) - PAYANT 💰 (Optionnel)

**Pourquoi ?** Alternative plus puissante à Gemini

**Comment obtenir :**
1. Allez sur https://platform.openai.com/api-keys
2. Créez un compte
3. Ajoutez un moyen de paiement
4. Créez une clé API
5. Copiez la clé (commence par `sk-...`)

**Coût :** ~$0.002 par 1000 tokens (très économique avec gpt-4o-mini)

---

### 4. SendGrid (Email) - GRATUIT (Optionnel)

**Pourquoi ?** Pour envoyer des résumés par email

**Comment obtenir :**
1. Allez sur https://signup.sendgrid.com
2. Créez un compte gratuit
3. Vérifiez votre email
4. Allez dans Settings → API Keys
5. Créez une clé avec accès "Full Access"
6. Vérifiez votre email expéditeur dans Sender Authentication

**Limite gratuite :** 100 emails/jour

---

## 🎯 Déploiement sur Render - Étape par Étape

### Étape 1 : Créer le Service Web

1. Connectez-vous sur https://dashboard.render.com
2. Cliquez sur "New +" → "Web Service"
3. Connectez votre dépôt GitHub
4. Sélectionnez votre repository `medical-ai-assistant`

### Étape 2 : Configuration du Service

Remplissez les champs :

```
Name: medical-ai-assistant
Region: Frankfurt (EU Central) ou Oregon (US West)
Branch: main
Root Directory: (laissez vide)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Étape 3 : Plan Gratuit

- Sélectionnez "Free" (gratuit)
- Notez que le service s'endort après 15 min d'inactivité
- Il redémarre automatiquement à la première requête

### Étape 4 : Variables d'Environnement

Cliquez sur "Advanced" puis ajoutez ces variables :

#### OBLIGATOIRES

```bash
# Clé secrète Flask (générez-en une unique)
SECRET_KEY=votre-secret-key-tres-securise-changez-moi

# Port (Render l'utilise automatiquement)
PORT=10000
```

#### MÉTÉO (Recommandé)

```bash
OPENWEATHER_API_KEY=votre-cle-openweather-ici
```

#### IA - Choisissez AU MOINS UNE option

**Option 1 : Google Gemini (GRATUIT - Recommandé)**
```bash
GOOGLE_API_KEY=votre-cle-gemini-ici
```

**Option 2 : OpenAI (Payant)**
```bash
OPENAI_API_KEY=sk-votre-cle-openai-ici
```

**Option 3 : Groq (GRATUIT)**
```bash
GROQ_API_KEY=votre-cle-groq-ici
```

#### EMAIL (Optionnel)

```bash
SENDGRID_API_KEY=votre-cle-sendgrid
SENDGRID_FROM_EMAIL=votre-email-verifie@exemple.com
```

### Étape 5 : Déployer

1. Cliquez sur "Create Web Service"
2. Attendez 5-10 minutes (première installation)
3. Surveillez les logs en temps réel

---

## ✅ Vérification du Déploiement

### 1. Vérifier les Logs

Dans le dashboard Render, onglet "Logs", vous devriez voir :

```
✓ LLM Provider initialisé: Google Gemini
✓ Service météo OpenWeather initialisé
✓ Service email activé
Entraînement du modèle...
Modèle prêt!
```

### 2. Tester l'Application

Cliquez sur l'URL de votre service (ex: `https://medical-ai-assistant.onrender.com`)

Vous devriez voir la page d'accueil de l'assistant médical.

### 3. Tester les Fonctionnalités

Dans le chat, testez :

```
✅ "Bonjour" → Doit répondre avec l'IA
✅ "Quelle est la météo à Paris ?" → Doit afficher la météo
✅ "Fais une recherche poussée sur le diabète" → Doit faire une analyse détaillée
✅ "Quels sont les symptômes de la grippe ?" → Doit donner des infos médicales
```

---

## 🐛 Dépannage

### Erreur : "Application failed to respond"

**Cause :** Le service n'a pas démarré correctement

**Solutions :**
1. Vérifiez les logs pour voir l'erreur exacte
2. Vérifiez que `gunicorn` est dans `requirements.txt`
3. Vérifiez que `app.py` existe à la racine

### Erreur : "Module not found"

**Cause :** Dépendance manquante

**Solutions :**
1. Vérifiez que toutes les dépendances sont dans `requirements.txt`
2. Redéployez en cliquant sur "Manual Deploy" → "Clear build cache & deploy"

### La météo ne fonctionne pas

**Cause :** Clé API manquante ou invalide

**Solutions :**
1. Vérifiez que `OPENWEATHER_API_KEY` est bien configurée
2. Vérifiez que la clé est active (peut prendre 10 min après création)
3. Testez la clé sur https://openweathermap.org/api

### L'IA ne répond pas

**Cause :** Aucune clé LLM configurée

**Solutions :**
1. Ajoutez au moins `GOOGLE_API_KEY` (gratuit)
2. Vérifiez que la clé est valide
3. Regardez les logs pour voir quel provider est actif

### Service lent au démarrage

**Cause :** Plan gratuit - le service s'endort après 15 min

**Solutions :**
1. C'est normal sur le plan gratuit
2. Le service redémarre en ~30 secondes à la première requête
3. Passez au plan payant ($7/mois) pour un service toujours actif

---

## 🔄 Mises à Jour

### Déploiement Automatique

Render redéploie automatiquement à chaque push sur `main` :

```bash
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin main
```

Render détecte le push et redéploie automatiquement (2-5 min).

### Déploiement Manuel

Dans le dashboard Render :
1. Allez dans votre service
2. Cliquez sur "Manual Deploy"
3. Sélectionnez "Clear build cache & deploy" si problème

---

## 📊 Monitoring

### Logs en Temps Réel

Dans Render → Logs, vous pouvez :
- Voir les requêtes en temps réel
- Détecter les erreurs
- Surveiller les performances

### Métriques

Dans Render → Metrics, vous voyez :
- CPU usage
- Memory usage
- Request count
- Response time

---

## 💰 Coûts Estimés

### Plan Gratuit (Recommandé pour débuter)

```
Render Web Service: GRATUIT
OpenWeather API: GRATUIT (1000 appels/jour)
Google Gemini: GRATUIT
SendGrid: GRATUIT (100 emails/jour)

TOTAL: 0€/mois 🎉
```

### Plan Payant (Pour production)

```
Render Web Service: $7/mois (toujours actif)
OpenAI API: ~$5-20/mois (selon usage)
SendGrid: GRATUIT ou $15/mois (40k emails)

TOTAL: ~$12-42/mois
```

---

## 🎯 Checklist Finale

Avant de partager votre application :

- [ ] ✅ Service déployé et accessible
- [ ] ✅ Météo fonctionne
- [ ] ✅ IA répond correctement
- [ ] ✅ Recherches poussées fonctionnent
- [ ] ✅ Interface responsive (mobile/desktop)
- [ ] ✅ Pas d'erreurs dans les logs
- [ ] ✅ Variables d'environnement sécurisées
- [ ] ✅ `.env` dans `.gitignore`

---

## 🎉 Félicitations !

Votre Assistant Médical IA est maintenant en ligne ! 🚀

**URL de votre app :** `https://votre-service.onrender.com`

**Partagez-la avec :**
- Vos amis et famille
- Votre portfolio
- Les réseaux sociaux

---

## 📞 Support

**Problèmes ?**
- Consultez les logs Render
- Vérifiez `NOUVELLES_FONCTIONNALITES.md`
- Testez localement avec `python test_nouvelles_fonctionnalites.py`

**Questions ?**
- Documentation Render : https://render.com/docs
- Documentation OpenWeather : https://openweathermap.org/api
- Documentation OpenAI : https://platform.openai.com/docs

---

**Bon déploiement ! 🚀**
