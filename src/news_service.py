"""
Service d'actualités pour l'assistant médical
Utilise NewsAPI (100 requêtes/jour gratuit)
"""

import requests
import os
from datetime import datetime
from typing import Optional, Dict, Any, List

class NewsService:
    def __init__(self):
        # Clé API NewsAPI (optionnelle)
        self.api_key = os.environ.get('NEWS_API_KEY')
        self.api_url = "https://newsapi.org/v2/top-headlines"
        
        # Catégories disponibles
        self.categories = {
            "santé": "health",
            "sante": "health",
            "health": "health",
            "sport": "sports",
            "sports": "sports",
            "tech": "technology",
            "technologie": "technology",
            "technology": "technology",
            "science": "science",
            "business": "business",
            "affaires": "business",
            "divertissement": "entertainment",
            "entertainment": "entertainment"
        }
        
        # Pays disponibles
        self.countries = {
            "france": "fr",
            "français": "fr",
            "francais": "fr",
            "fr": "fr",
            "usa": "us",
            "us": "us",
            "uk": "gb",
            "angleterre": "gb"
        }
    
    def is_available(self) -> bool:
        """Vérifie si le service est disponible"""
        return bool(self.api_key)
    
    def is_news_request(self, text: str) -> bool:
        """Détecte si le message est une demande d'actualités"""
        text_lower = text.lower()
        
        keywords = [
            "actualité", "actualités", "actualite", "actualites",
            "news", "nouvelles", "infos", "informations",
            "dernières nouvelles", "quoi de neuf", "derniers événements"
        ]
        
        return any(keyword in text_lower for keyword in keywords)
    
    def get_news(self, category: Optional[str] = None, country: str = "fr", query: Optional[str] = None) -> Dict[str, Any]:
        """Récupère les actualités"""
        if not self.is_available():
            return {
                "success": False,
                "error": "Service non configuré",
                "message": "L'API d'actualités n'est pas configurée. Obtiens une clé gratuite sur https://newsapi.org"
            }
        
        try:
            params = {
                "apiKey": self.api_key,
                "country": country,
                "pageSize": 5  # Limiter à 5 articles
            }
            
            # Ajouter la catégorie si spécifiée
            if category:
                cat_code = self._normalize_category(category)
                if cat_code:
                    params["category"] = cat_code
            
            # Ajouter une recherche si spécifiée
            if query:
                params["q"] = query
                del params["country"]  # Pas de filtre pays avec recherche
            
            response = requests.get(self.api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                
                if not articles:
                    return {
                        "success": False,
                        "error": "Aucun article",
                        "message": "Aucune actualité trouvée pour cette recherche."
                    }
                
                return {
                    "success": True,
                    "articles": articles[:5],  # Limiter à 5
                    "total": len(articles),
                    "category": category,
                    "country": country
                }
            else:
                error_data = response.json()
                return {
                    "success": False,
                    "error": f"API Error {response.status_code}",
                    "message": error_data.get("message", "Erreur API")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Erreur lors de la récupération des actualités : {str(e)}"
            }
    
    def parse_and_get_news(self, text: str) -> Dict[str, Any]:
        """Parse le texte et récupère les actualités"""
        text_lower = text.lower()
        
        # Détecter la catégorie
        category = None
        for cat_name, cat_code in self.categories.items():
            if cat_name in text_lower:
                category = cat_code
                break
        
        # Détecter le pays
        country = "fr"  # Par défaut France
        for country_name, country_code in self.countries.items():
            if country_name in text_lower:
                country = country_code
                break
        
        # Détecter une recherche spécifique
        query = None
        search_patterns = [
            r"actualités?\s+sur\s+(.+)",
            r"news\s+about\s+(.+)",
            r"infos?\s+sur\s+(.+)"
        ]
        
        import re
        for pattern in search_patterns:
            match = re.search(pattern, text_lower)
            if match:
                query = match.group(1).strip()
                break
        
        return self.get_news(category=category, country=country, query=query)
    
    def _normalize_category(self, category: str) -> Optional[str]:
        """Normalise la catégorie"""
        category_lower = category.lower().strip()
        return self.categories.get(category_lower)
    
    def format_response(self, news_result: Dict[str, Any], original_query: str) -> str:
        """Formate la réponse pour l'utilisateur"""
        if not news_result["success"]:
            if news_result.get("error") == "Service non configuré":
                return f"""📰 **Service d'Actualités Non Configuré**

⚠️ Le service d'actualités n'est pas encore activé.

**🎯 Pour l'activer (5 minutes - GRATUIT) :**

**Étape 1 :** Créer un compte NewsAPI
• Va sur https://newsapi.org/register
• Remplis le formulaire et vérifie ton email

**Étape 2 :** Obtenir ta clé API
• Copie ta clé API (ressemble à : `a1b2c3d4...`)

**Étape 3 :** Ajouter dans Render
• Render.com → Ton service → Environment
• Add Variable : `NEWS_API_KEY` = ta clé
• Save Changes → Attendre 3 minutes

**📚 Guide détaillé :** Voir `CONFIGURER_NEWSAPI.md`

**💡 Avantages :**
✅ 100 requêtes/jour GRATUIT
✅ Actualités de 150+ pays
✅ 7 catégories (santé, sport, tech, science...)
✅ Recherche par mots-clés

En attendant, je peux t'aider avec d'autres questions ! 😊"""
            
            return f"""📰 **Actualités**

❌ Je n'ai pas pu récupérer les actualités.

**Raison :** {news_result.get('message', 'Erreur inconnue')}

**💡 Exemples de demandes valides :**
• "Quelles sont les dernières actualités ?"
• "Actualités santé"
• "News sport"
• "Actualités tech"
• "Infos science"
• "Actualités sur le climat"

**🌍 Tu peux aussi spécifier un pays :**
• "Actualités France"
• "News USA"

Essaie de reformuler ta demande !"""
        
        articles = news_result["articles"]
        category = news_result.get("category")
        
        # En-tête
        response = "📰 **Dernières Actualités**\n\n"
        
        if category:
            cat_name = {v: k for k, v in self.categories.items()}.get(category, category)
            response += f"**Catégorie :** {cat_name.capitalize()}\n\n"
        
        response += "---\n\n"
        
        # Articles
        for i, article in enumerate(articles, 1):
            title = article.get("title", "Sans titre")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "Source inconnue")
            url = article.get("url", "")
            published_at = article.get("publishedAt", "")
            
            # Formater la date
            date_str = ""
            if published_at:
                try:
                    date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    date_str = date_obj.strftime("%d/%m/%Y %H:%M")
                except:
                    date_str = published_at
            
            response += f"**{i}. {title}**\n"
            if description:
                response += f"   {description[:150]}{'...' if len(description) > 150 else ''}\n"
            response += f"   📰 {source}"
            if date_str:
                response += f" • 📅 {date_str}"
            if url:
                response += f"\n   🔗 {url}"
            response += "\n\n"
        
        response += "---\n\n"
        response += "💡 **Autres catégories :**\n"
        response += "• Santé • Sport • Tech • Science • Business\n\n"
        response += "Veux-tu des actualités sur un sujet spécifique ?"
        
        return response

# Instance globale
news_service = NewsService()

# Test
if __name__ == "__main__":
    service = NewsService()
    
    if service.is_available():
        print("=== Test: Actualités générales ===")
        result = service.get_news()
        print(service.format_response(result, "actualités"))
    else:
        print("⚠️ NEWS_API_KEY non configurée")
