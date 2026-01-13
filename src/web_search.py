"""
Module de recherche web pour enrichir les réponses du chatbot
"""

import requests
import json
from datetime import datetime, timedelta

class MedicalWebSearch:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=24)  # Cache de 24h
        
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
            "cdc.gov"
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
        
        # 1. Recherche Wikipedia (gratuit et fiable)
        wiki_result = self._search_wikipedia(query, language)
        if wiki_result:
            results["sources"].append(wiki_result)
            results["summary"] = wiki_result.get("extract", "")
        
        # 2. Recherche DuckDuckGo (gratuit, pas de clé API)
        ddg_results = self._search_duckduckgo(query)
        if ddg_results:
            results["sources"].extend(ddg_results)
        
        # 3. Recherche PubMed (articles scientifiques gratuits)
        pubmed_results = self._search_pubmed(query)
        if pubmed_results:
            results["sources"].extend(pubmed_results)
        
        # Mettre en cache
        self.cache[cache_key] = {
            "data": results,
            "timestamp": datetime.now()
        }
        
        return results
    
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
        """Formate les résultats de recherche pour affichage"""
        if not results or not results.get("sources"):
            return None
        
        formatted = f"""**📚 Informations trouvées sur le web:**\n\n"""
        
        # Résumé principal
        if results.get("summary"):
            formatted += f"{results['summary'][:500]}...\n\n"
        
        # Sources
        formatted += "**🔍 Sources consultées:**\n\n"
        
        for i, source in enumerate(results["sources"][:5], 1):
            reliability_emoji = {
                "very_high": "⭐⭐⭐",
                "high": "⭐⭐",
                "medium": "⭐"
            }.get(source.get("reliability", "medium"), "⭐")
            
            formatted += f"{i}. **{source.get('source', 'Source')}** {reliability_emoji}\n"
            if source.get("title"):
                formatted += f"   {source['title'][:100]}\n"
            if source.get("url"):
                formatted += f"   🔗 {source['url']}\n"
            formatted += "\n"
        
        formatted += f"\n📅 **Dernière mise à jour:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        formatted += "\n⚠️ **Important:** Vérifiez toujours avec un professionnel de santé."
        
        return formatted
    
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
