"""Test rapide pour la recherche d'images de mouton"""

# Simuler l'extraction et la traduction
text = "je veux les images d'un mouton"

# Extraction
patterns = [
    "je veux les images d'un ", "je veux les images d'une ",
]

extracted = text.lower()
for pattern in patterns:
    if pattern in extracted:
        extracted = extracted.split(pattern, 1)[1].strip()
        break

print(f"Texte original: '{text}'")
print(f"Extrait: '{extracted}'")

# Traduction
translations = {
    "mouton": "sheep",
    "cheval": "horse",
    "chat": "cat",
    "chien": "dog"
}

search_query = extracted
for fr_word, en_word in translations.items():
    if fr_word in search_query:
        search_query = search_query.replace(fr_word, en_word)
        print(f"Traduit: '{extracted}' → '{search_query}'")
        break

print(f"\nRequête finale pour Pixabay: '{search_query}'")
