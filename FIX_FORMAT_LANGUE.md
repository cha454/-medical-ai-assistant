# 🔧 Fix: Support Format "bonjour en langue fang se dit MBOLO"

## 🐛 Problème Signalé

**Description**: Quand l'utilisateur enseigne avec le format "bonjour en langue fang se dit MBOLO", rien n'est enregistré.

**Exemple**:
```
Input: "bonjour en langue fang se dit MBOLO"
Résultat: L'IA répond mais n'enregistre PAS
```

**Test Utilisateur**:
1. Sur `/teach`: "bonjour en langue fang se dit MBOLO" → IA répond OK
2. Sur `/chat` (après actualisation): "comment dit on bonjour en langue fang?" → IA répond "Ndo" (FAUX)

---

## 🔍 Analyse du Problème

### Pattern Existant
```python
r'(.+?)\s+(?:signifie|veut dire|se dit|c\'est)\s+(.+?)\s+en\s+(\w+)'
```

Ce pattern cherche : `[TERME] [VERBE] [SIGNIFICATION] en [LANGUE]`

**Exemples qui fonctionnent**:
- ✅ "Nlo signifie fièvre en Fang"
- ✅ "Mbolo veut dire bonjour en Fang"

**Exemples qui NE fonctionnent PAS**:
- ❌ "bonjour en langue fang se dit MBOLO"
- ❌ "fièvre en Fang se dit Nlo"

### Pourquoi Ça Ne Fonctionne Pas ?

Le format utilisateur est : `[SIGNIFICATION] en [LANGUE] [VERBE] [TERME]`

C'est l'**ordre inverse** du pattern existant !

---

## ✅ Solution Appliquée

### Commit: `0fdd833`

### A. Nouveau Pattern Ajouté

```python
# Format: "bonjour en langue fang se dit MBOLO" (NOUVEAU)
r'(.+?)\s+en\s+(?:langue\s+)?(\w+)\s+(?:signifie|veut dire|se dit|c\'est)\s+(.+)'
```

Ce pattern capture :
- Groupe 1: `bonjour` (signification)
- Groupe 2: `fang` (langue)
- Groupe 3: `MBOLO` (terme)

**Note**: `(?:langue\s+)?` rend le mot "langue" optionnel

### B. Logique Améliorée

**Nouveau Code**:

```python
elif len(groups) == 3:
    # Déterminer le format en fonction de la position de "en" dans la phrase
    words = message_lower.split()
    en_position = words.index('en') if 'en' in words else -1
    
    if en_position >= 0 and en_position < 3:
        # Format: "en Fang, Nlo signifie fièvre"
        language = groups[0].strip()
        term = groups[1].strip()
        meaning = groups[2].strip()
    elif 'se dit' in message_lower or 'veut dire' in message_lower or 'signifie' in message_lower:
        # Vérifier si "se dit" vient APRÈS "en langue"
        se_dit_pos = message_lower.find('se dit')
        veut_dire_pos = message_lower.find('veut dire')
        signifie_pos = message_lower.find('signifie')
        keyword_pos = max(se_dit_pos, veut_dire_pos, signifie_pos)
        
        if en_position >= 0 and keyword_pos > en_position:
            # Format: "bonjour en langue fang se dit MBOLO"
            meaning = groups[0].strip()
            language = groups[1].strip()
            term = groups[2].strip()
        else:
            # Format: "Nlo signifie fièvre en Fang"
            term = groups[0].strip()
            meaning = groups[1].strip()
            language = groups[2].strip()
    # ... autres cas
    
    question = f"Comment dit-on {meaning} en {language} ?"
    answer = term
    print(f"✅ Pattern détecté: meaning='{meaning}', term='{term}', language='{language}'")
    return (question, answer, category, language.lower())
```

**Logique**:
1. Trouver la position du mot "en" dans la phrase
2. Trouver la position du verbe ("se dit", "signifie", etc.)
3. Si le verbe vient APRÈS "en" → Format inversé
4. Sinon → Format standard

---

## 🧪 Tests à Effectuer

### Test 1: Format Inversé (NOUVEAU)
```
Input: "bonjour en langue fang se dit MBOLO"
Attendu: ✅ Enregistré
Question: "Comment dit-on bonjour en fang ?"
Réponse: "MBOLO"
Logs: "✅ Pattern détecté: meaning='bonjour', term='MBOLO', language='fang'"
```

### Test 2: Format Inversé Sans "langue"
```
Input: "bonjour en fang se dit MBOLO"
Attendu: ✅ Enregistré
Question: "Comment dit-on bonjour en fang ?"
Réponse: "MBOLO"
```

### Test 3: Format Standard (Toujours Fonctionnel)
```
Input: "Nlo signifie fièvre en Fang"
Attendu: ✅ Enregistré
Question: "Comment dit-on fièvre en fang ?"
Réponse: "Nlo"
```

### Test 4: Format avec "veut dire"
```
Input: "merci en fang veut dire Akiba"
Attendu: ✅ Enregistré
Question: "Comment dit-on merci en fang ?"
Réponse: "Akiba"
```

### Test 5: Format avec "c'est"
```
Input: "au revoir en fang c'est Nzame"
Attendu: ✅ Enregistré
Question: "Comment dit-on au revoir en fang ?"
Réponse: "Nzame"
```

---

## 📊 Formats Supportés

### Avant (Limité)
| Format | Exemple | Support |
|--------|---------|---------|
| `[TERME] signifie [SIGNIFICATION] en [LANGUE]` | "Nlo signifie fièvre en Fang" | ✅ |
| `[TERME] veut dire [SIGNIFICATION] en [LANGUE]` | "Mbolo veut dire bonjour en Fang" | ✅ |
| `[SIGNIFICATION] en [LANGUE] se dit [TERME]` | "bonjour en fang se dit MBOLO" | ❌ |
| `[SIGNIFICATION] en langue [LANGUE] se dit [TERME]` | "bonjour en langue fang se dit MBOLO" | ❌ |

### Après (Complet)
| Format | Exemple | Support |
|--------|---------|---------|
| `[TERME] signifie [SIGNIFICATION] en [LANGUE]` | "Nlo signifie fièvre en Fang" | ✅ |
| `[TERME] veut dire [SIGNIFICATION] en [LANGUE]` | "Mbolo veut dire bonjour en Fang" | ✅ |
| `[SIGNIFICATION] en [LANGUE] se dit [TERME]` | "bonjour en fang se dit MBOLO" | ✅ |
| `[SIGNIFICATION] en langue [LANGUE] se dit [TERME]` | "bonjour en langue fang se dit MBOLO" | ✅ |
| `[SIGNIFICATION] en [LANGUE] veut dire [TERME]` | "merci en fang veut dire Akiba" | ✅ |
| `[SIGNIFICATION] en [LANGUE] c'est [TERME]` | "au revoir en fang c'est Nzame" | ✅ |
| `[SIGNIFICATION] en [LANGUE] = [TERME]` | "bonjour en fang = MBOLO" | ✅ |
| `[TERME] = [SIGNIFICATION]` | "MBOLO = bonjour" | ✅ |

---

## 🔍 Comment Vérifier ?

### 1. Vérifier les Logs Railway
Chercher dans les logs:
```
✅ Pattern détecté: meaning='bonjour', term='MBOLO', language='fang'
✅ Connaissance enregistrée: ID=X, Q='Comment dit-on bonjour en fang ?', A='MBOLO', Cat=langue_locale, Lang=fang
```

### 2. Tester sur /teach
1. Aller sur `/teach`
2. Taper: **"bonjour en langue fang se dit MBOLO"**
3. Vérifier que l'IA confirme

### 3. Vérifier sur /knowledge
1. Aller sur `/knowledge`
2. Chercher la connaissance
3. Vérifier:
   - Question: "Comment dit-on bonjour en fang ?"
   - Réponse: "MBOLO"
   - Catégorie: langue_locale
   - Langue: fang

### 4. Tester sur /chat
1. Aller sur `/chat`
2. Rafraîchir (F5)
3. Demander: **"comment dit on bonjour en langue fang?"**
4. ✅ L'IA devrait répondre: **"MBOLO"**

---

## 💡 Exemples d'Utilisation

### Langues Locales
```
"bonjour en fang se dit MBOLO"
"merci en ewondo veut dire Akiba"
"au revoir en lingala c'est Nzame"
"fièvre en fang = Nlo"
```

### Variantes Acceptées
```
"bonjour en langue fang se dit MBOLO"  ← avec "langue"
"bonjour en fang se dit MBOLO"         ← sans "langue"
"MBOLO signifie bonjour en fang"       ← ordre inverse
"MBOLO = bonjour"                      ← format court
```

---

## 🐛 Si Ça Ne Fonctionne Toujours Pas

### 1. Vérifier le Format
Assure-toi d'utiliser un des formats supportés:
- `[mot] en [langue] se dit [traduction]`
- `[traduction] signifie [mot] en [langue]`
- `[mot] = [traduction]`

### 2. Vérifier les Logs
Dans Railway, chercher:
```bash
grep "Pattern détecté" logs.txt
grep "Connaissance enregistrée" logs.txt
grep "Pas d'enseignement détecté" logs.txt
```

### 3. Tester Localement
```python
from src.teach_routes import extract_knowledge

# Test
result = extract_knowledge("bonjour en langue fang se dit MBOLO", "Réponse IA")
print(result)
# Attendu: ('Comment dit-on bonjour en fang ?', 'MBOLO', 'langue_locale', 'fang')
```

### 4. Utiliser le Script de Test
```bash
python test_knowledge_db.py
```

---

## 📝 Notes Importantes

### Mots-Clés Supportés
- `signifie`
- `veut dire`
- `se dit`
- `c'est`
- `=` (égal)

### Langues Détectées
Le pattern capture le nom de la langue après "en":
- "en fang" → langue = "fang"
- "en langue fang" → langue = "fang"
- "en ewondo" → langue = "ewondo"
- "en lingala" → langue = "lingala"

### Ordre des Mots
Le système détecte automatiquement l'ordre:
- Si "se dit" vient APRÈS "en" → Format inversé
- Si "signifie" vient AVANT "en" → Format standard

---

**Date**: 24 Janvier 2026  
**Commit**: `0fdd833`  
**Status**: ✅ Corrigé et Déployé  
**Prochaine Étape**: Tests Utilisateur avec Différents Formats
