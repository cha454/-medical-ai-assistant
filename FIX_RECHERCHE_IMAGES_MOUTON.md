# 🐑 Correction : Recherche d'images de mouton

## Problème identifié

Quand l'utilisateur demande "je veux les images d'un mouton", le système retournait des images de chevaux au lieu de moutons.

## Causes du problème

1. **Extraction de requête incomplète** : Le pattern "je veux les images d'un" n'était pas dans la liste des patterns reconnus
2. **Traduction trop stricte** : La traduction ne fonctionnait que si la requête était EXACTEMENT le mot français (ex: "mouton"), pas si elle contenait d'autres mots
3. **Filtrage Pixabay insuffisant** : Pixabay retournait tous les résultats sans vérifier que les tags correspondent à la requête

## Solutions appliquées

### 1. Amélioration de l'extraction de requête

**Fichier**: `src/image_search.py` - fonction `extract_query_from_request()`

Ajout des patterns manquants en début de liste (ordre important) :
```python
patterns = [
    "je veux les images d'un ", "je veux les images d'une ", 
    "je veux les images du ", "je veux les images de la ", 
    "je veux les images de ",
    "je veux une image d'un ", "je veux une image d'une ", 
    "je veux une image du ", "je veux une image de la ", 
    "je veux une image de ",
    "je veux des images d'un ", "je veux des images d'une ", 
    "je veux des images du ", "je veux des images de la ", 
    "je veux des images de ",
    # ... autres patterns
]
```

### 2. Amélioration de la traduction

**Fichier**: `src/image_search.py` - fonction `search_images()`

Changement de la logique de traduction :
```python
# AVANT (ne fonctionnait que pour un mot exact)
if search_query in translations:
    search_query = translations[search_query]

# APRÈS (fonctionne même si la requête contient d'autres mots)
for fr_word, en_word in translations.items():
    if fr_word in search_query:
        search_query = search_query.replace(fr_word, en_word)
        translated = True
```

### 3. Filtrage strict des résultats Pixabay

**Fichier**: `src/image_search.py` - fonction `_search_pixabay()`

Ajout d'un filtrage des résultats pour vérifier que les tags correspondent :
```python
# Filtrer les résultats pour s'assurer qu'ils correspondent à la requête
query_words = set(query.lower().split())

for item in data.get("hits", []):
    tags = item.get("tags", "").lower()
    tags_words = set(tags.replace(",", " ").split())
    
    # Pour les animaux, être plus strict sur la correspondance
    if query.lower() in animal_keywords:
        if query.lower() in tags or any(word in tags for word in query_words):
            images.append({...})
```

### 4. Ajout de logs de debug

Ajout de messages pour tracer le processus :
```python
print(f"🔍 Requête originale: '{query}' → '{search_query}'")
print(f"🌍 Traduction: '{query}' → '{search_query}'")
print(f"✓ Pixabay: {len(images)} images trouvées (filtrées de {len(data.get('hits', []))} résultats)")
```

## Test

Pour tester la correction :

1. Démarrer l'application : `python app.py`
2. Dans le chat, taper : "je veux les images d'un mouton"
3. Vérifier que les images retournées sont bien des moutons (sheep)

### Exemples de requêtes qui devraient fonctionner

- "je veux les images d'un mouton" → sheep
- "je veux les images d'un cheval" → horse
- "je veux les images d'un chat" → cat
- "je veux les images d'un chien" → dog
- "montre-moi des images de mouton" → sheep
- "photo de mouton" → sheep

## Résultat attendu

Maintenant, quand vous demandez des images d'un mouton :
1. Le système extrait correctement "mouton" de la phrase
2. Il traduit "mouton" en "sheep"
3. Il recherche "sheep" sur Pixabay avec catégorie "animals"
4. Il filtre les résultats pour ne garder que ceux qui ont "sheep" dans les tags
5. Il retourne 6 images de moutons

## Fichiers modifiés

- ✅ `src/image_search.py` - Amélioration extraction, traduction et filtrage

## Notes

- La traduction fonctionne maintenant même si la requête contient plusieurs mots
- Le filtrage Pixabay est plus strict pour éviter les résultats non pertinents
- Les logs permettent de déboguer facilement si un problème survient
