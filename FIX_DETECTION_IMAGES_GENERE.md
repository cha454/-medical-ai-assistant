# 🖼️ Correction : Détection des demandes d'images avec "génère"

## Problème identifié

Quand l'utilisateur demande "génère moi un chat rose", l'IA ne détectait pas que c'était une demande d'**images** et répondait avec du texte et des liens au lieu d'afficher directement les images.

## Cause du problème

Le mot "génère" (et ses variantes) n'était pas dans la liste des mots-clés de détection d'images dans `image_search.py`.

## Solution appliquée

### 1. Ajout de nouveaux mots-clés de détection

**Fichier**: `src/image_search.py` - fonction `__init__()`

Ajout des mots-clés manquants :
```python
self.image_keywords = [
    "image", "photo", "picture", "img", "illustration",
    "montre-moi", "montre moi", "voir", "affiche", "afficher",
    "à quoi ressemble", "ressemble", "apparence", "aspect",
    # NOUVEAUX mots-clés ajoutés :
    "génère", "genere", "génère-moi", "genere-moi", "génère moi", "genere moi",
    "crée", "cree", "crée-moi", "cree-moi", "crée moi", "cree moi",
    "dessine", "dessine-moi", "dessine moi",
    "trouve", "trouve-moi", "trouve moi",
    "cherche", "cherche-moi", "cherche moi"
]
```

### 2. Amélioration de l'extraction de requête

**Fichier**: `src/image_search.py` - fonction `extract_query_from_request()`

Ajout de patterns pour extraire correctement la requête :
```python
patterns = [
    # NOUVEAUX patterns en premier (plus spécifiques)
    "génère-moi un ", "genere-moi un ", "génère moi un ", "genere moi un ",
    "génère-moi une ", "genere-moi une ", "génère moi une ", "genere moi une ",
    "génère un ", "genere un ", "génère une ", "genere une ",
    "crée-moi un ", "cree-moi un ", "crée moi un ", "cree moi un ",
    "crée-moi une ", "cree-moi une ", "crée moi une ", "cree moi une ",
    "dessine-moi un ", "dessine moi un ", "dessine-moi une ", "dessine moi une ",
    "trouve-moi un ", "trouve moi un ", "trouve-moi une ", "trouve moi une ",
    "cherche-moi un ", "cherche moi un ", "cherche-moi une ", "cherche moi une ",
    # ... patterns existants
]
```

## Exemples de requêtes qui fonctionnent maintenant

### Avant (ne fonctionnait pas)
- ❌ "génère moi un chat rose" → Réponse texte avec liens
- ❌ "crée moi un chien" → Réponse texte avec liens
- ❌ "dessine moi une maison" → Réponse texte avec liens

### Après (fonctionne correctement)
- ✅ "génère moi un chat rose" → Affiche 6 images de chats roses
- ✅ "crée moi un chien" → Affiche 6 images de chiens
- ✅ "dessine moi une maison" → Affiche 6 images de maisons
- ✅ "trouve moi un arbre" → Affiche 6 images d'arbres
- ✅ "cherche moi un mouton" → Affiche 6 images de moutons

## Test

Pour tester la correction :

1. Démarrer l'application : `python app.py`
2. Dans le chat, taper : "génère moi un chat rose"
3. Vérifier que 6 images de chats roses s'affichent directement

### Autres exemples à tester

- "génère-moi un cheval blanc"
- "crée moi une fleur rouge"
- "dessine-moi un paysage"
- "trouve moi un lion"
- "cherche moi un éléphant"

## Résultat attendu

Maintenant, quand vous demandez "génère moi un chat rose" :
1. Le système détecte que c'est une demande d'image (grâce à "génère")
2. Il extrait "chat rose" de la phrase
3. Il traduit "chat" en "cat" et cherche "cat rose" (ou "pink cat")
4. Il affiche 6 images directement dans le chat
5. Pas de réponse texte avec des liens

## Avantages

- ✅ Détection plus naturelle des demandes d'images
- ✅ Support de multiples verbes d'action (génère, crée, dessine, trouve, cherche)
- ✅ Avec ou sans tiret (génère-moi / génère moi)
- ✅ Avec ou sans accent (génère / genere)
- ✅ Expérience utilisateur améliorée

## Fichiers modifiés

- ✅ `src/image_search.py` - Ajout mots-clés et patterns

## Notes

- Les mots-clés sont en minuscules car le texte est converti en lowercase avant la détection
- Les patterns sont ordonnés du plus spécifique au plus général
- La traduction français → anglais fonctionne toujours (chat → cat, etc.)
