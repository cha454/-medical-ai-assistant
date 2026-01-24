# 🧪 Test de la Base de Connaissances

## 🎯 Objectif

Vérifier que l'IA utilise correctement les connaissances apprises via le mode enseignement.

---

## ✅ Améliorations Appliquées

### 1. Recherche Intelligente
- **Avant**: Recherche exacte uniquement
- **Après**: Recherche par mots-clés individuels
- **Avantage**: Trouve les connaissances même si la question n'est pas formulée exactement pareil

### 2. Contexte Explicite pour le LLM
- **Avant**: Contexte simple
- **Après**: Instructions claires pour le LLM d'utiliser les connaissances apprises EN PRIORITÉ
- **Avantage**: Le LLM respecte mieux les enseignements de l'utilisateur

---

## 🧪 Scénario de Test

### Étape 1: Enseigner une Connaissance
1. Aller sur `/teach`
2. Taper: **"Mbolo signifie bonjour en langue Fang"**
3. Cliquer sur "Enseigner"
4. ✅ Vérifier que l'IA confirme avoir appris

### Étape 2: Vérifier l'Enregistrement
1. Aller sur `/knowledge`
2. ✅ Vérifier que la connaissance apparaît dans la liste
3. Noter l'ID de la connaissance

### Étape 3: Tester sur Chat (Après Actualisation)
1. Aller sur `/chat`
2. Rafraîchir la page (F5)
3. Poser la question: **"Comment dit-on bonjour en Fang ?"**
4. ✅ L'IA devrait répondre: **"Mbolo"**

### Étape 4: Tester avec Variantes
Essayer différentes formulations:
- "Que veut dire Mbolo ?"
- "Mbolo c'est quoi ?"
- "Traduis Mbolo"
- "Comment on dit bonjour en langue Fang ?"

✅ L'IA devrait utiliser la connaissance apprise dans tous les cas

---

## 🔍 Vérification des Logs

### Dans la Console du Navigateur (F12)
Chercher ces messages:
```
✓ Base de connaissances initialisée
✓ Connaissances personnalisées injectées dans le contexte
```

### Dans les Logs Railway
Chercher:
```
✓ Base de connaissances personnalisée activée
✓ Base de connaissances initialisée
```

---

## 🐛 Si Ça Ne Fonctionne Pas

### Problème 1: "Erreur: knowledge.html"
**Cause**: Fichier manquant (déjà corrigé)
**Solution**: Déjà résolu dans commit `241633c`

### Problème 2: L'IA ne trouve pas la connaissance
**Cause**: Recherche trop stricte
**Solution**: Améliorations appliquées dans commit `d01f29c`

### Problème 3: L'IA trouve mais n'utilise pas la connaissance
**Cause**: Contexte pas assez explicite pour le LLM
**Solution**: Contexte amélioré dans commit `d01f29c`

### Problème 4: Base de données vide après actualisation
**Cause**: Base de données SQLite non persistante
**Solution**: Vérifier que `knowledge.db` existe dans le dossier racine

---

## 📊 Exemples de Tests

### Test 1: Langue Locale
```
Teach: "Nlo signifie fièvre en Fang"
Chat: "Comment dit-on fièvre en Fang ?"
Attendu: "Nlo"
```

### Test 2: Plante Médicinale
```
Teach: "Le Kinkeliba soigne le paludisme"
Chat: "Quelle plante soigne le paludisme ?"
Attendu: "Le Kinkeliba"
```

### Test 3: Information Personnelle
```
Teach: "Je suis allergique à la pénicilline"
Chat: "Suis-je allergique à quelque chose ?"
Attendu: "Oui, tu es allergique à la pénicilline"
```

### Test 4: Terme Médical
```
Teach: "Le paludisme se dit malaria en anglais"
Chat: "Comment dit-on paludisme en anglais ?"
Attendu: "Malaria"
```

---

## 🔧 Débogage Avancé

### Vérifier la Base de Données
```python
import sqlite3

conn = sqlite3.connect('knowledge.db')
cursor = conn.cursor()

# Voir toutes les connaissances
cursor.execute('SELECT * FROM knowledge')
print(cursor.fetchall())

# Compter les connaissances
cursor.execute('SELECT COUNT(*) FROM knowledge')
print(f"Total: {cursor.fetchone()[0]}")

conn.close()
```

### Tester la Recherche
```python
from src.knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Rechercher
results = kb.search_knowledge("bonjour Fang")
print(f"Trouvé: {len(results)} résultats")
for r in results:
    print(f"- {r['question']}: {r['answer']}")

# Obtenir le contexte pour LLM
context = kb.get_context_for_llm("bonjour Fang")
print(context)
```

---

## ✅ Checklist de Validation

- [ ] La connaissance est enregistrée sur `/teach`
- [ ] La connaissance apparaît sur `/knowledge`
- [ ] La recherche trouve la connaissance (logs)
- [ ] Le contexte est injecté dans le LLM (logs)
- [ ] L'IA utilise la connaissance dans sa réponse
- [ ] Ça fonctionne avec différentes formulations
- [ ] Ça fonctionne après actualisation de la page

---

## 📝 Notes Importantes

### Persistance des Données
- Les connaissances sont stockées dans `knowledge.db` (SQLite)
- Ce fichier doit être persistant sur Railway
- Vérifier que le volume est configuré correctement

### Recherche Intelligente
- La recherche est maintenant **insensible à la casse**
- Elle cherche par **mots-clés individuels** (mots > 3 lettres)
- Elle cherche dans **question**, **réponse** ET **contexte**

### Contexte LLM
- Le contexte est maintenant **très explicite**
- Instructions claires pour utiliser les connaissances EN PRIORITÉ
- Format structuré pour faciliter la compréhension du LLM

---

## 🚀 Prochaines Améliorations Possibles

### Court Terme
- [ ] Recherche par similarité sémantique (embeddings)
- [ ] Synonymes et variations linguistiques
- [ ] Correction orthographique automatique

### Moyen Terme
- [ ] Interface de gestion avancée des connaissances
- [ ] Export/Import en masse
- [ ] Catégorisation automatique améliorée

### Long Terme
- [ ] Apprentissage automatique des patterns
- [ ] Suggestions de connaissances manquantes
- [ ] Validation collaborative des connaissances

---

**Date**: 24 Janvier 2026  
**Commits**: `d01f29c` (amélioration recherche), `241633c` (création knowledge.html)  
**Status**: ✅ Améliorations Appliquées
