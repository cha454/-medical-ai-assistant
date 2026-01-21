# 🚀 Commandes de Déploiement - Tous les Hébergeurs

## 📋 GUIDE RAPIDE

Ce fichier contient toutes les commandes nécessaires pour déployer sur chaque hébergeur.

---

## 🥇 RAILWAY (RECOMMANDÉ)

### Déploiement via Interface Web (5 minutes)

**Aucune commande nécessaire !** Tout se fait via l'interface web.

**Étapes :**
1. https://railway.app → Login with GitHub
2. New Project → Deploy from GitHub repo
3. Sélectionne `medical-ai-assistant`
4. Variables → Ajoute tes clés API
5. Settings → Generate Domain
6. C'est tout ! 🎉

### Déploiement via CLI (optionnel)

```bash
# 1. Installer Railway CLI
npm i -g @railway/cli

# Ou avec Homebrew (Mac/Linux)
brew install railway

# 2. Login
railway login

# 3. Initialiser le projet
cd medical-ai-assistant
railway init

# 4. Lier au projet GitHub
railway link

# 5. Ajouter les variables d'environnement
railway variables set GROQ_API_KEY=ta_cle
railway variables set GOOGLE_API_KEY=ta_cle
railway variables set NEWS_API_KEY=ta_cle
railway variables set OPENWEATHER_API_KEY=ta_cle
railway variables set SENDGRID_API_KEY=ta_cle
railway variables set SENDGRID_FROM_EMAIL=ton_email
railway variables set SECRET_KEY=ta_secret_key

# 6. Déployer
railway up

# 7. Ouvrir l'app
railway open
```

### Commandes utiles Railway

```bash
# Voir les logs
railway logs

# Voir les variables
railway variables

# Redémarrer l'app
railway restart

# Voir le statut
railway status

# Ouvrir le dashboard
railway open
```

---

## 🥈 FLY.IO

### Installation Fly CLI

**Windows (PowerShell) :**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux :**
```bash
curl -L https://fly.io/install.sh | sh
```

### Déploiement complet

```bash
# 1. Login
fly auth login

# 2. Aller dans le dossier
cd medical-ai-assistant

# 3. Créer l'app (interactive)
fly launch
# Répondre aux questions :
# - App name: medical-ai-assistant
# - Region: Paris (cdg) ou proche de toi
# - PostgreSQL: No (on utilise SQLite)
# - Redis: No

# 4. Ajouter les variables d'environnement
fly secrets set GROQ_API_KEY=ta_cle
fly secrets set GOOGLE_API_KEY=ta_cle
fly secrets set NEWS_API_KEY=ta_cle
fly secrets set OPENWEATHER_API_KEY=ta_cle
fly secrets set SENDGRID_API_KEY=ta_cle
fly secrets set SENDGRID_FROM_EMAIL=ton_email
fly secrets set SECRET_KEY=ta_secret_key

# 5. Déployer
fly deploy

# 6. Ouvrir l'app
fly open

# 7. Voir les logs
fly logs
```

### Fichier fly.toml (créé automatiquement)

```toml
app = "medical-ai-assistant"
primary_region = "cdg"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

### Commandes utiles Fly.io

```bash
# Voir les logs en temps réel
fly logs -a medical-ai-assistant

# Voir le statut
fly status

# Redémarrer l'app
fly apps restart medical-ai-assistant

# Voir les secrets
fly secrets list

# SSH dans l'app
fly ssh console

# Voir les métriques
fly dashboard metrics

# Supprimer l'app
fly apps destroy medical-ai-assistant
```

---

## 🥉 KOYEB

### Déploiement via Interface Web (5 minutes)

**Aucune commande nécessaire !** Tout se fait via l'interface web.

**Étapes :**
1. https://www.koyeb.com → Sign up with GitHub
2. Create App → GitHub
3. Sélectionne `medical-ai-assistant`
4. Builder: Buildpack
5. Run command: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Port: 8000
7. Environment variables → Ajoute tes clés API
8. Deploy ! 🎉

### Déploiement via CLI (optionnel)

```bash
# 1. Installer Koyeb CLI
# Windows (Scoop)
scoop install koyeb

# Mac/Linux
brew install koyeb-cli

# Ou télécharger depuis https://github.com/koyeb/koyeb-cli/releases

# 2. Login
koyeb login

# 3. Créer l'app
koyeb app create medical-ai-assistant

# 4. Créer le service
koyeb service create medical-ai-assistant \
  --app medical-ai-assistant \
  --git github.com/TON_USERNAME/medical-ai-assistant \
  --git-branch main \
  --ports 8000:http \
  --routes /:8000 \
  --env GROQ_API_KEY=ta_cle \
  --env GOOGLE_API_KEY=ta_cle \
  --env NEWS_API_KEY=ta_cle \
  --env OPENWEATHER_API_KEY=ta_cle \
  --env SENDGRID_API_KEY=ta_cle \
  --env SENDGRID_FROM_EMAIL=ton_email \
  --env SECRET_KEY=ta_secret_key

# 5. Voir les logs
koyeb service logs medical-ai-assistant/medical-ai-assistant
```

### Commandes utiles Koyeb

```bash
# Voir les apps
koyeb app list

# Voir les services
koyeb service list

# Voir les logs
koyeb service logs medical-ai-assistant/medical-ai-assistant

# Redéployer
koyeb service redeploy medical-ai-assistant/medical-ai-assistant

# Supprimer
koyeb service delete medical-ai-assistant/medical-ai-assistant
koyeb app delete medical-ai-assistant
```

---

## 📦 RENDER (TON HÉBERGEUR ACTUEL)

### Déploiement via Interface Web

**Étapes :**
1. https://render.com → Dashboard
2. New → Web Service
3. Connect GitHub → Sélectionne ton repo
4. Name: medical-ai-assistant
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`
7. Environment variables → Ajoute tes clés API
8. Create Web Service

### Commandes utiles (via Dashboard)

```
# Pas de CLI officielle pour Render
# Tout se fait via l'interface web :

1. Manual Deploy → Deploy latest commit
2. Logs → Voir les logs
3. Shell → Accéder au terminal
4. Environment → Gérer les variables
5. Settings → Configurer l'app
```

---

## 🔧 FICHIERS DE CONFIGURATION

### 1. Procfile (pour tous les hébergeurs)

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

### 2. railway.json (pour Railway)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 3. fly.toml (pour Fly.io)

Créé automatiquement par `fly launch`, mais tu peux le personnaliser :

```toml
app = "medical-ai-assistant"
primary_region = "cdg"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### 4. render.yaml (pour Render)

```yaml
services:
  - type: web
    name: medical-ai-assistant
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: GOOGLE_API_KEY
        sync: false
      - key: NEWS_API_KEY
        sync: false
      - key: OPENWEATHER_API_KEY
        sync: false
      - key: SENDGRID_API_KEY
        sync: false
      - key: SENDGRID_FROM_EMAIL
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

---

## 🔐 VARIABLES D'ENVIRONNEMENT

### Liste complète des variables à configurer :

```bash
# LLM (au moins une)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Services optionnels
NEWS_API_KEY=7b17ac517ec1404cb71b1a56ce47970c
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=ton_email@gmail.com

# Sécurité (obligatoire)
SECRET_KEY=une_cle_secrete_aleatoire_tres_longue_et_complexe

# Backups (optionnel)
GROQ_API_KEY_BACKUP=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY_BACKUP=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY_BACKUP=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Générer une SECRET_KEY :

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# Ou utilise le fichier fourni
python generate_secret_key.py
```

---

## 🧪 TESTER LE DÉPLOIEMENT

### 1. Vérifier que l'app démarre

```bash
# Railway
railway logs

# Fly.io
fly logs

# Koyeb
koyeb service logs medical-ai-assistant/medical-ai-assistant

# Render
# Via Dashboard → Logs
```

**Tu devrais voir :**
```
✓ LLM Provider initialisé: groq
✓ LLM activé: Groq (Llama 3.1)
✓ Email: SendGrid activé
✓ Service météo OpenWeather activé
✓ Service actualités activé
✓ Base de données initialisée
```

### 2. Tester l'URL

```bash
# Ouvrir l'app
# Railway
railway open

# Fly.io
fly open

# Koyeb / Render
# Copie l'URL depuis le dashboard
```

### 3. Tester les fonctionnalités

```bash
# Test API chat
curl -X POST https://ton-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour"}'

# Test page d'accueil
curl https://ton-url.com/

# Test santé
curl https://ton-url.com/health
```

---

## 🆘 DÉPANNAGE

### Problème : Build échoue

```bash
# Vérifier les logs de build
railway logs  # Railway
fly logs      # Fly.io

# Vérifier requirements.txt
cat requirements.txt

# Vérifier Python version
python --version  # Doit être 3.10+
```

### Problème : App ne démarre pas

```bash
# Vérifier les variables d'environnement
railway variables  # Railway
fly secrets list   # Fly.io

# Vérifier que SECRET_KEY existe
# Vérifier que au moins une clé LLM existe (GROQ ou GOOGLE)
```

### Problème : Port incorrect

```bash
# Vérifier que l'app utilise $PORT
# Dans app.py, ligne finale :
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
```

---

## 📝 RÉSUMÉ DES COMMANDES

### Railway (Recommandé - Interface Web)
```bash
# Aucune commande nécessaire !
# Tout via https://railway.app
```

### Fly.io (CLI)
```bash
fly auth login
fly launch
fly secrets set KEY=value
fly deploy
fly logs
```

### Koyeb (Interface Web)
```bash
# Aucune commande nécessaire !
# Tout via https://www.koyeb.com
```

### Render (Interface Web)
```bash
# Aucune commande nécessaire !
# Tout via https://render.com
```

---

## 🎯 RECOMMANDATION

**Pour toi : RAILWAY via Interface Web**

**Pourquoi ?**
- ✅ Aucune commande à taper
- ✅ Interface simple et moderne
- ✅ 8 GB RAM (16× plus que Render)
- ✅ Déploiement en 5 minutes
- ✅ Toujours actif (pas de sleep)

**Suis le guide : `MIGRATION_RAILWAY.md` 🚀**
