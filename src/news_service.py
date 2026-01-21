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
        
        # Utiliser 'everything' au lieu de 'top-headlines' pour le plan gratuit
        # Le plan Developer ne supporte pas top-headlines sans recherche
        self.api_url = "https://newsapi.org/v2/everything"
        self.top_headlines_url = "https://newsapi.org/v2/top-headlines"
        
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
        
        # Mots-clés sportifs courants pour améliorer les recherches
        self.sports_keywords = {
            "can": "CAN OR \"Coupe d'Afrique des Nations\" OR AFCON",
            "coupe d'afrique": "CAN OR \"Coupe d'Afrique des Nations\" OR AFCON",
            "afcon": "AFCON OR CAN OR \"Africa Cup of Nations\"",
            "football": "football OR soccer",
            "basket": "basketball OR NBA",
            "tennis": "tennis OR ATP OR WTA",
            "rugby": "rugby OR \"Top 14\" OR \"Six Nations\"",
            "formule 1": "\"Formula 1\" OR F1",
            "f1": "\"Formula 1\" OR F1",
            "ligue 1": "\"Ligue 1\" OR \"French football\"",
            "champions league": "\"Champions League\" OR UCL",
            "coupe du monde": "\"World Cup\" OR \"Coupe du Monde\"",
            "jeux olympiques": "Olympics OR \"Jeux Olympiques\"",
            "euro": "\"Euro 2024\" OR \"European Championship\""
        }
        
        # Mots-clés pour les pays africains (pour améliorer les recherches)
        self.country_keywords = {
            "gabon": "Gabon OR Libreville OR gabonais OR gabonaise",
            "maroc": "Maroc OR Marrakech OR Casablanca OR Rabat OR marocain",
            "algérie": "Algérie OR Alger OR algérien OR Algeria",
            "tunisie": "Tunisie OR Tunis OR tunisien OR Tunisia",
            "sénégal": "Sénégal OR Dakar OR sénégalais OR Senegal",
            "côte d'ivoire": "\"Côte d'Ivoire\" OR Abidjan OR ivoirien OR \"Ivory Coast\"",
            "cameroun": "Cameroun OR Yaoundé OR Douala OR camerounais OR Cameroon",
            "mali": "Mali OR Bamako OR malien",
            "burkina faso": "\"Burkina Faso\" OR Ouagadougou OR burkinabé",
            "niger": "Niger OR Niamey OR nigérien",
            "tchad": "Tchad OR N'Djamena OR tchadien OR Chad",
            "congo": "Congo OR Brazzaville OR Kinshasa OR congolais",
            "rdc": "RDC OR \"République Démocratique du Congo\" OR Kinshasa",
            "guinée": "Guinée OR Conakry OR guinéen OR Guinea",
            "bénin": "Bénin OR Cotonou OR béninois OR Benin",
            "togo": "Togo OR Lomé OR togolais"
        }
        
        # Pays disponibles (NewsAPI supporte 54 pays)
        self.countries = {
            "france": "fr",
            "français": "fr",
            "francais": "fr",
            "fr": "fr",
            "usa": "us",
            "us": "us",
            "états-unis": "us",
            "etats-unis": "us",
            "uk": "gb",
            "angleterre": "gb",
            "royaume-uni": "gb",
            "allemagne": "de",
            "espagne": "es",
            "italie": "it",
            "canada": "ca",
            "belgique": "be",
            "suisse": "ch",
            "maroc": "ma",
            "algérie": "dz",
            "tunisie": "tn",
            "sénégal": "sn",
            "côte d'ivoire": "ci",
            "cameroun": "cm"
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
            "dernières nouvelles", "quoi de neuf", "derniers événements",
            "actualité de", "actualité du", "actualité de la",
            "news about", "news on", "news of"
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
            # Pour le plan gratuit (Developer), on doit utiliser 'everything' avec une recherche
            # On ne peut pas utiliser 'top-headlines' sans recherche
            
            # Si pas de recherche spécifique, créer une recherche basée sur la catégorie
            if not query:
                if category:
                    # Mapper les catégories vers des mots-clés de recherche
                    category_keywords = {
                        "health": "health OR medical OR healthcare",
                        "sports": "sports OR football OR basketball",
                        "technology": "technology OR tech OR AI OR software",
                        "science": "science OR research OR discovery",
                        "business": "business OR economy OR finance",
                        "entertainment": "entertainment OR movie OR music"
                    }
                    query = category_keywords.get(category, "news")
                else:
                    # Recherche générale
                    query = "news OR actualités"
            
            # Paramètres pour l'API 'everything'
            params = {
                "apiKey": self.api_key,
                "q": query,  # Recherche obligatoire pour 'everything'
                "language": "fr" if country == "fr" else "en",  # Langue au lieu de pays
                "sortBy": "publishedAt",  # Trier par date
                "pageSize": 10  # Plus d'articles pour filtrer ensuite
            }
            
            # Ajouter une date récente (derniers 7 jours)
            from datetime import datetime, timedelta
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            params["from"] = week_ago
            
            # Debug: afficher les paramètres de la requête
            print(f"📰 NewsAPI Request: {self.api_url}")
            print(f"   Params: {params}")
            
            response = requests.get(self.api_url, params=params, timeout=10)
            
            # Debug: afficher la réponse
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Error: {response.text[:200]}")
            else:
                data = response.json()
                print(f"   Articles trouvés: {len(data.get('articles', []))}")
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                
                if not articles:
                    # Vérifier si c'est un problème de pays non supporté
                    if country and country not in ["fr", "us", "gb", "de", "es", "it", "ca", "be", "ch", "ma", "dz", "tn", "sn", "ci", "cm"]:
                        return {
                            "success": False,
                            "error": "Pays non supporté",
                            "message": f"Le pays '{country}' n'est pas supporté par NewsAPI. Essaie 'France', 'USA', 'UK', 'Maroc', 'Algérie', 'Tunisie', etc.",
                            "suggestion": "Essaie une recherche plus générale ou utilise la recherche web."
                        }
                    
                    return {
                        "success": False,
                        "error": "Aucun article",
                        "message": "Aucune actualité trouvée pour cette recherche. Essaie une recherche plus générale ou un autre pays.",
                        "suggestion": "Essaie une recherche plus large ou utilise la recherche web.",
                        "original_query": query  # Garder la requête originale pour suggestion
                    }
                
                return {
                    "success": True,
                    "articles": articles[:5],  # Limiter à 5
                    "total": len(articles),
                    "category": category,
                    "country": country
                }
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Clé API invalide",
                    "message": "La clé API NewsAPI est invalide ou expirée. Vérifie ta configuration."
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "Limite atteinte",
                    "message": "Limite de 100 requêtes/jour atteinte. Réessaie demain ou passe au plan payant."
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
        
        # Détecter une recherche spécifique EN PREMIER (priorité)
        query = None
        import re
        
        # Patterns de recherche spécifique (ordre important)
        search_patterns = [
            r"actualités?\s+(?:sur|de|du|de\s+la|concernant)\s+(.+)",
            r"news\s+(?:about|on|of)\s+(.+)",
            r"infos?\s+(?:sur|de|du|concernant)\s+(.+)",
            r"dernières?\s+(?:actualités?|news|infos?)\s+(?:sur|de|du|de\s+la)\s+(.+)"
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, text_lower)
            if match:
                query = match.group(1).strip()
                # Nettoyer la requête
                query = query.replace("?", "").replace("!", "").strip()
                
                # Vérifier si c'est un mot-clé sportif connu
                for sport_key, sport_query in self.sports_keywords.items():
                    if sport_key in query:
                        query = sport_query
                        print(f"🏆 Mot-clé sportif détecté: '{sport_key}' → '{sport_query}'")
                        break
                
                # Vérifier si c'est un mot-clé pays connu
                if query not in self.sports_keywords.values():  # Si pas déjà un mot-clé sportif
                    for country_key, country_query in self.country_keywords.items():
                        if country_key in query:
                            query = country_query
                            print(f"🌍 Mot-clé pays détecté: '{country_key}' → '{country_query}'")
                            break
                
                print(f"🔍 Recherche spécifique détectée: '{query}'")
                break
        
        # Si recherche spécifique trouvée, l'utiliser directement
        if query:
            # Détecter la langue pour la recherche
            language = "fr"  # Par défaut français
            if any(word in text_lower for word in ["news", "about", "latest"]):
                language = "en"
            
            return self.get_news(category=None, country="fr", query=query)
        
        # Sinon, détecter la catégorie
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
            
            # Si aucun article trouvé, suggérer d'utiliser le LLM avec recherche web
            original_query_text = news_result.get("original_query", original_query)
            
            return f"""📰 **Actualités**

❌ Je n'ai pas trouvé d'actualités récentes via NewsAPI.

**Raison :** {news_result.get('message', 'Erreur inconnue')}

**💡 Alternative - Recherche Web Intelligente :**

Au lieu de demander "actualités sur X", essaie simplement :
**"{original_query_text}"** (sans le mot "actualités")

Je vais alors utiliser ma recherche web multi-sources (14 sources) et mon intelligence artificielle pour te trouver les informations les plus récentes !

**🌐 Exemples :**
• Au lieu de "actualités sur l'éducation au Gabon"
  → Demande : **"éducation au Gabon"** ou **"système éducatif gabonais"**

• Au lieu de "actualités sur la CAN"
  → Demande : **"CAN 2025"** ou **"Coupe d'Afrique des Nations"**

**📰 Ou essaie des recherches plus générales :**
• "Actualités Afrique"
• "Actualités éducation"
• "Actualités France"
• "News sport"

Reformule ta question et je t'aiderai ! 😊"""
        
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
