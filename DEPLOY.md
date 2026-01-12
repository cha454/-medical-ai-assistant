# Guide de déploiement sur Render

## Étapes pour déployer votre Assistant Médical IA sur Render

### 1. Préparer votre code

✅ Tous les fichiers nécessaires sont déjà créés:
- `app.py` - Application Flask
- `requirements.txt` - Dépendances Python
- `render.yaml` - Configuration Render
- `templates/index.html` - Interface web

### 2. Créer un dépôt Git

```bash
cd medical-ai-assistant
git init
git add .
git commit -m "Initial commit - Assistant Medical IA"
```

### 3. Pousser sur GitHub

```bash
# Créez un nouveau repo sur GitHub, puis:
git remote add origin https://github.com/VOTRE-USERNAME/medical-ai-assistant.git
git branch -M main
git push -u origin main
```

### 4. Déployer sur Render

1. Allez sur https://render.com
2. Connectez-vous (ou créez un compte gratuit)
3. Cliquez sur "New +" → "Web Service"
4. Connectez votre dépôt GitHub
5. Sélectionnez le repo `medical-ai-assistant`

### 5. Configuration Render

Render détectera automatiquement le fichier `render.yaml`, mais vous pouvez aussi configurer manuellement:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn app:app
```

**Environment:**
- Python 3.9+

### 6. Variables d'environnement (optionnel)

Dans le dashboard Render, vous pouvez ajouter:
- `PYTHON_VERSION=3.9.0`

### 7. Déployer

Cliquez sur "Create Web Service" et attendez le déploiement (2-5 minutes).

Votre application sera disponible à: `https://votre-app.onrender.com`

## Test de l'API

Une fois déployé, testez les endpoints:

```bash
# Health check
curl https://votre-app.onrender.com/api/health

# Analyser des symptômes
curl -X POST https://votre-app.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fièvre", "toux", "fatigue"]}'
```

## Endpoints disponibles

- `GET /` - Interface web
- `GET /api/health` - Vérification de santé
- `POST /api/chat` - Chatbot
- `POST /api/analyze` - Analyse de symptômes
- `POST /api/drugs/check` - Vérification médicaments
- `GET /api/diseases` - Liste des maladies
- `GET /api/drugs` - Liste des médicaments

## Notes importantes

⚠️ **Plan gratuit Render:**
- L'application s'endort après 15 min d'inactivité
- Premier chargement peut prendre 30-60 secondes
- 750 heures gratuites par mois

💡 **Pour améliorer les performances:**
- Utilisez un plan payant ($7/mois)
- Ajoutez un service de cache (Redis)
- Optimisez le modèle ML

## Dépannage

**Erreur de build:**
- Vérifiez que `requirements.txt` est correct
- Assurez-vous que Python 3.9+ est utilisé

**Application ne démarre pas:**
- Vérifiez les logs dans le dashboard Render
- Testez localement: `python app.py`

**Erreur 502:**
- L'app est en train de démarrer (attendez 1 minute)
- Vérifiez que le port est correct (Render utilise $PORT)

## Support

Pour toute question, consultez:
- Documentation Render: https://render.com/docs
- Logs de l'application dans le dashboard Render
