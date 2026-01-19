# 🔑 Configuration des Sources de Recherche

## 📌 Sources Déjà Actives (Gratuites)

Ces sources fonctionnent **sans aucune configuration** :

✅ **Wikipedia** - Encyclopédie libre  
✅ **DuckDuckGo** - Moteur de recherche respectueux de la vie privée  
✅ **PubMed** - Base de données d'articles scientifiques médicaux

**Vous avez déjà 3 sources fiables qui fonctionnent !**

---

## 🚀 Sources Optionnelles (Pour Améliorer Encore Plus)

### 1. Google Custom Search API (Recommandé)

**Avantages** :
- 100 requêtes gratuites par jour
- Résultats de qualité Google
- Facile à configurer

**Configuration** :

1. Allez sur : https://developers.google.com/custom-search/v1/overview
2. Cliquez sur "Get a Key"
3. Créez un projet Google Cloud (gratuit)
4. Activez l'API Custom Search
5. Créez un Custom Search Engine : https://programmablesearchengine.google.com/
6. Notez votre **API Key** et votre **Search Engine ID (CX)**

**Dans votre fichier `.env`** :
```bash
GOOGLE_SEARCH_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_SEARCH_CX=0123456789abcdefg:xxxxxxxxxx
```

---

### 2. Bing Search API

**Avantages** :
- 1000 requêtes gratuites par mois
- Résultats de qualité Microsoft
- Bonne couverture internationale

**Configuration** :

1. Allez sur : https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
2. Créez un compte Azure (gratuit)
3. Créez une ressource "Bing Search v7"
4. Copiez votre clé API

**Dans votre fichier `.env`** :
```bash
BING_SEARCH_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 3. Brave Search API

**Avantages** :
- 2000 requêtes gratuites par mois
- Moteur de recherche indépendant
- Respect de la vie privée

**Configuration** :

1. Allez sur : https://brave.com/search/api/
2. Créez un compte
3. Demandez une clé API (gratuite)
4. Copiez votre clé

**Dans votre fichier `.env`** :
```bash
BRAVE_SEARCH_API_KEY=BSAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 4. Google Scholar (via SerpAPI)

**Avantages** :
- Accès aux articles académiques
- 100 requêtes gratuites par mois
- Très fiable pour les recherches scientifiques

**Configuration** :

1. Allez sur : https://serpapi.com/
2. Créez un compte gratuit
3. Copiez votre clé API
4. Vous avez 100 recherches gratuites par mois

**Dans votre fichier `.env`** :
```bash
SERPAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📝 Exemple de Fichier `.env` Complet

```bash
# LLM Provider (obligatoire)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Email (obligatoire)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=votre-email@gmail.com

# Météo (obligatoire)
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Recherche Web - Sources Optionnelles
GOOGLE_SEARCH_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_SEARCH_CX=0123456789abcdefg:xxxxxxxxxx
BING_SEARCH_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BRAVE_SEARCH_API_KEY=BSAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERPAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🎯 Quelle Configuration Choisir ?

### Configuration Minimale (Gratuite) ✅
**Déjà active sans configuration** :
- Wikipedia
- DuckDuckGo
- PubMed

**Résultat** : 3 sources fiables

---

### Configuration Recommandée 🌟
**Ajoutez juste Google Custom Search** :
- Wikipedia
- DuckDuckGo
- PubMed
- **Google Custom Search** (100/jour gratuit)

**Résultat** : 4 sources dont 2 très fiables (⭐⭐⭐)

---

### Configuration Complète 🚀
**Toutes les sources activées** :
- Wikipedia
- DuckDuckGo
- PubMed
- Google Custom Search
- Bing Search
- Brave Search
- Google Scholar

**Résultat** : 7 sources dont 4 très fiables (⭐⭐⭐)

---

## 🔍 Comment Vérifier que Ça Fonctionne ?

### 1. Vérifier les Logs au Démarrage

Quand vous lancez l'application, vous devriez voir :
```
✓ LLM activé: OpenAI GPT-4
✓ Service email activé
✓ Service météo OpenWeather activé
✓ Recherche Web: Activé
```

### 2. Tester une Recherche

Posez une question et regardez les logs :
```
🔍 Recherche web multi-sources pour: symptômes du diabète
✓ Google: 5 résultats trouvés
✓ Bing: 5 résultats trouvés
✓ Brave: 3 résultats trouvés
```

### 3. Vérifier la Réponse

La réponse devrait contenir :
```
📊 Qualité de la recherche:
• 7 sources consultées
• 4 sources très fiables (⭐⭐⭐)
• 3 sources fiables (⭐⭐)
```

---

## ⚠️ Limites Gratuites

| Source | Limite Gratuite | Suffisant pour |
|--------|-----------------|----------------|
| Wikipedia | Illimité | ✅ Toujours |
| DuckDuckGo | Illimité | ✅ Toujours |
| PubMed | Illimité | ✅ Toujours |
| Google Custom Search | 100/jour | ✅ Usage normal |
| Bing Search | 1000/mois | ✅ Usage normal |
| Brave Search | 2000/mois | ✅ Usage intensif |
| Google Scholar | 100/mois | ⚠️ Usage modéré |

---

## 🔒 Sécurité

**Important** :
- ✅ Ne partagez JAMAIS vos clés API
- ✅ Le fichier `.env` est dans `.gitignore` (non versionné)
- ✅ Sur Render, ajoutez les clés dans "Environment Variables"
- ✅ Régénérez vos clés si elles sont compromises

---

## 🆘 Dépannage

### Problème : "Google API Error: 429"
**Solution** : Vous avez dépassé la limite de 100 requêtes/jour. Attendez demain ou ajoutez d'autres sources.

### Problème : "Bing API Error: 401"
**Solution** : Votre clé API est invalide. Vérifiez qu'elle est correctement copiée dans `.env`.

### Problème : Pas de résultats web
**Solution** : Les 3 sources gratuites (Wikipedia, DuckDuckGo, PubMed) fonctionnent toujours. Vérifiez votre connexion internet.

---

## 📊 Impact sur la Qualité

### Sans Sources Optionnelles
```
📊 Qualité de la recherche:
• 3 sources consultées
• 1 source très fiable (⭐⭐⭐)
• 2 sources fiables (⭐⭐)
```

### Avec Google Custom Search
```
📊 Qualité de la recherche:
• 4 sources consultées
• 2 sources très fiables (⭐⭐⭐)
• 2 sources fiables (⭐⭐)
```

### Avec Toutes les Sources
```
📊 Qualité de la recherche:
• 7 sources consultées
• 4 sources très fiables (⭐⭐⭐)
• 3 sources fiables (⭐⭐)
```

---

## 🎉 Conclusion

**Vous n'avez rien à configurer pour commencer !**

Les 3 sources gratuites (Wikipedia, DuckDuckGo, PubMed) sont déjà actives et fournissent des résultats fiables.

Si vous voulez améliorer encore plus la qualité, ajoutez **Google Custom Search** (100 requêtes gratuites/jour) - c'est la meilleure option gratuite.

---

**Date** : 20 janvier 2026  
**Version** : 1.0
