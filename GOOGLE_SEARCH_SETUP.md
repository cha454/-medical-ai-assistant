# Configuration de Google Custom Search API

Pour activer la recherche Google dans votre assistant, suivez ces étapes :

## 1. Créer un projet Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API "Custom Search API"

## 2. Obtenir une clé API

1. Dans Google Cloud Console, allez dans **APIs & Services** > **Credentials**
2. Cliquez sur **Create Credentials** > **API Key**
3. Copiez votre clé API
4. (Optionnel) Restreignez la clé à l'API Custom Search pour la sécurité

## 3. Créer un moteur de recherche personnalisé

1. Allez sur [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Cliquez sur **Add** pour créer un nouveau moteur
3. Configuration recommandée :
   - **Sites to search**: Laissez vide pour rechercher sur tout le web
   - **Language**: Français (ou votre langue)
   - **Name**: Assistant Médical IA Search
4. Cliquez sur **Create**
5. Dans les paramètres du moteur, activez **Search the entire web**
6. Copiez votre **Search engine ID** (cx)

## 4. Ajouter les clés à votre fichier .env

Ajoutez ces lignes à votre fichier `.env` :

```env
# Google Custom Search API (optionnel - 100 requêtes/jour gratuit)
GOOGLE_SEARCH_API_KEY=votre_cle_api_ici
GOOGLE_SEARCH_CX=votre_search_engine_id_ici
```

## 5. Limites gratuites

- **100 requêtes par jour** gratuitement
- Au-delà : 5$ pour 1000 requêtes supplémentaires

## 6. Alternative : Sans Google

Si vous ne configurez pas Google Search, l'assistant utilisera automatiquement :
- Wikipedia (gratuit, illimité)
- DuckDuckGo (gratuit, illimité)
- PubMed (gratuit, illimité)

Ces sources sont déjà très fiables pour la plupart des questions !

## 7. Vérifier que ça fonctionne

Une fois configuré, vous verrez dans les logs :
```
✓ Google: 5 résultats trouvés
```

Et dans les réponses, vous verrez des sources Google avec ⭐⭐⭐ ou ⭐⭐

## Ressources

- [Documentation Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [Tarification](https://developers.google.com/custom-search/v1/overview#pricing)
- [Limites et quotas](https://developers.google.com/custom-search/v1/overview#api_key)
