"""
Module de recherche web pour enrichir les réponses du chatbot
Supporte: Google Custom Search, Wikipedia, DuckDuckGo, PubMed, Bing, Brave Search
"""

import requests
import json
import os
from datetime import datetime, timedelta
from urllib.parse import quote

class MedicalWebSearch:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=24)  # Cache de 24h
        
        # Clés API Google Custom Search (optionnel)
        self.google_api_key = os.environ.get('GOOGLE_SEARCH_API_KEY')
        self.google_cx = os.environ.get('GOOGLE_SEARCH_CX')  # Custom Search Engine ID
        
        # Clé API Bing Search (optionnel)
        self.bing_api_key = os.environ.get('BING_SEARCH_API_KEY')
        
        # Clé API Brave Search (optionnel)
        self.brave_api_key = os.environ.get('BRAVE_SEARCH_API_KEY')
        
        # Sources médicales fiables
        self.trusted_sources = [
            "who.int",  # OMS
            "santepubliquefrance.fr",
            "ameli.fr",
            "vidal.fr",
            "has-sante.fr",
            "inserm.fr",
            "mayoclinic.org",
            "nih.gov",
            "cdc.gov",
            "webmd.com",
            "healthline.com",
            "medlineplus.gov",
            "ncbi.nlm.nih.gov",
            "cochrane.org"
        ]
    
    def search_medical_info(self, query, language="fr"):
        """Recherche des informations médicales sur le web"""
        
        # Vérifier le cache
        cache_key = f"{query}_{language}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['data']
        
        results = {
            "query": query,
            "sources": [],
            "summary": None,
            "last_updated": datetime.now().isoformat()
        }
        
        # 1. Recherche Google Custom Search (si configuré)
        if self.google_api_key and self.google_cx:
            google_results = self._search_google(query, language)
            if google_results:
                results["sources"].extend(google_results)
                # Utiliser le premier résultat Google comme résumé si pas de Wikipedia
                if google_results and not results.get("summary"):
                    results["summary"] = google_results[0].get("extract", "")
        
        # 2. Recherche Wikipedia (gratuit et fiable)
        wiki_result = self._search_wikipedia(query, language)
        if wiki_result:
            results["sources"].append(wiki_result)
            # Wikipedia en priorité pour le résumé
            if wiki_result.get("extract"):
                results["summary"] = wiki_result.get("extract", "")
        
        # 3. Recherche DuckDuckGo (gratuit, pas de clé API)
        ddg_results = self._search_duckduckgo(query)
        if ddg_results:
            results["sources"].extend(ddg_results)
        
        # 4. Recherche PubMed (articles scientifiques gratuits)
        pubmed_results = self._search_pubmed(query)
        if pubmed_results:
            results["sources"].extend(pubmed_results)
        
        # 5. Recherche Bing (si configuré)
        if self.bing_api_key:
            bing_results = self._search_bing(query, language)
            if bing_results:
                results["sources"].extend(bing_results)
        
        # 6. Recherche Brave Search (si configuré)
        if self.brave_api_key:
            brave_results = self._search_brave(query, language)
            if brave_results:
                results["sources"].extend(brave_results)
        
        # 7. Recherche Scholar Google (articles académiques)
        scholar_results = self._search_google_scholar(query)
        if scholar_results:
            results["sources"].extend(scholar_results)
        
        # Trier les résultats par fiabilité
        results["sources"] = self._rank_sources(results["sources"])
        
        # Mettre en cache
        self.cache[cache_key] = {
            "data": results,
            "timestamp": datetime.now()
        }
        
        return results
    
    def _search_google(self, query, language="fr"):
        """Recherche sur Google Custom Search API"""
        if not self.google_api_key or not self.google_cx:
            return []
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_api_key,
                "cx": self.google_cx,
                "q": query,
                "lr": f"lang_{language}",  # Langue des résultats
                "num": 5  # Nombre de résultats (max 10)
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get("items", []):
                    # Vérifier si c'est une source fiable
                    url_lower = item.get("link", "").lower()
                    is_trusted = any(source in url_lower for source in self.trusted_sources)
                    
                    results.append({
                        "source": "Google",
                        "title": item.get("title", ""),
                        "extract": item.get("snippet", ""),
                        "url": item.get("link", ""),
                        "reliability": "very_high" if is_trusted else "high"
                    })
                
                print(f"✓ Google: {len(results)} résultats trouvés")
                return results
            else:
                print(f"Google API Error: {response.status_code}")
                if response.status_code == 429:
                    print("⚠️ Limite de requêtes Google atteinte (100/jour gratuit)")
        except Exception as e:
            print(f"Google search error: {e}")
        return []
    
    def _search_wikipedia(self, query, language="fr"):
        """Recherche sur Wikipedia"""
        try:
            lang_code = "fr" if language == "fr" else "en"
            url = f"https://{lang_code}.wikipedia.org/api/rest_v1/page/summary/{query}"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "Wikipedia",
                    "title": data.get("title", ""),
                    "extract": data.get("extract", ""),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                    "thumbnail": data.get("thumbnail", {}).get("source", ""),
                    "reliability": "high"
                }
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        return None
    
    def _search_duckduckgo(self, query):
        """Recherche sur DuckDuckGo Instant Answer API"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                results = []
                
                # Abstract
                if data.get("Abstract"):
                    results.append({
                        "source": "DuckDuckGo",
                        "title": data.get("Heading", ""),
                        "extract": data.get("Abstract", ""),
                        "url": data.get("AbstractURL", ""),
                        "reliability": "medium"
                    })
                
                # Related topics
                for topic in data.get("RelatedTopics", [])[:3]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append({
                            "source": "DuckDuckGo",
                            "title": topic.get("Text", "")[:100],
                            "extract": topic.get("Text", ""),
                            "url": topic.get("FirstURL", ""),
                            "reliability": "medium"
                        })
                
                return results
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        return []
    
    def _search_pubmed(self, query):
        """Recherche sur PubMed (articles scientifiques)"""
        try:
            # Recherche d'articles
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": 3,
                "retmode": "json"
            }
            
            search_response = requests.get(search_url, params=search_params, timeout=5)
            if search_response.status_code != 200:
                return []
            
            search_data = search_response.json()
            ids = search_data.get("esearchresult", {}).get("idlist", [])
            
            if not ids:
                return []
            
            # Récupérer les détails des articles
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(ids),
                "retmode": "json"
            }
            
            fetch_response = requests.get(fetch_url, params=fetch_params, timeout=5)
            if fetch_response.status_code != 200:
                return []
            
            fetch_data = fetch_response.json()
            results = []
            
            for article_id in ids:
                article = fetch_data.get("result", {}).get(article_id, {})
                if article:
                    results.append({
                        "source": "PubMed",
                        "title": article.get("title", ""),
                        "extract": article.get("title", ""),  # PubMed ne donne pas d'abstract via cette API
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/",
                        "authors": ", ".join([author.get("name", "") for author in article.get("authors", [])[:3]]),
                        "date": article.get("pubdate", ""),
                        "reliability": "very_high"
                    })
            
            return results
        except Exception as e:
            print(f"PubMed search error: {e}")
        return []
    
    def format_search_results(self, results):
        """Formate les résultats de recherche pour affichage avec HTML enrichi"""
        if not results or not results.get("sources"):
            return None
        
        # Début du conteneur HTML pour les sources
        html = '<div class="search-sources-container">'
        html += '<div class="search-sources-title"><i class="fas fa-book-reader"></i> Sources consultées pour cette réponse</div>'
        html += '<div class="sources-list">'
        
        for source in results["sources"][:5]:  # Limiter à 5 sources pour ne pas surcharger
            reliability_icon = {
                "very_high": "🛡️",
                "high": "✅",
                "medium": "🔍"
            }.get(source.get("reliability", "medium"), "🔍")
            
            source_name = source.get('source', 'Source Web')
            source_url = source.get('url', '#')
            source_title = source.get('title', 'Voir la source')
            
            html += f"""
            <a href="{source_url}" target="_blank" class="source-item" title="{source_title}">
                <div class="source-icon">{reliability_icon}</div>
                <div class="source-info">
                    <span class="source-name">{source_name}</span>
                    <span class="source-url">{source_url}</span>
                </div>
                <div class="source-link-icon"><i class="fas fa-external-link-alt"></i></div>
            </a>"""
        
        html += '</div></div>'
        
        # Texte Markdown standard qui sera rendu par marked.js
        # On ajoute le HTML à la fin du texte Markdown
        summary = results.get("summary", "")
        if len(summary) > 600:
            summary = summary[:600] + "..."
            
        formatted = f"{summary}\n\n{html}"
        
        return formatted
    
    def _search_bing(self, query, language="fr"):
        """Recherche sur Bing Search API"""
        if not self.bing_api_key:
            return []
        
        try:
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
            params = {
                "q": query,
                "mkt": "fr-FR" if language == "fr" else "en-US",
                "count": 5,
                "responseFilter": "Webpages"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get("webPages", {}).get("value", []):
                    url_lower = item.get("url", "").lower()
                    is_trusted = any(source in url_lower for source in self.trusted_sources)
                    
                    results.append({
                        "source": "Bing",
                        "title": item.get("name", ""),
                        "extract": item.get("snippet", ""),
                        "url": item.get("url", ""),
                        "reliability": "very_high" if is_trusted else "high"
                    })
                
                print(f"✓ Bing: {len(results)} résultats trouvés")
                return results
            else:
                print(f"Bing API Error: {response.status_code}")
        except Exception as e:
            print(f"Bing search error: {e}")
        return []
    
    def _search_brave(self, query, language="fr"):
        """Recherche sur Brave Search API"""
        if not self.brave_api_key:
            return []
        
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "Accept": "application/json",
                "X-Subscription-Token": self.brave_api_key
            }
            params = {
                "q": query,
                "country": "FR" if language == "fr" else "US",
                "search_lang": language,
                "count": 5
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get("web", {}).get("results", []):
                    url_lower = item.get("url", "").lower()
                    is_trusted = any(source in url_lower for source in self.trusted_sources)
                    
                    results.append({
                        "source": "Brave",
                        "title": item.get("title", ""),
                        "extract": item.get("description", ""),
                        "url": item.get("url", ""),
                        "reliability": "very_high" if is_trusted else "high"
                    })
                
                print(f"✓ Brave: {len(results)} résultats trouvés")
                return results
            else:
                print(f"Brave API Error: {response.status_code}")
        except Exception as e:
            print(f"Brave search error: {e}")
        return []
    
    def _search_google_scholar(self, query):
        """Recherche sur Google Scholar (scraping léger)"""
        try:
            # Utiliser l'API Serpapi si disponible, sinon scraping basique
            serpapi_key = os.environ.get('SERPAPI_KEY')
            
            if serpapi_key:
                url = "https://serpapi.com/search"
                params = {
                    "engine": "google_scholar",
                    "q": query,
                    "api_key": serpapi_key,
                    "num": 3
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    
                    for item in data.get("organic_results", []):
                        results.append({
                            "source": "Google Scholar",
                            "title": item.get("title", ""),
                            "extract": item.get("snippet", ""),
                            "url": item.get("link", ""),
                            "authors": item.get("publication_info", {}).get("authors", ""),
                            "reliability": "very_high"
                        })
                    
                    print(f"✓ Google Scholar: {len(results)} résultats trouvés")
                    return results
        except Exception as e:
            print(f"Google Scholar search error: {e}")
        return []
    
    def _rank_sources(self, sources):
        """Trie les sources par fiabilité et pertinence"""
        reliability_order = {
            "very_high": 3,
            "high": 2,
            "medium": 1
        }
        
        # Trier par fiabilité puis par source
        sorted_sources = sorted(
            sources,
            key=lambda x: (
                reliability_order.get(x.get("reliability", "medium"), 0),
                x.get("source", "")
            ),
            reverse=True
        )
        
        # Dédupliquer par URL
        seen_urls = set()
        unique_sources = []
        for source in sorted_sources:
            url = source.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_sources.append(source)
        
        return unique_sources
    
    def search_and_format(self, query, language="fr"):
        """Recherche et formate en une seule étape"""
        results = self.search_medical_info(query, language)
        return self.format_search_results(results)

# Instance globale
web_search = MedicalWebSearch()

# Test
if __name__ == "__main__":
    searcher = MedicalWebSearch()
    
    # Test Wikipedia
    print("=== Test Wikipedia ===")
    results = searcher.search_medical_info("diabète", "fr")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Test formatage
    print("\n=== Test Formatage ===")
    formatted = searcher.format_search_results(results)
    print(formatted)
