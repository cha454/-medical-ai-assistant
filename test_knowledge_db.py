"""
Script de test pour vérifier la base de connaissances
"""

from src.knowledge_base import KnowledgeBase

# Initialiser
kb = KnowledgeBase()

# Statistiques
stats = kb.get_statistics()
print(f"📊 Total connaissances: {stats['total']}")
print(f"📊 Par catégorie: {stats['by_category']}")
print(f"📊 Par langue: {stats['by_language']}")
print()

# Dernières connaissances
print("📚 Dernières connaissances enregistrées:")
knowledge = kb.get_all_knowledge(limit=10)
if knowledge:
    for k in knowledge:
        print(f"\n- ID: {k['id']}")
        print(f"  Question: {k['question']}")
        print(f"  Réponse: {k['answer']}")
        print(f"  Catégorie: {k['category']}")
        print(f"  Langue: {k.get('language', 'fr')}")
else:
    print("❌ Aucune connaissance trouvée")

print()

# Test de recherche
print("🔍 Test de recherche pour 'bonjour fang':")
results = kb.search_knowledge("bonjour fang", limit=5)
if results:
    for r in results:
        print(f"\n- Question: {r['question']}")
        print(f"  Réponse: {r['answer']}")
else:
    print("❌ Aucun résultat trouvé")
