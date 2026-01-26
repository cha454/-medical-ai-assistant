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
        
        # Mots-clés pour détecter une demande d'image (RECHERCHE uniquement)
        self.image_keywords = [
            "image", "photo", "picture", "img", "illustration",
            "montre-moi", "montre moi", "voir", "affiche", "afficher",
            "à quoi ressemble", "ressemble", "apparence", "aspect",
            "trouve", "trouve-moi", "trouve moi",
            "cherche", "cherche-moi", "cherche moi"
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
        
        # Traduction simple français -> anglais pour mots courants
        translations = {
            "chat": "cat",
            "chien": "dog",
            "cœur": "heart",
            "coeur": "heart",
            "poumons": "lungs",
            "poumon": "lung",
            "cerveau": "brain",
            "foie": "liver",
            "rein": "kidney",
            "reins": "kidneys",
            "estomac": "stomach",
            "intestin": "intestine",
            "os": "bone",
            "muscle": "muscle",
            "sang": "blood",
            "peau": "skin",
            "œil": "eye",
            "oeil": "eye",
            "yeux": "eyes",
            "oreille": "ear",
            "nez": "nose",
            "bouche": "mouth",
            "dent": "tooth",
            "dents": "teeth",
            "main": "hand",
            "pied": "foot",
            "jambe": "leg",
            "bras": "arm",
            "tête": "head",
            "tete": "head",
            "corps": "body",
            "cellule": "cell",
            "cellules": "cells",
            "virus": "virus",
            "bactérie": "bacteria",
            "bacterie": "bacteria",
            "maladie": "disease",
            "symptôme": "symptom",
            "symptome": "symptom",
            "traitement": "treatment",
            "médicament": "medicine",
            "medicament": "medicine",
            "hôpital": "hospital",
            "hopital": "hospital",
            "médecin": "doctor",
            "medecin": "doctor",
            "infirmière": "nurse",
            "infirmiere": "nurse",
            "patient": "patient",
            "chirurgie": "surgery",
            "opération": "operation",
            "operation": "operation",
            "radiographie": "x-ray",
            "scanner": "ct scan",
            "irm": "mri",
            "échographie": "ultrasound",
            "echographie": "ultrasound",
            "fracture": "fracture",
            "blessure": "injury",
            "douleur": "pain",
            "fièvre": "fever",
            "fievre": "fever",
            "toux": "cough",
            "rhume": "cold",
            "grippe": "flu",
            "diabète": "diabetes",
            "diabete": "diabetes",
            "cancer": "cancer",
            "tumeur": "tumor",
            "infection": "infection",
            "inflammation": "inflammation",
            "allergie": "allergy",
            "asthme": "asthma",
            "hypertension": "hypertension",
            "cholestérol": "cholesterol",
            "cholesterol": "cholesterol"
        }

        # Traduire la requête si c'est un mot français courant
        search_query = query.lower().strip()
        print(f"🔍 Requête originale: '{query}' → '{search_query}'")
        
        # Animaux courants (FR -> EN)
        animal_translations = {
            "mouton": "sheep",
            "brebis": "ewe",
            "agneau": "lamb",
            "chèvre": "goat",
            "chevre": "goat",
            "bouc": "goat"
        }
        # Fusionner
        translations.update(animal_translations)
        
        # Vérifier si la requête contient un mot à traduire
        translated = False
        for fr_word, en_word in translations.items():
            if fr_word in search_query:
                search_query = search_query.replace(fr_word, en_word)
                translated = True
        
        if translated:
            print(f"🌍 Traduction: '{query}' → '{search_query}'")
        
        # Essayer Google Images en priorité
        if self.google_api_key and self.google_cx:
            google_images = self._search_google_images(search_query, max_results)
            if google_images:
                results["images"] = google_images
                results["source"] = "Google Images"
                return results
        
        # Essayer Bing Images
        if self.bing_api_key:
            bing_images = self._search_bing_images(search_query, max_results)
            if bing_images:
                results["images"] = bing_images
                results["source"] = "Bing Images"
                return results
        
        # Essayer Unsplash (photos de qualité)
        if self.unsplash_api_key:
            unsplash_images = self._search_unsplash(search_query, max_results)
            if unsplash_images:
                results["images"] = unsplash_images
                results["source"] = "Unsplash"
                return results
        
        # Essayer Pixabay (gratuit, pas de clé requise pour certaines requêtes)
        if self.pixabay_api_key:
            pixabay_images = self._search_pixabay(search_query, max_results)
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
            # Catégorie animaux si la requête correspond à un animal
            animal_keywords = {
                "sheep", "ewe", "lamb", "goat", "horse", "cow", "dog", "cat", "pig",
                "chicken", "duck", "camel", "bird", "mouton", "chèvre", "chevre",
                "cheval", "vache", "chien", "chat", "porc", "poulet", "canard"
            }
            params = {
                "key": self.pixabay_api_key,
                "q": query,
                "per_page": min(max_results, 200),
                "safesearch": "true",
                "image_type": "photo"
            }
            if query.lower() in animal_keywords:
                params["category"] = "animals"
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                images = []
                
                # Filtrer les résultats pour s'assurer qu'ils correspondent à la requête
                query_words = set(query.lower().split())
                
                for item in data.get("hits", []):
                    # Vérifier que les tags contiennent au moins un mot de la requête
                    tags = item.get("tags", "").lower()
                    tags_words = set(tags.replace(",", " ").split())
                    
                    # Si la requête est un animal, vérifier que les tags correspondent
                    if query.lower() in animal_keywords:
                        # Pour les animaux, être plus strict sur la correspondance
                        if query.lower() in tags or any(word in tags for word in query_words):
                            images.append({
                                "url": item.get("largeImageURL"),
                                "thumbnail": item.get("previewURL"),
                                "title": item.get("tags", ""),
                                "source_url": item.get("pageURL", ""),
                                "width": item.get("imageWidth"),
                                "height": item.get("imageHeight"),
                                "photographer": item.get("user", "")
                            })
                    else:
                        # Pour les autres requêtes, accepter si au moins un mot correspond
                        if query_words & tags_words:
                            images.append({
                                "url": item.get("largeImageURL"),
                                "thumbnail": item.get("previewURL"),
                                "title": item.get("tags", ""),
                                "source_url": item.get("pageURL", ""),
                                "width": item.get("imageWidth"),
                                "height": item.get("imageHeight"),
                                "photographer": item.get("user", "")
                            })
                
                print(f"✓ Pixabay: {len(images)} images trouvées (filtrées de {len(data.get('hits', []))} résultats)")
                return images[:max_results]  # Limiter au nombre demandé
            else:
                print(f"Pixabay API Error: {response.status_code}")
        except Exception as e:
            print(f"Pixabay search error: {e}")
        return []
    
    def format_image_results(self, results: Dict[str, Any]) -> str:
        """Formate les résultats de recherche d'images pour affichage avec images intégrées"""
        if not results or not results.get("images"):
            return "❌ Aucune image trouvée pour cette recherche."
        
        images = results["images"]
        source = results.get("source", "Web")
        
        # Utiliser HTML pour afficher les images directement
        formatted = f"""🖼️ **{len(images)} images trouvées** (source: {source})

**Recherche:** {results.get('query', '')}

---

"""
        
        for i, img in enumerate(images[:6], 1):  # Maximum 6 images
            img_url = img.get('url', '')
            thumbnail = img.get('thumbnail', img_url)  # Utiliser thumbnail si disponible
            title = img.get('title', 'Sans titre')[:100]
            width = img.get('width', '?')
            height = img.get('height', '?')
            photographer = img.get('photographer', '')
            source_url = img.get('source_url', '')
            
            # Afficher l'image directement avec HTML
            formatted += f"""**Image {i}:** {title}

<img src="{img_url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" loading="lazy" />

"""
            
            # Informations supplémentaires
            formatted += f"📏 **Dimensions:** {width}x{height}\n"
            if photographer:
                formatted += f"👤 **Photographe:** {photographer}\n"
            if source_url:
                formatted += f"🔗 **Source:** [Voir sur {source}]({source_url})\n"
            formatted += "\n---\n\n"
        
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
        
        # Patterns courants pour RECHERCHE d'images (ordre important: plus spécifiques en premier)
        patterns = [
            "trouve-moi un ", "trouve moi un ", "trouve-moi une ", "trouve moi une ",
            "trouve un ", "trouve une ",
            "cherche-moi un ", "cherche moi un ", "cherche-moi une ", "cherche moi une ",
            "cherche un ", "cherche une ",
            "je veux les images d'un ", "je veux les images d'une ", "je veux les images du ", "je veux les images de la ", "je veux les images de ",
            "je veux une image d'un ", "je veux une image d'une ", "je veux une image du ", "je veux une image de la ", "je veux une image de ",
            "je veux des images d'un ", "je veux des images d'une ", "je veux des images du ", "je veux des images de la ", "je veux des images de ",
            "montre-moi une image de ", "montre moi une image de ", "montre-moi des images de ", "montre moi des images de ",
            "montre-moi une image d'", "montre moi une image d'", "montre-moi des images d'", "montre moi des images d'",
            "montre-moi ", "montre moi ",
            "image de ", "image d'", "image du ", "image des ", "image d ", "image un ",
            "images de ", "images d'", "images du ", "images des ", "images d ", "images un ",
            "photo de ", "photo d'", "photo du ", "photo des ", "photo d ", "photo un ",
            "photos de ", "photos d'", "photos du ", "photos des ", "photos d ", "photos un ",
            "voir ", "affiche ", "afficher ",
            "à quoi ressemble ", "ressemble "
        ]
        
        for pattern in patterns:
            if pattern in text_lower:
                # Extraire ce qui vient après le pattern
                query = text_lower.split(pattern, 1)[1].strip()
                # Nettoyer
                query = query.rstrip('?!.,;')
                
                # Supprimer les articles français au début
                articles = ["un ", "une ", "le ", "la ", "les ", "l'", "des ", "du ", "de la "]
                for article in articles:
                    if query.startswith(article):
                        query = query[len(article):].strip()
                        break
                
                return query
        
        # Si aucun pattern trouvé, retourner le texte complet nettoyé
        query = text.strip()
        
        # Supprimer les articles au début
        articles = ["un ", "une ", "le ", "la ", "les ", "l'", "des ", "du ", "de la "]
        for article in articles:
            if query.lower().startswith(article):
                query = query[len(article):].strip()
                break
        
        return query

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
