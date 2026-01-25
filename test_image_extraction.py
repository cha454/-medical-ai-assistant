"""Test de l'extraction de requête pour la recherche d'images"""

import sys
sys.path.insert(0, 'src')

from image_search import MedicalImageSearch

# Créer une instance
searcher = MedicalImageSearch()

# Tests
test_queries = [
    "je veux les images d'un mouton",
    "je veux les images d'un arbre",
    "je veux une image d'un cheval",
    "montre-moi des images de chat",
    "photo de chien",
    "image du cœur humain"
]

print("=== Test d'extraction de requête ===\n")
for query in test_queries:
    extracted = searcher.extract_query_from_request(query)
    print(f"Entrée: '{query}'")
    print(f"Extrait: '{extracted}'")
    print()
