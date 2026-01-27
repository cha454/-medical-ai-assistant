"""
Service d'actualités hybride pour l'assistant médical
Combine GNews API (international) + RSS Feeds (Afrique)
"""

import requests
import feedparser
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

class NewsServiceV2:
    def __init__(self):
        # Clé API GNews (optionnelle - 100 requêtes/jour gratuit)
        self.gnews_key = os.environ.get('GNEWS_API_KEY')
        
        # URLs des API
        self.gnews_url = "https://gnews.io/api/v4/search"
        
        # Flux RSS pour les actualités africaines
        self.african_rss_feeds = {
            "gabon": [
                "https://www.gabonreview.com/feed/",
                "https://www.agpgabon.ga/feed/",
            ],
            "afrique_generale": [
                "https://www.jeuneafrique.com/feed/",
                "https://www.bbc.com/afrique/rss.xml",
                "https://www.rfi.fr/fr/afrique/rss",
                "https://africanews.com/feed/",
            ],
            "maroc": [
                "https://www.le360.ma/fr/rss",
                "https://www.hespress.com/feed",
            ],
            "algerie": [
                "https://www.tsa-algerie.com/feed/",
            ],
            "tunisie": [
                "https://www.tunisienumerique.com/feed/",
            ],
            "senegal": [
                "https://www.dakaractu.com/feed",
            ],
            "cote_ivoire": [
                "https://www.connectionivoirienne.net/feed/",
            ],
            "cameroun": [
                "https://www.camer.be/feed/",
            ],
        }
        
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
        
        # Pays africains
        self.african_countries = [
            "gabon", "maroc", "algérie", "algerie", "tunisie", "sénégal", "senegal",
            "côte d'ivoire", "cote d'ivoire", "cameroun", "mali", "burkina faso",
            "niger", "tchad", "congo", "rdc", "guinée", "guinee", "bénin", "benin", "togo"
        ]
        
        print(f"✓ Service actualités hybride initialisé (GNews + RSS)")
    
    def is_available(self) -> bool:
        """Vérifie si au moins un service est disponible"""
        return True  # RSS est toujours disponible
    
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
    
    def get_news_hybrid(self, query: str, country: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """Récupère les actualités en combinant GNews et RSS"""
        articles = []
        sources_used = []
        
        # Détecter si c'est une recherche africaine
        is_african = False
        if query:
            query_lower = query.lower()
            is_african = any(country_name in query_lower for country_name in self.african_countries)
        
        # 1. Si recherche africaine → Priorité RSS
        if is_african:
            print(f"🌍 Recherche africaine détectée → Utilisation RSS en priorité")
            rss_articles = self._get_rss_news(query)
            if rss_articles:
                articles.extend(rss_articles)
                sources_used.append("RSS Feeds (Afrique)")
        
        # 2. Compléter avec GNews (si disponible et pas trop d'articles RSS)
        if self.gnews_key and len(articles) < 5:
            print(f"📰 Complément avec GNews API")
            gnews_articles = self._get_gnews(query, category)
            if gnews_articles:
                articles.extend(gnews_articles)
                sources_used.append("GNews API")
        
        # 3. Si pas de GNews et pas assez d'articles RSS → Plus de RSS
        if not self.gnews_key and len(articles) < 5:
            print(f"📡 Recherche RSS étendue")
            more_rss = self._get_rss_news(query, extended=True)
            if more_rss:
                articles.extend(more_rss)
        
        # Dédupliquer et limiter à 10 articles
        articles = self._deduplicate_articles(articles)[:10]
        
        if not articles:
            return {
                "success": False,
                "error": "Aucun article",
                "message": "Aucune actualité trouvée pour cette recherche.",
                "suggestion": "Essaie une recherche plus générale ou un autre sujet."
            }
        
        return {
            "success": True,
            "articles": articles[:5],  # Limiter à 5 pour l'affichage
            "total": len(articles),
            "sources": sources_used,
            "query": query
        }
    
    def _get_gnews(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Récupère les actualités depuis GNews API"""
        if not self.gnews_key:
            return []
        
        try:
            params = {
                "apikey": self.gnews_key,
                "q": query,
                "lang": "fr",
                "max": 10,
                "sortby": "publishedAt"
            }
            
            if category:
                params["topic"] = category
            
            print(f"📰 GNews Request: {query}")
            response = requests.get(self.gnews_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get("articles", []):
                    articles.append({
                        "title": article.get("title"),
                        "description": article.get("description"),
                        "url": article.get("url"),
                        "source": {"name": article.get("source", {}).get("name", "GNews")},
                        "publishedAt": article.get("publishedAt"),
                        "image": article.get("image")
                    })
                
                print(f"   ✓ {len(articles)} articles GNews trouvés")
                return articles
            else:
                print(f"   ⚠️ GNews Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ GNews Exception: {e}")
            return []
    
    def _get_rss_news(self, query: str, extended: bool = False) -> List[Dict]:
        """Récupère les actualités depuis les flux RSS africains"""
        articles = []
        query_lower = query.lower()
        
        # Déterminer quels flux RSS utiliser
        feeds_to_check = []
        
        # Recherche spécifique par pays
        for country, feeds in self.african_rss_feeds.items():
            if country.replace("_", " ") in query_lower:
                feeds_to_check.extend(feeds)
                print(f"🌍 Flux RSS {country}: {len(feeds)} sources")
        
        # Si pas de pays spécifique ou extended, utiliser les flux généraux
        if not feeds_to_check or extended:
            feeds_to_check.extend(self.african_rss_feeds["afrique_generale"])
        
        # Limiter le nombre de flux pour ne pas être trop lent
        feeds_to_check = list(set(feeds_to_check))[:5]  # Max 5 flux
        
        # Parser chaque flux RSS
        for feed_url in feeds_to_check:
            try:
                print(f"📡 Parsing RSS: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # Max 5 articles par flux
                    # Filtrer par mots-clés si recherche spécifique
                    title = entry.get("title", "")
                    description = entry.get("description", "") or entry.get("summary", "")
                    
                    # Si recherche spécifique, vérifier que l'article correspond
                    if query and len(query) > 3:
                        if query_lower not in title.lower() and query_lower not in description.lower():
                            continue
                    
                    # Extraire la date
                    published = entry.get("published", "") or entry.get("updated", "")
                    
                    articles.append({
                        "title": title,
                        "description": description[:300] if description else "",
                        "url": entry.get("link", ""),
                        "source": {"name": feed.feed.get("title", "RSS Feed")},
                        "publishedAt": published,
                        "image": entry.get("media_content", [{}])[0].get("url") if entry.get("media_content") else None
                    })
                
            except Exception as e:
                print(f"   ⚠️ RSS Error ({feed_url}): {e}")
                continue
        
        print(f"   ✓ {len(articles)} articles RSS trouvés")
        return articles
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Supprime les articles en double (même titre)"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article.get("title", "").lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    def parse_and_get_news(self, text: str) -> Dict[str, Any]:
        """Parse le texte et récupère les actualités"""
        text_lower = text.lower()
        
        # Détecter une recherche spécifique
        query = None
        import re
        
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
                query = query.replace("?", "").replace("!", "").strip()
                print(f"🔍 Recherche détectée: '{query}'")
                break
        
        # Si pas de recherche spécifique, recherche générale
        if not query:
            query = "actualités"
        
        # Détecter la catégorie
        category = None
        for cat_name, cat_code in self.categories.items():
            if cat_name in text_lower:
                category = cat_code
                break
        
        return self.get_news_hybrid(query=query, category=category)
    
    def format_response(self, news_result: Dict[str, Any], original_query: str) -> str:
        """Formate la réponse pour l'utilisateur"""
        if not news_result["success"]:
            return f"""📰 **Actualités**

❌ Je n'ai pas trouvé d'actualités récentes.

**Raison :** {news_result.get('message', 'Erreur inconnue')}

**💡 Suggestions :**
• Essaie une recherche plus générale
• Vérifie l'orthographe
• Demande des actualités sur un autre sujet

**Exemples :**
• "Actualités Afrique"
• "Actualités santé"
• "News sport"
• "Actualités Gabon"

Reformule ta question et je t'aiderai ! 😊"""
        
        articles = news_result["articles"]
        sources = news_result.get("sources", [])
        
        # En-tête
        response = '<div class="news-container">\n'
        response += '<h3>📰 Dernières Actualités</h3>\n\n'
        
        if sources:
            response += f'<p class="news-sources"><strong>Sources :</strong> {", ".join(sources)}</p>\n\n'
        
        # Grille d'articles (2 par ligne)
        response += '<div class="news-grid">\n'
        
        for i, article in enumerate(articles, 1):
            title = article.get("title", "Sans titre")
            description = article.get("description", "")
            source = article.get("source", {}).get("name", "Source inconnue")
            url = article.get("url", "")
            published_at = article.get("publishedAt", "")
            image_url = article.get("image", "")
            
            # Formater la date
            date_str = ""
            if published_at:
                try:
                    # Essayer différents formats de date
                    for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%d %H:%M:%S"]:
                        try:
                            date_obj = datetime.strptime(published_at[:19], fmt[:19])
                            date_str = date_obj.strftime("%d/%m/%Y %H:%M")
                            break
                        except:
                            continue
                except:
                    date_str = published_at[:10] if len(published_at) >= 10 else ""
            
            # Carte d'article
            response += '<div class="news-card">\n'
            
            # Image ou placeholder
            if image_url:
                response += f'  <div class="news-image" style="background-image: url(\'{image_url}\')"></div>\n'
            else:
                response += '  <div class="news-image news-placeholder">📰</div>\n'
            
            # Contenu
            response += '  <div class="news-content">\n'
            response += f'    <h4 class="news-title">{title}</h4>\n'
            
            if description:
                desc_short = description[:150] + '...' if len(description) > 150 else description
                response += f'    <p class="news-description">{desc_short}</p>\n'
            
            response += '    <div class="news-meta">\n'
            response += f'      <span class="news-source">📰 {source}</span>\n'
            if date_str:
                response += f'      <span class="news-date">📅 {date_str}</span>\n'
            response += '    </div>\n'
            
            if url:
                response += f'    <a href="{url}" target="_blank" class="news-link">🔗 Lire l\'article</a>\n'
            
            response += '  </div>\n'
            response += '</div>\n'
        
        response += '</div>\n'  # Fin de la grille
        
        # Footer
        response += '<div class="news-footer">\n'
        response += '<p>💡 <strong>Autres catégories :</strong> Santé • Sport • Tech • Science • Business</p>\n'
        response += '<p>Veux-tu des actualités sur un sujet spécifique ?</p>\n'
        response += '</div>\n'
        response += '</div>\n'  # Fin du container
        
        return response

# Instance globale
news_service_v2 = NewsServiceV2()

# Test
if __name__ == "__main__":
    service = NewsServiceV2()
    
    print("=== Test: Actualités Gabon ===")
    result = service.parse_and_get_news("actualités du Gabon")
    print(service.format_response(result, "actualités du Gabon"))
