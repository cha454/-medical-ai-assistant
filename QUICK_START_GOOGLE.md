# 🚀 Guide Rapide : Activer la Recherche Google

## Option 1 : Sans Google (Gratuit, Illimité) ✅

**Aucune configuration nécessaire !**

Votre assistant utilise déjà :
- ✅ **Wikipedia** - Résumés fiables et à jour
- ✅ **DuckDuckGo** - Recherche web générale
- ✅ **PubMed** - Articles scientifiques médicaux

**C'est suffisant pour 95% des questions !**

---

## Option 2 : Avec Google (100 requêtes/jour gratuit) 🔍

### Pourquoi ajouter Google ?
- ✨ Résultats plus récents et variés
- ✨ Meilleure couverture des actualités
- ✨ Sources supplémentaires fiables

### Configuration en 5 minutes

#### Étape 1 : Obtenir une clé API Google
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un projet (gratuit)
3. Activez "Custom Search API"
4. Créez une clé API dans "Credentials"

#### Étape 2 : Créer un moteur de recherche
1. Allez sur [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Créez un nouveau moteur
3. Activez "Search the entire web"
4. Copiez votre Search Engine ID (cx)

#### Étape 3 : Configurer sur Render
1. Allez dans votre dashboard Render
2. Sélectionnez votre service
3. Allez dans "Environment"
4. Ajoutez ces variables :
   ```
   GOOGLE_SEARCH_API_KEY = votre_cle_api
   GOOGLE_SEARCH_CX = votre_cx_id
   ```
5. Sauvegardez (redéploiement automatique)

#### Étape 4 : Tester
Posez une question à votre assistant et vérifiez les sources :
- Vous devriez voir "Google ⭐⭐" dans les sources

---

## Vérifier que ça fonctionne

### Test local (optionnel)
```bash
python test_google_search.py
```

### Dans l'application
Posez une question et regardez les sources citées :
- **Sans Google** : Wikipedia, DuckDuckGo, PubMed
- **Avec Google** : Google + Wikipedia + DuckDuckGo + PubMed

---

## Limites et Coûts

### Gratuit
- **100 requêtes/jour** avec Google
- **Illimité** avec Wikipedia, DuckDuckGo, PubMed

### Payant (si vous dépassez)
- 5$ pour 1000 requêtes supplémentaires
- Facturation automatique Google Cloud

### Recommandation
Pour un usage personnel/test : **Restez en gratuit** (100/jour suffit largement)

---

## Besoin d'aide ?

📖 Guide détaillé : [GOOGLE_SEARCH_SETUP.md](GOOGLE_SEARCH_SETUP.md)

❓ Questions : Ouvrez une issue sur GitHub
