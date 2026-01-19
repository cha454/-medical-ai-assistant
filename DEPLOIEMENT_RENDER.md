# 🚀 Guide de déploiement sur Render

## ✅ Votre application est prête !

Tous les fichiers nécessaires sont en place. Suivez ce guide étape par étape.

## 📋 Prérequis

- Un compte GitHub (gratuit)
- Un compte Render (gratuit) : https://render.com/
- Votre clé API GLM-4 (ou Google Gemini)

## 🔧 Étape 1 : Préparer le dépôt GitHub

### 1.1 Créer un fichier .gitignore

Créez un fichier `.gitignore` à la racine du projet :

```
# Environnement Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Variables d'environnement (IMPORTANT!)
.env

# Base de données locale
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

### 1.2 Créer un dépôt GitHub

1. Allez sur https://github.com/new
2. Nommez votre dépôt : `medical-ai-assistant`
3. Choisissez "Public" ou "Private"
4. **NE PAS** initialiser avec README (vous en avez déjà un)
5. Cliquez "Create repository"

### 1.3 Pousser votre code

Dans votre terminal (dans le dossier `medical-ai-assistant`) :

```bash
git init
git add .
git commit -m "Initial commit - Medical AI Assistant with GLM-4"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/medical-ai-assistant.git
git push -u origin main
```

**⚠️ IMPORTANT** : Vérifiez que le fichier `.env` n'est PAS dans GitHub !

## 🌐 Étape 2 : Déployer sur Render

### 2.1 Créer un nouveau Web Service

1. Allez sur https://dashboard.render.com/
2. Cliquez sur "New +" → "Web Service"
3. Connectez votre compte GitHub si ce n'est pas fait
4. Sélectionnez votre dépôt `medical-ai-assistant`
5. Cliquez "Connect"

### 2.2 Configuration du service

Remplissez les champs suivants :

**Informations de base :**
- **Name** : `medical-ai-assistant` (ou votre choix)
- **Region** : Choisissez la plus proche (Europe West pour la France)
- **Branch** : `main`
- **Root Directory** : Laissez vide
- **Runtime** : `Python 3`

**Build & Deploy :**
- **Build Command** : 
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command** :
  ```bash
  gunicorn app:app
  ```

**Plan :**
- Sélectionnez **"Free"** (gratuit, 750h/mois)

### 2.3 Variables d'environnement

Cliquez sur "Advanced" puis "Add Environment Variable".

Ajoutez ces variables **UNE PAR UNE** :

#### Variables obligatoires :

| Key | Value | Description |
|-----|-------|-------------|
| `SECRET_KEY` | `votre-cle-secrete-aleatoire-123` | Clé secrète Flask (changez-la!) |
| `FLASK_ENV` | `production` | Mode production |
| `GLM_API_KEY` | `votre_cle_glm4` | Votre clé API GLM-4 |

#### Variables optionnelles :

| Key | Value | Description |
|-----|-------|-------------|
| `GOOGLE_API_KEY` | `votre_cle_google` | Backup si GLM-4 échoue |
| `SENDGRID_API_KEY` | `votre_cle_sendgrid` | Pour les emails (optionnel) |
| `SENDGRID_FROM_EMAIL` | `votre@email.com` | Email expéditeur |

**💡 Astuce** : Pour générer une SECRET_KEY sécurisée :
```python
import secrets
print(secrets.token_hex(32))
```

### 2.4 Lancer le déploiement

1. Cliquez sur "Create Web Service"
2. Render va :
   - Cloner votre dépôt
   - Installer les dépendances
   - Démarrer l'application
3. Attendez 5-10 minutes (première fois)

### 2.5 Vérifier le déploiement

Une fois le déploiement terminé :

1. Vous verrez "Live" en vert
2. Cliquez sur l'URL (ex: `https://medical-ai-assistant.onrender.com`)
3. Testez l'endpoint de santé : `https://votre-url.onrender.com/api/health`

Vous devriez voir :
```json
{
  "status": "healthy",
  "message": "Assistant Médical IA opérationnel",
  "version": "2.0.0"
}
```

## 🎯 Étape 3 : Tester votre API

### Test 1 : Page d'accueil
```
https://votre-url.onrender.com/
```

### Test 2 : Interface de chat
```
https://votre-url.onrender.com/chat
```

### Test 3 : API Chat (avec curl)
```bash
curl -X POST https://votre-url.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour, quels sont les symptômes de la grippe?", "language": "fr"}'
```

### Test 4 : Vérifier le provider LLM
Regardez les logs dans Render :
- Allez dans "Logs"
- Cherchez : `✓ LLM Provider initialisé: glm`

## 🔄 Étape 4 : Mises à jour

Pour mettre à jour votre application :

```bash
# Faites vos modifications
git add .
git commit -m "Description des changements"
git push
```

Render redéploiera automatiquement ! 🎉

## ⚙️ Configuration avancée

### Augmenter les performances

Dans Render, vous pouvez :
- Passer au plan payant pour plus de RAM/CPU
- Activer "Auto-Deploy" (déjà activé par défaut)
- Configurer des "Health Check Paths" : `/api/health`

### Ajouter un domaine personnalisé

1. Dans Render, allez dans "Settings"
2. Section "Custom Domain"
3. Ajoutez votre domaine
4. Configurez les DNS selon les instructions

### Monitoring

Render fournit :
- **Logs en temps réel** : Onglet "Logs"
- **Métriques** : CPU, RAM, requêtes
- **Alertes** : Configurables par email

## 🐛 Dépannage

### Erreur : "Build failed"

**Problème** : Dépendances manquantes ou incompatibles

**Solution** :
1. Vérifiez `requirements.txt`
2. Testez localement : `pip install -r requirements.txt`
3. Regardez les logs de build dans Render

### Erreur : "Application failed to start"

**Problème** : Erreur dans le code ou variables d'environnement manquantes

**Solution** :
1. Vérifiez les logs dans Render
2. Assurez-vous que `GLM_API_KEY` est définie
3. Testez localement : `python app.py`

### Erreur : "Service Unavailable"

**Problème** : L'application s'est arrêtée

**Solution** :
1. Regardez les logs pour voir l'erreur
2. Redémarrez le service : "Manual Deploy" → "Clear build cache & deploy"

### L'application est lente au premier chargement

**Normal !** Le plan gratuit de Render met l'application en veille après 15 minutes d'inactivité.
- Premier chargement : 30-60 secondes
- Chargements suivants : instantanés
- Solution : Passer au plan payant ($7/mois) pour éviter la mise en veille

### GLM-4 ne fonctionne pas

**Vérifications** :
1. La clé API est-elle correcte dans les variables d'environnement ?
2. Avez-vous du quota restant sur https://open.bigmodel.cn/ ?
3. Regardez les logs : cherchez "GLM-4 Error"

**Fallback** : Ajoutez `GOOGLE_API_KEY` comme backup

## 📊 Limites du plan gratuit

| Ressource | Limite |
|-----------|--------|
| Heures/mois | 750h (suffisant pour 1 service 24/7) |
| RAM | 512 MB |
| CPU | Partagé |
| Bande passante | Illimitée |
| Builds | Illimités |
| Mise en veille | Après 15 min d'inactivité |

## 🎉 Félicitations !

Votre Assistant Médical IA avec GLM-4 est maintenant en ligne !

**URL de votre application** : `https://votre-nom.onrender.com`

### Prochaines étapes

- ✅ Testez toutes les fonctionnalités
- ✅ Partagez l'URL avec vos utilisateurs
- ✅ Surveillez les logs et les performances
- ✅ Ajoutez des fonctionnalités (voir README.md)

## 📚 Ressources

- **Documentation Render** : https://render.com/docs
- **Support Render** : https://render.com/support
- **Documentation GLM-4** : https://open.bigmodel.cn/dev/api
- **Votre dashboard** : https://dashboard.render.com/

---

**Besoin d'aide ?** Consultez les logs dans Render ou ouvrez une issue sur GitHub.
