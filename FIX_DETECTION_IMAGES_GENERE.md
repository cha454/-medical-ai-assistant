# 🖼️ Correction : Séparation Recherche vs Génération d'Images

## Problème identifié

Les mots-clés "génère", "crée", "dessine" étaient ajoutés à la **recherche d'images**, ce qui causait une confusion entre :
- **Recherche d'images** : Chercher des images existantes sur le web (Pixabay, Google)
- **Génération d'images** : Créer une nouvelle image avec IA (DALL-E)

## Différence importante

### 1. Recherche d'images (ce qui existe déjà)
- "montre-moi un chat rose" → Cherche des images sur Pixabay/Google
- "je veux les images d'un mouton" → Affiche des images existantes
- **Module** : `image_search.py`

### 2. Génération d'images (ce qui existe aussi)
- "génère-moi un chat rose" → **CRÉER** une nouvelle image avec DALL-E
- "dessine-moi un dragon" → L'IA dessine une image unique
- **Module** : `image_generator.py`

## Solution appliquée

### Correction dans `image_search.py`

**Mots-clés RETIRÉS de la recherche :**
- ❌ "génère", "genere", "génère-moi", "genere-moi"
- ❌ "crée", "cree", "crée-moi", "cree-moi"
- ❌ "dessine", "dessine-moi"

**Mots-clés GARDÉS pour la recherche :**
- ✅ "image", "photo", "picture", "illustration"
- ✅ "montre-moi", "montre moi", "voir", "affiche"
- ✅ "trouve", "trouve-moi", "cherche", "cherche-moi"
- ✅ "à quoi ressemble", "ressemble"

### Mots-clés dans `image_generator.py` (déjà corrects)

**Mots-clés pour la GÉNÉRATION :**
- ✅ "génère", "générer", "genere", "generer"
- ✅ "créer", "creer", "créé", "cree"
- ✅ "dessine", "dessiner", "dessiné"
- ✅ "illustre", "illustrer"
- ✅ "crée moi", "génère moi"

## Ordre de détection dans le chatbot

```python
# 1. RECHERCHE d'images (image_search.py)
if image_search.is_image_request(user_input):
    # Cherche sur Pixabay/Google
    
# 2. GÉNÉRATION d'images (image_generator.py)
if image_generator.detect_image_request(user_input):
    # Génère avec DALL-E
```

## Exemples corrects maintenant

### Recherche d'images (web)
- ✅ "montre-moi un chat rose" → Cherche sur Pixabay
- ✅ "je veux les images d'un mouton" → Cherche sur Google
- ✅ "trouve-moi un arbre" → Cherche des images existantes
- ✅ "à quoi ressemble un lion" → Cherche des photos

### Génération d'images (IA)
- ✅ "génère-moi un chat rose" → Crée avec DALL-E
- ✅ "crée-moi un dragon" → Génère une nouvelle image
- ✅ "dessine-moi une maison" → Dessine avec IA
- ✅ "peux-tu créer un paysage" → Génère avec DALL-E

## Configuration requise

Pour que la génération d'images fonctionne, il faut :
1. Clé API OpenAI dans `.env` : `CLE_API_OPENAI=sk-...`
2. Module `openai` installé : `pip install openai`

Si la clé n'est pas configurée, seule la recherche d'images fonctionnera.

## Fichiers modifiés

- ✅ `src/image_search.py` - Retrait des mots-clés de génération
- ✅ `src/image_generator.py` - Déjà correct (pas de modification)

## Résultat

Maintenant, les deux fonctionnalités sont bien séparées :
- **"montre-moi"** → Recherche sur le web
- **"génère-moi"** → Création avec IA

Plus de confusion ! 🎉
