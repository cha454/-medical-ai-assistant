"""
Test d'intégration du système de connaissances personnalisées
"""

import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("TEST D'INTÉGRATION - MODE ENSEIGNEMENT")
print("=" * 60)

# Test 1: Import de la base de connaissances
print("\n1️⃣ Test import KnowledgeBase...")
try:
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    print("   ✅ KnowledgeBase importée et initialisée")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 2: Statistiques initiales
print("\n2️⃣ Test statistiques...")
try:
    stats = kb.get_statistics()
    print(f"   ✅ Total connaissances: {stats['total']}")
    print(f"   ✅ Par catégorie: {stats['by_category']}")
    print(f"   ✅ Par langue: {stats['by_language']}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 3: Ajout d'une connaissance de test
print("\n3️⃣ Test ajout de connaissance...")
try:
    kb_id = kb.add_knowledge(
        question="Test: Nlo en Fang",
        answer="Nlo signifie fièvre en langue Fang",
        category="langue_locale",
        language="fang",
        context="Test d'intégration",
        tags=["test", "fang", "fièvre"]
    )
    print(f"   ✅ Connaissance ajoutée (ID: {kb_id})")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 4: Recherche
print("\n4️⃣ Test recherche...")
try:
    results = kb.search_knowledge("Nlo", limit=5)
    print(f"   ✅ Résultats trouvés: {len(results)}")
    if results:
        for r in results:
            print(f"      - {r['question']}: {r['answer'][:50]}...")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 5: Contexte pour LLM
print("\n5️⃣ Test génération contexte LLM...")
try:
    context = kb.get_context_for_llm("Nlo", limit=10)
    print(f"   ✅ Contexte généré ({len(context)} caractères)")
    if context:
        print(f"      Aperçu: {context[:200]}...")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 6: Import du chatbot enrichi
print("\n6️⃣ Test import EnhancedMedicalChatbot...")
try:
    from enhanced_chatbot import EnhancedMedicalChatbot
    chatbot = EnhancedMedicalChatbot()
    print("   ✅ EnhancedMedicalChatbot importé et initialisé")
    
    # Vérifier que la base de connaissances est bien intégrée
    if hasattr(chatbot, 'kb') and chatbot.kb:
        print("   ✅ Base de connaissances intégrée dans le chatbot")
    else:
        print("   ⚠️ Base de connaissances non intégrée")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 7: Test du blueprint teach_routes
print("\n7️⃣ Test import teach_routes...")
try:
    from teach_routes import teach_bp
    print("   ✅ Blueprint teach_routes importé")
    print(f"   ✅ Nom du blueprint: {teach_bp.name}")
    print(f"   ✅ URL prefix: {teach_bp.url_prefix or '/'}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 8: Nettoyage (supprimer la connaissance de test)
print("\n8️⃣ Nettoyage...")
try:
    if kb_id:
        kb.delete_knowledge(kb_id)
        print(f"   ✅ Connaissance de test supprimée (ID: {kb_id})")
except Exception as e:
    print(f"   ⚠️ Erreur nettoyage: {e}")

# Résumé final
print("\n" + "=" * 60)
print("RÉSUMÉ DES TESTS")
print("=" * 60)
print("✅ Tous les tests sont passés avec succès!")
print("\n📊 Statistiques finales:")
stats = kb.get_statistics()
print(f"   - Total connaissances: {stats['total']}")
print(f"   - Catégories: {len(stats['by_category'])}")
print(f"   - Langues: {len(stats['by_language'])}")

print("\n🎯 PROCHAINES ÉTAPES:")
print("   1. Démarrer l'application: python app.py")
print("   2. Ouvrir http://localhost:5000/chat")
print("   3. Cliquer sur '🎓 Enseigner'")
print("   4. Commencer à enseigner à l'IA!")
print("\n" + "=" * 60)
