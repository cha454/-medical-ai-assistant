# 🐘 Solution Persistance : PostgreSQL sur Railway

## 🎯 Problème Résolu

La base de connaissances (`knowledge.db`) se vidait à chaque actualisation car SQLite n'est pas persistant sur Railway sans volume.

**Solution** : Utiliser PostgreSQL fourni gratuitement par Railway (persistant par défaut).

---

## ✅ Modifications Effectuées

### 1. Code Modifié : `src/knowledge_base.py`

Le code détecte automatiquement l'environnement :
- **Railway** (avec `DATABASE_URL`) → PostgreSQL
- **Local** (sans `DATABASE_URL`) → SQLite

```python
def __init__(self, db_path=None):
    self.use_postgres = False
    self.db_url = os.environ.get('DATABASE_URL')
    
    if self.db_url:
        # PostgreSQL sur Railway
        self.use_postgres = True
        print(f"✓ Utilisation de PostgreSQL (Railway)")
    else:
        # SQLite en local
        print(f"✓ Base de données SQLite: {db_path}")
```

**Avantages** :
- ✅ Détection automatique
- ✅ Pas de changement de code nécessaire
- ✅ Fonctionne en local ET sur Railway
- ✅ Support complet des deux bases de données

### 2. Dépendance Ajoutée : `requirements.txt`

```
psycopg2-binary>=2.9.0
```

### 3. `.gitignore` Modifié

```
*.db
!knowledge.db  # ← Permet de tracker knowledge.db en local
```

---

## 🚀 Configuration Railway (3 étapes)

### Étape 1 : Ajouter PostgreSQL

1. Aller sur Railway Dashboard
2. Ouvrir ton projet `medical-ai-assistant`
3. Cliquer sur **"+ New"** (en haut à droite)
4. Sélectionner **"Database"**
5. Choisir **"PostgreSQL"**
6. Attendre la création (30 secondes)

✅ Railway crée automatiquement la variable `DATABASE_URL`

### Étape 2 : Vérifier la Variable

1. Cliquer sur ton service `medical-ai-assistant`
2. Aller dans **"Variables"**
3. Vérifier que `DATABASE_URL` existe
   - Format : `postgresql://user:password@host:port/database`
   - Créée automatiquement par Railway

### Étape 3 : Redéployer

1. Aller dans **"Deployments"**
2. Cliquer sur **"Redeploy"**
3. Attendre le déploiement (2-3 minutes)

---

## 🔍 Vérification

### 1. Vérifier les Logs

Dans les logs Railway, chercher :
```
✓ Utilisation de PostgreSQL (Railway)
```

Si tu vois ça, PostgreSQL est actif ! 🎉

### 2. Test Complet de Persistance

#### Test 1 : Enseigner
1. Aller sur `/teach`
2. Dire : "Mbolo signifie bonjour en Fang"
3. L'IA confirme l'apprentissage

#### Test 2 : Vérifier
1. Aller sur `/knowledge`
2. ✅ La connaissance doit apparaître

#### Test 3 : Actualiser (F5)
1. Actualiser la page `/knowledge`
2. ✅ La connaissance doit TOUJOURS être là

#### Test 4 : Redémarrer l'App
1. Railway Dashboard → Settings → Restart
2. Attendre le redémarrage
3. Aller sur `/knowledge`
4. ✅ La connaissance doit TOUJOURS être là

#### Test 5 : Utiliser sur Chat
1. Aller sur `/chat`
2. Demander : "Comment dit-on bonjour en Fang ?"
3. ✅ L'IA doit répondre : "Mbolo"

---

## 📊 Comparaison SQLite vs PostgreSQL

| Critère | SQLite (Local) | PostgreSQL (Railway) |
|---------|----------------|----------------------|
| **Persistance** | ✅ Oui (fichier local) | ✅ Oui (base distante) |
| **Performance** | ⚡ Très rapide | ⚡ Rapide |
| **Concurrent** | ⚠️ Limité | ✅ Excellent |
| **Gratuit** | ✅ Oui | ✅ Oui (Railway) |
| **Backup** | 📁 Fichier .db | 🔄 Railway backup |
| **Scalabilité** | ⚠️ Limitée | ✅ Excellente |

---

## 🎓 Comment ça Marche ?

### Détection Automatique

```python
# Railway détecte DATABASE_URL
if os.environ.get('DATABASE_URL'):
    # Utiliser PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
else:
    # Utiliser SQLite
    conn = sqlite3.connect('knowledge.db')
```

### Syntaxe Adaptée

Le code adapte automatiquement la syntaxe SQL :

**PostgreSQL** :
```sql
-- Placeholder
INSERT INTO knowledge VALUES (%s, %s, %s)

-- Auto-increment
id SERIAL PRIMARY KEY

-- Conflict
ON CONFLICT (name) DO NOTHING
```

**SQLite** :
```sql
-- Placeholder
INSERT INTO knowledge VALUES (?, ?, ?)

-- Auto-increment
id INTEGER PRIMARY KEY AUTOINCREMENT

-- Conflict
INSERT OR IGNORE
```

---

## 🐛 Dépannage

### Problème 1 : "No module named 'psycopg2'"

**Cause** : `psycopg2-binary` pas installé

**Solution** :
```bash
pip install psycopg2-binary
```

Ou attendre le redéploiement Railway (installe automatiquement).

### Problème 2 : "could not connect to server"

**Cause** : PostgreSQL pas créé sur Railway

**Solution** :
1. Railway Dashboard → + New → Database → PostgreSQL
2. Attendre la création
3. Redéployer

### Problème 3 : La base se vide toujours

**Vérifications** :
1. PostgreSQL est-il créé ? (Railway Dashboard → Databases)
2. `DATABASE_URL` existe-t-elle ? (Variables)
3. Les logs montrent-ils "PostgreSQL" ? (Logs)
4. Le code est-il à jour ? (Dernier commit)

### Problème 4 : Erreur "relation does not exist"

**Cause** : Tables pas créées

**Solution** : Redémarrer l'app (les tables se créent automatiquement au démarrage)

---

## 💾 Backup et Migration

### Exporter depuis SQLite (Local)

```bash
# Exporter en JSON
python manage_knowledge.py export knowledge_backup.json
```

### Importer vers PostgreSQL (Railway)

1. Déployer sur Railway avec PostgreSQL
2. Utiliser l'API d'import :
```bash
curl -X POST https://your-app.railway.app/api/knowledge/import \
  -H "Content-Type: application/json" \
  -d @knowledge_backup.json
```

Ou utiliser le script :
```python
from src.knowledge_base import KnowledgeBase
import json

kb = KnowledgeBase()  # Utilise PostgreSQL sur Railway

with open('knowledge_backup.json') as f:
    data = json.load(f)
    for item in data:
        kb.add_knowledge(
            question=item['question'],
            answer=item['answer'],
            category=item['category']
        )
```

---

## 📈 Avantages PostgreSQL

### 1. Persistance Garantie
- ✅ Survit aux redémarrages
- ✅ Survit aux redéploiements
- ✅ Survit aux mises à jour

### 2. Performance
- ⚡ Optimisé pour les requêtes concurrentes
- ⚡ Index automatiques
- ⚡ Cache intelligent

### 3. Scalabilité
- 📈 Supporte des milliers de connaissances
- 📈 Plusieurs utilisateurs simultanés
- 📈 Croissance sans limite

### 4. Backup Automatique
- 🔄 Railway fait des backups automatiques
- 🔄 Restauration en 1 clic
- 🔄 Historique des versions

---

## ✅ Checklist de Configuration

- [x] Code modifié (`knowledge_base.py`)
- [x] Dépendance ajoutée (`psycopg2-binary`)
- [x] `.gitignore` mis à jour
- [ ] PostgreSQL créé sur Railway
- [ ] Variable `DATABASE_URL` vérifiée
- [ ] Application redéployée
- [ ] Logs vérifiés (PostgreSQL actif)
- [ ] Test : Enseigner une connaissance
- [ ] Test : Actualiser → Connaissance toujours là
- [ ] Test : Redémarrer → Connaissance toujours là
- [ ] Test : Utiliser sur /chat → IA répond correctement

---

## 🎉 Résultat Final

Après configuration :
1. ✅ Les connaissances sont **persistantes**
2. ✅ Elles survivent aux **actualisations**
3. ✅ Elles survivent aux **redémarrages**
4. ✅ Elles survivent aux **redéploiements**
5. ✅ L'IA les **utilise correctement** sur /chat
6. ✅ Fonctionne en **local** (SQLite) ET sur **Railway** (PostgreSQL)

**La base de connaissances fonctionne enfin parfaitement ! 🚀**

---

**Date** : 24 Janvier 2026  
**Commit** : À venir  
**Status** : ✅ Code Prêt - Configuration Railway Requise
