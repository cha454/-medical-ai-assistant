"""
Script de test pour la recherche Google Custom Search
"""

import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web_search import web_search

def test_google_search():
    """Test de la recherche Google"""
    
    print("=" * 60)
    print("TEST DE LA RECHERCHE WEB")
    print("=" * 60)
    
    # Vérifier la configuration
    google_api_key = os.environ.get('GOOGLE_SEARCH_API_KEY')
    google_cx = os.environ.get('GOOGLE_SEARCH_CX')
    
    print("\n📋 Configuration:")
    print(f"   Google API Key: {'✓ Configurée' if google_api_key else '✗ Non configurée'}")
    print(f"   Google CX: {'✓ Configurée' if google_cx else '✗ Non configurée'}")
    
    if google_api_key and google_cx:
        print("\n✅ Google Custom Search est activé!")
    else:
        print("\n⚠️  Google Custom Search non configuré")
        print("   L'assistant utilisera Wikipedia, DuckDuckGo et PubMed")
        print("\n   Pour activer Google Search:")
        print("   1. Voir GOOGLE_SEARCH_SETUP.md")
        print("   2. Ajouter GOOGLE_SEARCH_API_KEY et GOOGLE_SEARCH_CX dans .env")
    
    # Test de recherche
    print("\n" + "=" * 60)
    print("TEST DE RECHERCHE")
    print("=" * 60)
    
    queries = [
        "symptômes du diabète",
        "COVID-19 prévention",
        "aspirine effets secondaires"
    ]
    
    for query in queries:
        print(f"\n🔍 Recherche: {query}")
        print("-" * 60)
        
        results = web_search.search_medical_info(query, "fr")
        
        if results and results.get("sources"):
            print(f"✓ {len(results['sources'])} sources trouvées:")
            
            for i, source in enumerate(results["sources"][:3], 1):
                print(f"\n   {i}. {source.get('source', 'Source')} ({source.get('reliability', 'medium')})")
                print(f"      Titre: {source.get('title', 'N/A')[:80]}")
                if source.get('url'):
                    print(f"      URL: {source['url']}")
        else:
            print("✗ Aucun résultat trouvé")
    
    print("\n" + "=" * 60)
    print("FIN DES TESTS")
    print("=" * 60)

if __name__ == "__main__":
    test_google_search()
