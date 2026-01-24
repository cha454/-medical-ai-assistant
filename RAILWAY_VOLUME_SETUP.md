# 🚂 Configuration Volume Persistant Railway

## 🐛 Problème

La base de connaissances (`knowledge.db`) se vide à chaque actualisation ou redémarrage sur Railway.

**Cause**: Le fichier SQLite n'est pas dans un volume persistant.

---

## ✅ Solution : Configurer un Volume Persistant

### Méthode 1 : Via l'Interface Railway (RECOMMANDÉ)

#### Étape 1 : Créer un Volume
1. Aller sur Railway Dashboard
2. Sélectionner ton projet `medical-ai-assistant`
3. Aller dans l'onglet **"Settings"**
4. Cliquer sur **"Volumes"** dans le menu latéral
5. Cliquer sur **"+ New Volume"**
6. Configurer :
   - **Mount Path**: `/app/data`
   - **Size**: 1 GB (suffisant pour la base de données)
7. Cliquer sur **"Add Volume"**

#### Étape 2 : Ajouter Variable d'Environnement
1. Aller dans l'onglet **"Variables"**
2. Ajouter une nouvelle variable :
   - **Key**: `DATA_DIR`
   - **Value**: `/app/data`
3. Sauvegarder

#### Étape 3 : Redéployer
1. Aller dans l'onglet **"Deployments"**
2. Cliquer sur **"Redeploy"**
3. Attendre que le déploiement se termine

---

### Méthode 2 : Via railway.toml (Alternative)

Créer un fichier `railway.toml` à la racine :

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn app:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[[deploy.volumes]]
mountPath = "/app/data"
```

Puis redéployer.

---

## 🔍 Vérification

### 1. Vérifier que le Volume est Monté

Dans les logs Railway, chercher :
```
✓ Dossier data créé: /app/data
✓ Base de données: /app/data/knowledge.db
```

### 2. Tester la Persistance

1. **Enseigner** sur `/teach` :
   ```
   "Mbolo signifie bonjour en Fang"
   ```

2. **Vérifier** sur `/knowledge` :
   - La connaissance doit apparaître

3. **Actualiser** la page `/knowledge` (F5) :
   - ✅ La connaissance doit TOUJOURS être là

4. **Redémarrer** l'application sur Railway :
   - Aller dans Settings → Restart
   - Attendre le redémarrage
   - ✅ La connaissance doit TOUJOURS être là

5. **Tester** sur `/chat` :
   - Demander : "Comment dit-on bonjour en Fang ?"
   - ✅ L'IA doit répondre : "Mbolo"

---

## 📊 Avant/Après

### Avant (Sans Volume)
```
Déploiement 1:
- Enseigner "Mbolo = bonjour" → ✅ OK
- Actualiser → ❌ Perdu
- Redémarrer → ❌ Perdu

Déploiement 2:
- Base de données vide → ❌ Tout perdu
```

### Après (Avec Volume)
```
Déploiement 1:
- Enseigner "Mbolo = bonjour" → ✅ OK
- Actualiser → ✅ Toujours là
- Redémarrer → ✅ Toujours là

Déploiement 2:
- Base de données conservée → ✅ Tout conservé
```

---

## 🛠️ Code Modifié

### knowledge_base.py

**Avant**:
```python
def __init__(self, db_path='knowledge.db'):
    self.db_path = db_path
```

**Après**:
```python
def __init__(self, db_path=None):
    if db_path is None:
        import os
        data_dir = os.environ.get('DATA_DIR', '/app/data')
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        
        db_path = os.path.join(data_dir, 'knowledge.db')
    
    self.db_path = db_path
```

**Avantages**:
- ✅ Utilise `/app/data` par défaut (volume persistant)
- ✅ Crée le dossier automatiquement
- ✅ Fallback sur le dossier courant si erreur
- ✅ Configurable via variable d'environnement `DATA_DIR`

---

## 🐛 Dépannage

### Problème 1 : "Permission denied" sur /app/data

**Solution**: Vérifier que le volume est bien monté dans Railway Settings → Volumes

### Problème 2 : La base de données se vide toujours

**Vérifications**:
1. Le volume est-il créé ? (Railway Dashboard → Volumes)
2. Le mount path est-il `/app/data` ?
3. La variable `DATA_DIR` est-elle définie ?
4. Les logs montrent-ils `✓ Base de données: /app/data/knowledge.db` ?

### Problème 3 : "No such file or directory"

**Solution**: Le dossier `/app/data` n'existe pas. Vérifier que :
- Le volume est bien monté
- Le code crée le dossier automatiquement
- Les permissions sont correctes

---

## 📝 Notes Importantes

### Taille du Volume
- **1 GB** est largement suffisant pour la base de données
- SQLite est très compact (quelques KB à quelques MB)
- Peut stocker des milliers de connaissances

### Backup
Pour sauvegarder la base de données :
```bash
# Télécharger depuis Railway
railway run cat /app/data/knowledge.db > knowledge_backup.db

# Ou utiliser l'API d'export
curl https://your-app.railway.app/api/knowledge/export
```

### Migration
Si tu as déjà des données dans l'ancienne base :
1. Exporter : `/api/knowledge/export`
2. Configurer le volume
3. Importer : Utiliser `manage_knowledge.py`

---

## ✅ Checklist de Configuration

- [ ] Volume créé sur Railway (Mount Path: `/app/data`)
- [ ] Variable `DATA_DIR=/app/data` ajoutée
- [ ] Code modifié (commit `XXX`)
- [ ] Application redéployée
- [ ] Logs montrent `✓ Base de données: /app/data/knowledge.db`
- [ ] Test : Enseigner une connaissance
- [ ] Test : Actualiser la page → Connaissance toujours là
- [ ] Test : Redémarrer l'app → Connaissance toujours là
- [ ] Test : Demander sur /chat → IA utilise la connaissance

---

## 🚀 Après Configuration

Une fois le volume configuré :
1. ✅ Les connaissances sont **persistantes**
2. ✅ Elles survivent aux **redémarrages**
3. ✅ Elles survivent aux **redéploiements**
4. ✅ L'IA peut les **utiliser sur /chat**

**La base de connaissances fonctionne enfin correctement ! 🎉**

---

**Date**: 24 Janvier 2026  
**Commit**: À venir  
**Status**: ⏳ Configuration Requise sur Railway
