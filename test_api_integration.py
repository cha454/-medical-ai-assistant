"""
Script de test pour vérifier toutes les intégrations API
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from api_integration import api_integration
import json

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_service_status():
    print_section("TEST 1: Statut des Services")
    
    status = api_integration.get_service_status()
    print("\n📊 Statut des services:")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    available = api_integration.get_available_services()
    print(f"\n✅ Services disponibles: {available}")
    print(f"📈 Total actifs: {len(available)}/{len(status)}")

def test_web_search():
    print_section("TEST 2: Recherche Web")
    
    if not api_integration.is_service_available('web_search'):
        print("⚠️ Service de recherche web non disponible")
        return
    
    print("\n🔍 Recherche: 'diabète'")
    result = api_integration.search_medical_info("diabète", "fr")
    
    if result.get('success'):
        print(f"✅ Trouvé {len(result['results'].get('sources', []))} sources")
        if result['results'].get('summary'):
            print(f"\n📝 Résumé: {result['results']['summary'][:200]}...")
    else:
        print(f"❌ Erreur: {result.get('error')}")

def test_llm():
    print_section("TEST 3: LLM (Intelligence Artificielle)")
    
    if not api_integration.is_service_available('llm'):
        print("⚠️ LLM non configuré")
        print("💡 Configurez une clé API dans .env:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print("   - GOOGLE_API_KEY")
        print("   - MISTRAL_API_KEY")
        return
    
    print("\n🤖 Test génération de texte...")
    result = api_integration.generate_llm_response(
        "Explique le diabète en 2 phrases",
        language="fr"
    )
    
    if result.get('success'):
        print(f"✅ Provider: {result.get('provider')}")
        print(f"📝 Réponse: {result['response'][:200]}...")
    else:
        print(f"❌ Erreur: {result.get('error')}")

def test_email():
    print_section("TEST 4: Service Email")
    
    if not api_integration.is_service_available('email'):
        print("⚠️ Service email non configuré")
        print("💡 Configurez dans .env:")
        print("   Option 1 (Recommandé): SENDGRID_API_KEY")
        print("   Option 2: SMTP_USER et SMTP_PASSWORD")
        return
    
    email_service = api_integration.services['email']['instance']
    print(f"✅ Provider: {email_service.provider}")
    print(f"📧 Email expéditeur: {email_service.sender_email}")
    print("\n💡 Pour tester l'envoi, utilisez l'endpoint /api/email/send")

def test_image_analyzer():
    print_section("TEST 5: Analyse d'Images")
    
    if not api_integration.is_service_available('image_analyzer'):
        print("⚠️ Service d'analyse d'images non disponible")
        print("💡 Nécessite TensorFlow et un modèle entraîné")
        return
    
    print("✅ Service d'analyse d'images disponible")
    print("💡 Utilisez l'endpoint /api/image/analyze pour tester")

def test_integration_info():
    print_section("TEST 6: Informations Complètes")
    
    info = api_integration.get_integration_info()
    print("\n📊 Résumé:")
    print(f"   Total services: {info['total_services']}")
    print(f"   Services actifs: {info['active_services']}")
    print(f"   Timestamp: {info['timestamp']}")

def main():
    print("\n" + "🏥 "*20)
    print("   TEST D'INTÉGRATION API - ASSISTANT MÉDICAL IA")
    print("🏥 "*20)
    
    # Exécuter tous les tests
    test_service_status()
    test_web_search()
    test_llm()
    test_email()
    test_image_analyzer()
    test_integration_info()
    
    # Résumé final
    print_section("RÉSUMÉ")
    available = api_integration.get_available_services()
    total = len(api_integration.services)
    
    print(f"\n✅ Services opérationnels: {len(available)}/{total}")
    
    if len(available) == total:
        print("\n🎉 Toutes les intégrations sont fonctionnelles!")
    elif len(available) > 0:
        print("\n⚠️ Certains services nécessitent une configuration")
        print("📖 Consultez .env.example pour les clés API requises")
    else:
        print("\n❌ Aucun service externe configuré")
        print("💡 L'application fonctionnera en mode de base")
    
    print("\n📚 Documentation complète: API_DOCUMENTATION.md")
    print("🚀 Démarrer l'app: python app.py")
    print("\n")

if __name__ == "__main__":
    main()
