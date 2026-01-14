"""
Script pour tester quels modèles Gemini sont disponibles
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('GOOGLE_API_KEY', 'AIzaSyAjkUMIWhGpJQ-CToduhDAXDd9mEFhCjJU')

print(f"🔑 Clé API: {api_key[:20]}...")
print("\n" + "="*60)
print("TEST DES MODÈLES GEMINI DISPONIBLES")
print("="*60 + "\n")

# Liste des modèles à tester
models_to_test = [
    "gemini-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
]

versions = ["v1beta", "v1"]

for version in versions:
    print(f"\n📋 Version API: {version}")
    print("-" * 60)
    
    for model in models_to_test:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"
        
        data = {
            "contents": [{
                "parts": [{"text": "Bonjour"}]
            }]
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {model}: FONCTIONNE")
            elif response.status_code == 404:
                print(f"❌ {model}: Non trouvé (404)")
            else:
                print(f"⚠️  {model}: Erreur {response.status_code}")
                
        except Exception as e:
            print(f"❌ {model}: Exception - {e}")

print("\n" + "="*60)
print("FIN DES TESTS")
print("="*60)
