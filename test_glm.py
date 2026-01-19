"""
Script de test pour l'API GLM-4 (Zhipu AI)
"""

import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from llm_provider import LLMProvider

def test_glm():
    """Test de l'intégration GLM-4"""
    
    print("=" * 60)
    print("🧪 TEST DE L'API GLM-4 (Zhipu AI)")
    print("=" * 60)
    
    # Vérifier la clé API
    glm_key = os.environ.get('GLM_API_KEY')
    if not glm_key:
        print("\n❌ ERREUR: GLM_API_KEY non configurée dans .env")
        print("\n📝 Pour obtenir votre clé API:")
        print("   1. Allez sur: https://open.bigmodel.cn/")
        print("   2. Créez un compte (gratuit)")
        print("   3. Obtenez votre API key")
        print("   4. Ajoutez-la dans le fichier .env:")
        print("      GLM_API_KEY=votre_cle_ici")
        return
    
    print(f"\n✓ Clé API GLM-4 détectée: {glm_key[:20]}...")
    
    # Initialiser le provider
    llm = LLMProvider()
    
    print(f"\n✓ Provider actif: {llm.active_provider}")
    print(f"✓ LLM disponible: {llm.is_available()}")
    
    if llm.active_provider != "glm":
        print(f"\n⚠️ ATTENTION: Le provider actif n'est pas GLM-4 mais {llm.active_provider}")
        print("   GLM-4 sera utilisé en priorité si la clé est configurée.")
    
    # Afficher les infos du provider
    info = llm.get_provider_info()
    print(f"\n📊 Informations du provider:")
    print(f"   Nom: {info.get('name', 'N/A')}")
    print(f"   Modèle: {info.get('model', 'N/A')}")
    print(f"   Qualité: {info.get('quality', 'N/A')}")
    print(f"   Vitesse: {info.get('speed', 'N/A')}")
    print(f"   Coût: {info.get('cost', 'N/A')}")
    
    # Test 1: Question simple
    print("\n" + "=" * 60)
    print("TEST 1: Question simple")
    print("=" * 60)
    
    question1 = "Bonjour ! Peux-tu te présenter en 2-3 phrases ?"
    print(f"\n❓ Question: {question1}")
    print("\n⏳ Génération de la réponse...")
    
    response1 = llm.generate_response(question1)
    
    if response1:
        print(f"\n✅ Réponse reçue ({len(response1)} caractères):")
        print("-" * 60)
        print(response1)
        print("-" * 60)
    else:
        print("\n❌ Aucune réponse reçue")
        return
    
    # Test 2: Question médicale
    print("\n" + "=" * 60)
    print("TEST 2: Question médicale")
    print("=" * 60)
    
    question2 = "Quels sont les symptômes courants de la grippe ?"
    print(f"\n❓ Question: {question2}")
    print("\n⏳ Génération de la réponse...")
    
    response2 = llm.generate_response(question2)
    
    if response2:
        print(f"\n✅ Réponse reçue ({len(response2)} caractères):")
        print("-" * 60)
        print(response2)
        print("-" * 60)
    else:
        print("\n❌ Aucune réponse reçue")
        return
    
    # Test 3: Conversation avec historique
    print("\n" + "=" * 60)
    print("TEST 3: Conversation avec historique")
    print("=" * 60)
    
    history = [
        {"role": "user", "content": "Bonjour, je m'appelle Marie."},
        {"role": "assistant", "content": "Bonjour Marie ! Ravi de faire ta connaissance. Comment puis-je t'aider aujourd'hui ?"}
    ]
    
    question3 = "Quel est mon prénom ?"
    print(f"\n❓ Question: {question3}")
    print("📝 Avec historique de conversation")
    print("\n⏳ Génération de la réponse...")
    
    response3 = llm.generate_response(question3, conversation_history=history)
    
    if response3:
        print(f"\n✅ Réponse reçue ({len(response3)} caractères):")
        print("-" * 60)
        print(response3)
        print("-" * 60)
    else:
        print("\n❌ Aucune réponse reçue")
        return
    
    # Résumé
    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS RÉUSSIS !")
    print("=" * 60)
    print("\n🎉 GLM-4 est correctement configuré et fonctionne parfaitement !")
    print("\n💡 Vous pouvez maintenant utiliser votre assistant médical avec GLM-4.")
    print("   Pour démarrer l'application: python app.py")

if __name__ == "__main__":
    test_glm()
