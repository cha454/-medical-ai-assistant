"""
Module de recherche d'images médicales sur le web
Supporte: Google Images, Bing Images, Unsplash, Pixabay
"""

import requests
import os
from urllib.parse import quote
from typing import List, Dict, Any

class MedicalImageSearch:
    def __init__(self):
        # Clés API
        self.google_api_key = os.environ.get('GOOGLE_SEARCH_API_KEY')
        self.google_cx = os.environ.get('GOOGLE_SEARCH_CX')
        self.bing_api_key = os.environ.get('BING_SEARCH_API_KEY')
        self.unsplash_api_key = os.environ.get('UNSPLASH_ACCESS_KEY')
        self.pixabay_api_key = os.environ.get('PIXABAY_API_KEY')
        
        # Mots-clés pour détecter une demande d'image
        self.image_keywords = [
            "image", "photo", "picture", "img", "illustration",
            "montre-moi", "montre moi", "voir", "affiche", "afficher",
            "à quoi ressemble", "ressemble", "apparence", "aspect"
        ]
    
    def is_image_request(self, text: str) -> bool:
        """Détecte si l'utilisateur demande une image"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.image_keywords)
    
    def search_images(self, query: str, max_results: int = 6) -> Dict[str, Any]:
        """Recherche des images médicales"""
        results = {
            "query": query,
            "images": [],
            "source": None
        }
        
        # Essayer Google Images en priorité
        if self.google_api_key and self.google_cx:
            google_images = self._search_google_images(query, max_results)
            if google_images:
                results["images"] = google_images
                results["source"] = "Google Images"
                return results
        
        # Essayer Bing Images
        if self.bing_api_key:
            bing_images = self._search_bing_images(query, max_results)
            if bing_images:
                results["images"] = bing_images
                results["source"] = "Bing Images"
                return results
        
        # Essayer Unsplash (photos de qualité)
        if self.unsplash_api_key:
            unsplash_images = self._search_unsplash(query, max_results)
            if unsplash_images:
                results["images"] = unsplash_images
                results["source"] = "Unsplash"
                return results
        
        # Essayer Pixabay (gratuit, pas de clé requise pour certaines requêtes)
        if self.pixabay_api_key:
            pixabay_images = self._search_pixabay(query, max_results)
            if pixabay_images:
                results["images"] = pixabay_images
                results["source"] = "Pixabay"
                return results
        
        return results
    
    def _search_google_images(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Recherche sur Google Images API"""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_api_key,
                "cx": self.google_cx,
                "q": query,
                "searchType": "image",
                "num": min(max_results, 10),
                "safe": "active",  # Filtrage contenu
                "imgSize": "medium"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for item in data.get("items", []):
                    images.append({
                        "url": item.get("link"),
                        "thumbnail": item.get("image", {}).get("thumbnailLink"),
                        "title": item.get("title", ""),
                        "source_url": item.get("image", {}).get("contextLink", ""),
                        "width": item.get("image", {}).get("width"),
                        "height": item.get("image", {}).get("height")
                    })
                
                print(f"✓ Google Images: {len(images)} images trouvées")
                return images
            else:
                print(f"Google Images API Error: {response.status_code}")
                if response.status_code == 429:
                    print("⚠️ Limite de requêtes Google atteinte")
        except Exception as e:
            print(f"Google Images search error: {e}")
        return []
    
    def _search_bing_images(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Recherche sur Bing Images API"""
        try:
            url = "https://api.bing.microsoft.com/v7.0/images/search"
            headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
            params = {
                "q": query,
                "count": min(max_results, 50),
                "safeSearch": "Strict",
                "imageType": "Photo"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for item in data.get("value", []):
                    images.append({
                        "url": item.get("contentUrl"),
                        "thumbnail": item.get("thumbnailUrl"),
                        "title": item.get("name", ""),
                        "source_url": item.get("hostPageUrl", ""),
                        "width": item.get("width"),
                        "height": item.get("height")
                    })
                
                print(f"✓ Bing Images: {len(images)} images trouvées")
                return images
            else:
                print(f"Bing Images API Error: {response.status_code}")
        except Exception as e:
            print(f"Bing Images search error: {e}")
        return []
    
    def _search_unsplash(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Recherche sur Unsplash API"""
        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {self.unsplash_api_key}"}
            params = {
                "query": query,
                "per_page": min(max_results, 30),
                "orientation": "landscape"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for item in data.get("results", []):
                    images.append({
                        "url": item.get("urls", {}).get("regular"),
                        "thumbnail": item.get("urls", {}).get("thumb"),
                        "title": item.get("description") or item.get("alt_description", ""),
                        "source_url": item.get("links", {}).get("html", ""),
                        "width": item.get("width"),
                        "height": item.get("height"),
                        "photographer": item.get("user", {}).get("name", "")
                    })
                
                print(f"✓ Unsplash: {len(images)} images trouvées")
                return images
            else:
                print(f"Unsplash API Error: {response.status_code}")
        except Exception as e:
            print(f"Unsplash search error: {e}")
        return []
    
    def _search_pixabay(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Recherche sur Pixabay API"""
        try:
            url = "https://pixabay.com/api/"
            params = {
                "key": self.pixabay_api_key,
                "q": query,
                "per_page": min(max_results, 200),
                "safesearch": "true",
                "image_type": "photo"
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for item in data.get("hits", []):
                    images.append({
                        "url": item.get("largeImageURL"),
                        "thumbnail": item.get("previewURL"),
                        "title": item.get("tags", ""),
                        "source_url": item.get("pageURL", ""),
                        "width": item.get("imageWidth"),
                        "height": item.get("imageHeight"),
                        "photographer": item.get("user", "")
                    })
                
                print(f"✓ Pixabay: {len(images)} images trouvées")
                return images
            else:
                print(f"Pixabay API Error: {response.status_code}")
        except Exception as e:
            print(f"Pixabay search error: {e}")
        return []
    
    def format_image_results(self, results: Dict[str, Any]) -> str:
        """Formate les résultats de recherche d'images pour affichage"""
        if not results or not results.get("images"):
            return "❌ Aucune image trouvée pour cette recherche."
        
        images = results["images"]
        source = results.get("source", "Web")
        
        formatted = f"""🖼️ **{len(images)} images trouvées** (source: {source})

**Recherche:** {results.get('query', '')}

"""
        
        for i, img in enumerate(images[:6], 1):  # Maximum 6 images
            formatted += f"""**Image {i}:**
- 📸 Titre: {img.get('title', 'Sans titre')[:100]}
- 🔗 URL: {img.get('url', '')}
- 📏 Dimensions: {img.get('width', '?')}x{img.get('height', '?')}
"""
            if img.get('photographer'):
                formatted += f"- 👤 Photographe: {img['photographer']}\n"
            formatted += "\n"
        
        formatted += """
⚠️ **Note importante:**
- Ces images proviennent du web et sont à but éducatif uniquement
- Pour un diagnostic médical, consultez toujours un professionnel de santé
- Vérifiez les droits d'utilisation avant toute réutilisation
"""
        
        return formatted
    
    def extract_query_from_request(self, text: str) -> str:
        """Extrait la requête de recherche d'image du texte"""
        text_lower = text.lower()
        
        # Patterns courants
        patterns = [
            "image de ", "image d'", "image du ", "image des ",
            "photo de ", "photo d'", "photo du ", "photo des ",
            "montre-moi ", "montre moi ",
            "voir ", "affiche ", "afficher ",
            "à quoi ressemble ", "ressemble "
        ]
        
        for pattern in patterns:
            if pattern in text_lower:
                # Extraire ce qui vient après le pattern
                query = text_lower.split(pattern, 1)[1].strip()
                # Nettoyer
                query = query.rstrip('?!.,;')
                return query
        
        # Si aucun pattern trouvé, retourner le texte complet
        return text.strip()

# Instance globale
image_search = MedicalImageSearch()

# Test
if __name__ == "__main__":
    searcher = MedicalImageSearch()
    
    # Test détection
    print("=== Test Détection ===")
    print(searcher.is_image_request("Montre-moi une image du cœur"))  # True
    print(searcher.is_image_request("Qu'est-ce que le diabète?"))  # False
    
    # Test extraction
    print("\n=== Test Extraction ===")
    print(searcher.extract_query_from_request("Montre-moi une image du cœur humain"))
    print(searcher.extract_query_from_request("Photo de poumons"))
