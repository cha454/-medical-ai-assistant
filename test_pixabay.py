"""
Test de la clé API Pixabay
"""

import requests

def test_pixabay_key(api_key):
    """Teste si la clé API Pixabay est valide"""
    
    print(f"🔍 Test de la clé Pixabay: {api_key[:10]}...")
    
    try:
        url = "https://pixabay.com/api/"
        params = {
            "key": api_key,
            "q": "nature",  # Recherche simple
            "per_page": 3,
            "safesearch": "true"
        }
        
        print("📤 Envoi de la requête à Pixabay...")
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📥 Code de réponse: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total_hits = data.get("totalHits", 0)
            hits = len(data.get("hits", []))
            
            print(f"✅ CLÉ VALIDE !")
            print(f"✅ {total_hits} images trouvées au total")
            print(f"✅ {hits} images retournées")
            
            if hits > 0:
                print("\n📸 Première image:")
                first_image = data["hits"][0]
                print(f"   - ID: {first_image.get('id')}")
                print(f"   - Tags: {first_image.get('tags')}")
                print(f"   - URL: {first_image.get('webformatURL')}")
                print(f"   - Dimensions: {first_image.get('imageWidth')}x{first_image.get('imageHeight')}")
            
            return True
            
        elif response.status_code == 400:
            print("❌ CLÉ INVALIDE - Erreur 400")
            print(f"   Message: {response.text}")
            return False
            
        elif response.status_code == 429:
            print("⚠️ LIMITE DÉPASSÉE - Erreur 429")
            print("   Vous avez dépassé la limite de 5000 requêtes/heure")
            return False
            
        else:
            print(f"❌ ERREUR {response.status_code}")
            print(f"   Message: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - La requête a pris trop de temps")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ ERREUR DE CONNEXION - Vérifiez votre connexion internet")
        return False
        
    except Exception as e:
        print(f"❌ ERREUR INATTENDUE: {e}")
        return False

if __name__ == "__main__":
    # Clé à tester
    api_key = "u_uk9zov7h5f"
    
    print("=" * 60)
    print("🖼️  TEST DE CLÉ API PIXABAY")
    print("=" * 60)
    print()
    
    result = test_pixabay_key(api_key)
    
    print()
    print("=" * 60)
    if result:
        print("✅ RÉSULTAT: La clé est VALIDE et fonctionne !")
        print()
        print("📝 PROCHAINES ÉTAPES:")
        print("1. Ajoutez cette clé dans Render:")
        print("   - Key: PIXABAY_API_KEY")
        print(f"   - Value: {api_key}")
        print("2. Redéployez votre application")
        print("3. Testez: 'Montre-moi une image de la tour Eiffel'")
    else:
        print("❌ RÉSULTAT: La clé est INVALIDE ou a un problème")
        print()
        print("💡 SOLUTIONS:")
        print("1. Vérifiez que vous avez copié la clé complète")
        print("2. Allez sur https://pixabay.com/api/docs/")
        print("3. Vérifiez que votre compte est actif")
        print("4. Générez une nouvelle clé si nécessaire")
    print("=" * 60)
