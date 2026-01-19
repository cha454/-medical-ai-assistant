"""
Script de test pour les nouvelles fonctionnalités
- OpenWeather API (Météo)
- OpenAI API (Recherches poussées)
"""

import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_weather_service():
    """Test du service météo OpenWeather"""
    print("\n" + "="*60)
    print("🌤️  TEST SERVICE MÉTÉO OPENWEATHER")
    print("="*60)
    
    try:
        from weather_service import weather_service
        
        if not weather_service.is_available():
            print("❌ Service météo non disponible")
            print("💡 Configurez OPENWEATHER_API_KEY dans .env")
            return False
        
        print("✅ Service météo disponible")
        
        # Test météo Paris
        print("\n📍 Test: Météo à Paris")
        result = weather_service.get_weather("Paris", "FR")
        
        if "error" in result:
            print(f"❌ Erreur: {result['message']}")
            return False
        
        print(f"✅ Ville: {result['location']['city']}, {result['location']['country']}")
        print(f"🌡️  Température: {result['current']['temperature']}{result['current']['temp_unit']}")
        print(f"☁️  Conditions: {result['current']['description']}")
        print(f"💧 Humidité: {result['current']['humidity']}%")
        print(f"💨 Vent: {result['wind']['speed']} {result['wind']['speed_unit']}")
        
        # Test résumé météo
        print("\n📝 Test: Résumé météo")
        summary = weather_service.get_weather_summary("Paris", "FR")
        print(summary[:200] + "...")
        
        print("\n✅ Service météo fonctionne parfaitement!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test météo: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_provider():
    """Test du provider LLM (OpenAI/Gemini)"""
    print("\n" + "="*60)
    print("🤖 TEST PROVIDER LLM (OpenAI/Gemini)")
    print("="*60)
    
    try:
        from llm_provider import llm
        
        if not llm.is_available():
            print("❌ Aucun LLM disponible")
            print("💡 Configurez au moins une clé API:")
            print("   - GOOGLE_API_KEY (gratuit)")
            print("   - OPENAI_API_KEY (payant)")
            print("   - GROQ_API_KEY (gratuit)")
            return False
        
        provider_info = llm.get_provider_info()
        print(f"✅ LLM disponible: {provider_info.get('name', 'Inconnu')}")
        print(f"📊 Modèle: {provider_info.get('model', 'Inconnu')}")
        print(f"⚡ Vitesse: {provider_info.get('speed', 'Inconnu')}")
        print(f"💰 Coût: {provider_info.get('cost', 'Inconnu')}")
        
        # Test simple
        print("\n💬 Test: Question simple")
        response = llm.generate_response("Bonjour, comment ça va ?", language="fr")
        
        if response:
            print(f"✅ Réponse reçue ({len(response)} caractères)")
            print(f"📝 Aperçu: {response[:150]}...")
        else:
            print("❌ Pas de réponse du LLM")
            return False
        
        print("\n✅ Provider LLM fonctionne parfaitement!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test LLM: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_chatbot():
    """Test du chatbot enrichi avec météo"""
    print("\n" + "="*60)
    print("💬 TEST CHATBOT ENRICHI")
    print("="*60)
    
    try:
        from enhanced_chatbot import EnhancedMedicalChatbot
        
        chatbot = EnhancedMedicalChatbot()
        print("✅ Chatbot initialisé")
        
        # Test demande météo
        print("\n🌤️  Test: Demande météo")
        response = chatbot.process_message("Quelle est la météo à Paris ?", "fr")
        print(f"📝 Réponse ({len(response)} caractères):")
        print(response[:300] + "...")
        
        # Test recherche poussée
        print("\n🔍 Test: Recherche poussée")
        response = chatbot.process_message("Fais une recherche poussée sur le diabète", "fr")
        print(f"📝 Réponse ({len(response)} caractères):")
        print(response[:300] + "...")
        
        print("\n✅ Chatbot enrichi fonctionne parfaitement!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test chatbot: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("\n" + "="*60)
    print("🧪 TEST DES NOUVELLES FONCTIONNALITÉS")
    print("="*60)
    
    # Vérifier les variables d'environnement
    print("\n📋 Variables d'environnement:")
    print(f"   OPENWEATHER_API_KEY: {'✅ Configurée' if os.getenv('OPENWEATHER_API_KEY') else '❌ Manquante'}")
    print(f"   GOOGLE_API_KEY: {'✅ Configurée' if os.getenv('GOOGLE_API_KEY') else '❌ Manquante'}")
    print(f"   OPENAI_API_KEY: {'✅ Configurée' if os.getenv('OPENAI_API_KEY') else '❌ Manquante'}")
    print(f"   GROQ_API_KEY: {'✅ Configurée' if os.getenv('GROQ_API_KEY') else '❌ Manquante'}")
    
    # Exécuter les tests
    results = {
        "Météo": test_weather_service(),
        "LLM": test_llm_provider(),
        "Chatbot": test_enhanced_chatbot()
    }
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    total_success = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 Score: {total_success}/{total_tests} tests réussis")
    
    if total_success == total_tests:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("✅ Votre application est prête à être déployée sur Render")
    else:
        print("\n⚠️  Certains tests ont échoué")
        print("💡 Vérifiez les clés API dans votre fichier .env")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
