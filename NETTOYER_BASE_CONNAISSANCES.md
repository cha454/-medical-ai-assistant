# 🧹 Nettoyer la Base de Connaissances

## 🎯 Objectif

Supprimer les connaissances en double ou incorrectes et recommencer proprement.

---

## ✅ Améliorations Appliquées (Commit `447e66c`)

### 1. Filtrage Intelligent
Le système ne sauvegarde plus :
- ❌ Les salutations simples ("bonjour", "salut", etc.)
- ❌ Les questions sans information ("comment on dit...", "je veux apprendre...")
- ❌ Les phrases trop courtes (< 10 caractères)
- ❌ Les conversations générales

### 2. Nouveau Format Simplifié
Tu peux maintenant enseigner avec le format simple :
```
Mbolo = bonjour
```
Au lieu de :
```
Mbolo signifie bonjour en langue Fang
```

### 3. Extraction Améliorée
- Détection automatique de la langue
- Formatage cohérent des questions/réponses
- Catégorisation automatique

---

## 🧹 Méthode 1: Nettoyer via l'Interface Web

### Étape 1: Aller sur /knowledge
```
https://medical-ai-assistant-production.up.railway.app/knowledge
```

### Étape 2: Supprimer les Doublons
Pour chaque connaissance incorrecte ou en double :
1. Cliquer sur "🗑️ Supprimer"
2. Confirmer la suppression

### Connaissances à Supprimer (d'après ton exemple)
- ❌ "comment on dit bonjour en langue fang" → Question, pas une connaissance
- ❌ "je veux t'apprendre comment on dit..." → Conversation, pas une connaissance
- ❌ "bonjour" → Salutation simple, pas une connaissance
- ✅ Garder seulement : "bonjour = Mbolo" (si c'est la bonne traduction)

---

## 🧹 Méthode 2: Nettoyer via Script Python

### Script de Nettoyage
Créer un fichier `clean_knowledge.py` :

```python
import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('knowledge.db')
cursor = conn.cursor()

# Afficher toutes les connaissances
print("📚 Connaissances actuelles:\n")
cursor.execute('SELECT id, question, answer, category FROM knowledge ORDER BY id')
for row in cursor.fetchall():
    print(f"ID {row[0]}: {row[1]} → {row[2]} ({row[3]})")

print("\n" + "="*50 + "\n")

# Supprimer les connaissances non pertinentes
# Salutations simples
cursor.execute("DELETE FROM knowledge WHERE LOWER(question) IN ('bonjour', 'salut', 'hello', 'bonsoir')")
deleted_greetings = cursor.rowcount
print(f"✓ {deleted_greetings} salutations supprimées")

# Questions sans réponse utile
cursor.execute("DELETE FROM knowledge WHERE question LIKE '%comment%' AND question LIKE '%?%'")
deleted_questions = cursor.rowcount
print(f"✓ {deleted_questions} questions supprimées")

# Phrases "je veux apprendre"
cursor.execute("DELETE FROM knowledge WHERE LOWER(question) LIKE '%je veux%'")
deleted_wants = cursor.rowcount
print(f"✓ {deleted_wants} phrases 'je veux' supprimées")

# Sauvegarder les changements
conn.commit()

# Afficher le résultat
cursor.execute('SELECT COUNT(*) FROM knowledge')
total = cursor.fetchone()[0]
print(f"\n📊 Total restant: {total} connaissances")

# Afficher les connaissances restantes
print("\n📚 Connaissances après nettoyage:\n")
cursor.execute('SELECT id, question, answer, category FROM knowledge ORDER BY id')
for row in cursor.fetchall():
    print(f"ID {row[0]}: {row[1]} → {row[2]} ({row[3]})")

conn.close()
print("\n✅ Nettoyage terminé!")
```

### Exécuter le Script
```bash
python clean_knowledge.py
```

---

## 🧹 Méthode 3: Réinitialiser Complètement

### ⚠️ ATTENTION: Ceci supprime TOUTES les connaissances !

```python
import sqlite3

conn = sqlite3.connect('knowledge.db')
cursor = conn.cursor()

# Supprimer toutes les connaissances
cursor.execute('DELETE FROM knowledge')
conn.commit()

print(f"✅ Toutes les connaissances supprimées")
print(f"📊 Total: 0 connaissances")

conn.close()
```

---

## 📝 Recommencer Proprement

### Format Recommandé pour Enseigner

#### Langues Locales (Format Simple)
```
Mbolo = bonjour
Nlo = fièvre
Akiba = merci
```

#### Langues Locales (Format Complet)
```
Mbolo signifie bonjour en Fang
Nlo signifie fièvre en Fang
Akiba signifie merci en Fang
```

#### Plantes Médicinales
```
Le Kinkeliba soigne le paludisme
L'Artemisia traite la fièvre
```

#### Informations Personnelles
```
Je suis allergique à la pénicilline
J'ai du diabète de type 2
```

---

## ✅ Vérification Après Nettoyage

### 1. Vérifier sur /knowledge
- Aller sur `/knowledge`
- Vérifier que seules les vraies connaissances sont présentes
- Pas de questions, pas de conversations

### 2. Tester sur /chat
- Enseigner: `Mbolo = bonjour`
- Aller sur `/chat`
- Demander: "Comment dit-on bonjour en Fang ?"
- ✅ Réponse attendue: "Mbolo"

---

## 🎯 Exemple Complet

### Étape 1: Nettoyer
```python
# Supprimer toutes les connaissances incorrectes
python clean_knowledge.py
```

### Étape 2: Enseigner Proprement
Sur `/teach`, enseigner une par une :
```
Mbolo = bonjour
Nlo = fièvre
Akiba = merci
Nzambe = Dieu
Moto = personne
```

### Étape 3: Vérifier
Sur `/knowledge`, vérifier que les 5 connaissances sont bien enregistrées.

### Étape 4: Tester
Sur `/chat`, tester :
- "Comment dit-on bonjour en Fang ?" → Mbolo
- "Que signifie Nlo ?" → fièvre
- "Traduis Akiba" → merci

---

## 📊 Statistiques Attendues

Après nettoyage et enseignement propre :
```
Total: 5 connaissances
Catégories:
  - langue_locale: 5
  - autre: 0
```

---

## 🚀 Prochaines Améliorations

### Court Terme
- [ ] Détection automatique des doublons
- [ ] Fusion automatique des connaissances similaires
- [ ] Validation avant enregistrement

### Moyen Terme
- [ ] Interface de modification des connaissances
- [ ] Historique des modifications
- [ ] Import/Export en masse

---

**Date**: 24 Janvier 2026  
**Commit**: `447e66c` - Amélioration extraction connaissances  
**Status**: ✅ Filtrage Intelligent Activé
