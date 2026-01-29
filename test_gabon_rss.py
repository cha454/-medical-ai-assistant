#!/usr/bin/env python3
"""
Test des flux RSS du Gabon pour diagnostiquer le problème d'affichage
"""

import feedparser
import requests
from datetime import datetime

# Flux RSS du Gabon
gabon_feeds = [
    "https://www.gabonreview.com/feed/",
    "https://www.agpgabon.ga/feed/",
    "https://infosgabon.com/feed/",
    "https://gabonactu.com/feed/",
]

def test_rss_feed(feed_url):
    """Teste un flux RSS spécifique"""
    print(f"\n🔍 Test du flux: {feed_url}")
    print("=" * 60)
    
    try:
        # Test de connectivité
        response = requests.get(feed_url, timeout=10)
        print(f"✅ Statut HTTP: {response.status_code}")
        print(f"✅ Taille: {len(response.content)} bytes")
        
        # Parse RSS
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            print(f"⚠️  Feed malformé: {feed.bozo_exception}")
        
        print(f"✅ Titre du feed: {feed.feed.get('title', 'N/A')}")
        print(f"✅ Description: {feed.feed.get('description', 'N/A')}")
        print(f"✅ Nombre d'articles: {len(feed.entries)}")
        
        # Afficher les 3 premiers articles
        for i, entry in enumerate(feed.entries[:3], 1):
            print(f"\n📰 Article {i}:")
            print(f"   Titre: {entry.get('title', 'N/A')}")
            print(f"   Date: {entry.get('published', 'N/A')}")
            print(f"   URL: {entry.get('link', 'N/A')}")
            
            # Vérifier les images
            image_found = False
            
            # Méthode 1: media_content
            if entry.get("media_content"):
                for media in entry.get("media_content", []):
                    if media.get("type", "").startswith("image/"):
                        print(f"   🖼️  Image (media_content): {media.get('url')}")
                        image_found = True
                        break
            
            # Méthode 2: enclosures
            if not image_found and entry.get("links"):
                for link in entry.get("links", []):
                    if link.get("type", "").startswith("image/"):
                        print(f"   🖼️  Image (enclosure): {link.get('href')}")
                        image_found = True
                        break
            
            # Méthode 3: description HTML
            if not image_found:
                description = entry.get("description", "") or entry.get("summary", "")
                if "<img" in description:
                    import re
                    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description)
                    if img_match:
                        print(f"   🖼️  Image (HTML): {img_match.group(1)}")
                        image_found = True
            
            if not image_found:
                print(f"   ❌ Pas d'image trouvée")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

def main():
    """Test tous les flux RSS du Gabon"""
    print("🇬🇦 TEST DES FLUX RSS DU GABON")
    print("=" * 60)
    
    working_feeds = 0
    total_feeds = len(gabon_feeds)
    
    for feed_url in gabon_feeds:
        if test_rss_feed(feed_url):
            working_feeds += 1
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"✅ Flux fonctionnels: {working_feeds}/{total_feeds}")
    print(f"❌ Flux en erreur: {total_feeds - working_feeds}/{total_feeds}")
    
    if working_feeds == 0:
        print("\n⚠️  PROBLÈME DÉTECTÉ: Aucun flux RSS du Gabon ne fonctionne!")
        print("   Cela explique pourquoi l'affichage est vide.")
    elif working_feeds < total_feeds:
        print(f"\n⚠️  PROBLÈME PARTIEL: {total_feeds - working_feeds} flux ne fonctionnent pas.")
    else:
        print("\n✅ Tous les flux fonctionnent. Le problème est ailleurs.")

if __name__ == "__main__":
    main()