# 🖼️ Guide de Recherche d'Images Médicales

## ✅ Fonctionnalité Intégrée

Votre assistant peut maintenant **chercher et afficher des images médicales** depuis le web !

## 🎯 Comment Utiliser

### Exemples de Demandes

```
"Montre-moi une image du cœur humain"
"Photo de poumons"
"Image d'un diabète"
"À quoi ressemble une fracture du bras"
"Affiche-moi des images de cellules"
"Voir une image du cerveau"
```

### Mots-Clés Détectés

L'assistant détecte automatiquement les demandes d'images avec ces mots-clés :
- image, photo, picture, img, illustration
- montre-moi, montre moi
- voir, affiche, afficher
- à quoi ressemble, ressemble
- apparence, aspect

## 🔧 Configuration Requise

Pour que la recherche d'images fonctionne, vous devez configurer **au moins une** clé API parmi :

### 1. Google Custom Search API (Recommandé)

**Avantages:**
- Meilleure qualité de résultats
- Filtrage de contenu
- Recherche précise

**Configuration:**
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un projet
3. Activez "Custom Search API"
4. Créez une clé API
5. Créez un moteur de recherche personnalisé sur [Programmable Search Engine](https://programmablesearchengine.google.com/)
6. Récupérez le CX (Search Engine ID)

**Variables d'environnement (.env):**
```bash
GOOGLE_SEARCH_API_KEY=votre_cle_api_google
GOOGLE_SEARCH_CX=votre_cx_id
```

**Limites:**
- Gratuit : 100 requêtes/jour
- Payant : $5 pour 1000 requêtes supplémentaires

---

### 2. Bing Search API

**Avantages:**
- Bonne qualité
- Quota généreux
- Facile à configurer

**Configuration:**
1. Allez sur [Azure Portal](https://portal.azure.com/)
2. Créez une ressource "Bing Search v7"
3. Récupérez la clé API

**Variables d'environnement (.env):**
```bash
BING_SEARCH_API_KEY=votre_cle_bing
```

**Limites:**
- Gratuit : 1000 requêtes/mois (niveau F1)
- Payant : à partir de $3 pour 1000 requêtes

---

### 3. Unsplash API

**Avantages:**
- Photos de haute qualité
- Gratuit
- Facile à utiliser

**Configuration:**
1. Allez sur [Unsplash Developers](https://unsplash.com/developers)
2. Créez une application
3. Récupérez l'Access Key

**Variables d'environnement (.env):**
```bash
UNSPLASH_ACCESS_KEY=votre_access_key
```

**Limites:**
- Gratuit : 50 requêtes/heure
- Production : 5000 requêtes/heure (après approbation)

---

### 4. Pixabay API

**Avantages:**
- Totalement gratuit
- Pas de limite stricte
- Images libres de droits

**Configuration:**
1. Allez sur [Pixabay API](https://pixabay.com/api/docs/)
2. Créez un compte
3. Récupérez la clé API

**Variables d'environnement (.env):**
```bash
PIXABAY_API_KEY=votre_cle_pixabay
```

**Limites:**
- Gratuit : 5000 requêtes/heure

---

## 📊 Comparaison des Services

| Service | Qualité | Gratuit | Limite Gratuite | Recommandation |
|---------|---------|---------|-----------------|----------------|
| **Google Images** | ⭐⭐⭐⭐⭐ | Oui | 100/jour | ⭐⭐⭐ Meilleur |
| **Bing Images** | ⭐⭐⭐⭐ | Oui | 1000/mois | ⭐⭐⭐ Excellent |
| **Unsplash** | ⭐⭐⭐⭐⭐ | Oui | 50/heure | ⭐⭐ Bon (photos artistiques) |
| **Pixabay** | ⭐⭐⭐ | Oui | 5000/heure | ⭐⭐ Bon (backup) |

## 🚀 Installation Rapide

### Option 1 : Google Images (Recommandé)

```bash
# 1. Obtenir les clés API (voir ci-dessus)

# 2. Ajouter dans .env
echo "GOOGLE_SEARCH_API_KEY=votre_cle" >> .env
echo "GOOGLE_SEARCH_CX=votre_cx" >> .env

# 3. Redémarrer l'application
```

### Option 2 : Bing Images

```bash
# 1. Obtenir la clé API (voir ci-dessus)

# 2. Ajouter dans .env
echo "BING_SEARCH_API_KEY=votre_cle" >> .env

# 3. Redémarrer l'application
```

### Option 3 : Pixabay (Plus Simple)

```bash
# 1. Obtenir la clé API (voir ci-dessus)

# 2. Ajouter dans .env
echo "PIXABAY_API_KEY=votre_cle" >> .env

# 3. Redémarrer l'application
```

## 💡 Exemples d'Utilisation

### Recherche Médicale

```
Utilisateur: "Montre-moi une image du cœur humain"


IA: 🖼️ **6 images trouvées** (source: Google Images)

**Recherche:** cœur humain

**Image 1:**
- 📸 Titre: Anatomie du cœur humain
- 🔗 URL: https://...
- 📏 Dimensions: 1200x800

**Image 2:**
- 📸 Titre: Schéma du système cardiovasculaire
- 🔗 URL: https://...
- 📏 Dimensions: 1024x768

[...]

⚠️ **Note importante:**
- Ces images proviennent du web et sont à but éducatif uniquement
- Pour un diagnostic médical, consultez toujours un professionnel de santé
```

### Recherche Anatomique

```
Utilisateur: "Photo de poumons"

IA: [Affiche 6 images de poumons avec détails]
```

### Recherche de Symptômes

```
Utilisateur: "À quoi ressemble une éruption cutanée"

IA: [Affiche des images d'éruptions cutanées]
```

## 🎨 Format de Réponse

Pour chaque image trouvée, l'IA affiche :
- 📸 **Titre** : Description de l'image
- 🔗 **URL** : Lien direct vers l'image
- 📏 **Dimensions** : Largeur x Hauteur
- 👤 **Photographe** : Auteur (si disponible)

## ⚠️ Limitations et Avertissements

### Limitations Techniques
- Maximum 6 images par recherche
- Filtrage de contenu activé (safe search)
- Cache de 24h pour économiser les requêtes API

### Avertissements Médicaux
- ⚠️ Les images sont à **but éducatif uniquement**
- ⚠️ Ne remplacent **pas un diagnostic médical**
- ⚠️ Consultez toujours un **professionnel de santé**
- ⚠️ Vérifiez les **droits d'utilisation** avant réutilisation

### Limites des API Gratuites
- Google : 100 requêtes/jour
- Bing : 1000 requêtes/mois
- Unsplash : 50 requêtes/heure
- Pixabay : 5000 requêtes/heure

## 🔐 Sécurité et Confidentialité

### Filtrage de Contenu
- Safe Search activé par défaut
- Contenu inapproprié filtré
- Images médicales uniquement

### Données Personnelles
- Aucune image n'est stockée
- Pas de tracking utilisateur
- Requêtes anonymes

## 🐛 Résolution de Problèmes

### "Aucune image trouvée"

**Causes possibles:**
1. Aucune clé API configurée
2. Quota API dépassé
3. Termes de recherche trop spécifiques
4. Erreur de connexion

**Solutions:**
1. Vérifiez que vous avez configuré au moins une clé API
2. Vérifiez les quotas sur votre console API
3. Utilisez des termes plus généraux
4. Vérifiez votre connexion internet

### "API Error 429"

**Cause:** Limite de requêtes dépassée

**Solutions:**
1. Attendez la réinitialisation du quota (quotidien/mensuel)
2. Configurez une autre API en backup
3. Passez à un plan payant si nécessaire

### "API Error 401"

**Cause:** Clé API invalide

**Solutions:**
1. Vérifiez que la clé est correcte dans .env
2. Régénérez une nouvelle clé
3. Vérifiez que l'API est activée dans votre console

## 📚 Ressources

### Documentation Officielle
- [Google Custom Search API](https://developers.google.com/custom-search/v1/overview)
- [Bing Search API](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)
- [Unsplash API](https://unsplash.com/documentation)
- [Pixabay API](https://pixabay.com/api/docs/)

### Tutoriels
- [Créer un moteur Google Custom Search](https://support.google.com/programmable-search/answer/2649143)
- [Obtenir une clé Bing Search](https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource)

## 🎉 Prêt à Utiliser !

Une fois configuré, demandez simplement :
- "Montre-moi une image de..."
- "Photo de..."
- "À quoi ressemble..."

Et l'IA vous trouvera les images correspondantes ! 🖼️✨

---

## 📝 Notes Importantes

### Pour Render (Déploiement)

Ajoutez les variables d'environnement dans le dashboard Render :
1. Allez dans votre service
2. Environment → Add Environment Variable
3. Ajoutez vos clés API
4. Redéployez

### Pour Développement Local

Ajoutez les clés dans votre fichier `.env` :
```bash
# Recherche d'images
GOOGLE_SEARCH_API_KEY=votre_cle
GOOGLE_SEARCH_CX=votre_cx
BING_SEARCH_API_KEY=votre_cle
UNSPLASH_ACCESS_KEY=votre_cle
PIXABAY_API_KEY=votre_cle
```

### Priorité des Services

L'application essaie les services dans cet ordre :
1. Google Images (meilleure qualité)
2. Bing Images (bon backup)
3. Unsplash (photos artistiques)
4. Pixabay (gratuit illimité)

Si un service échoue, l'application essaie automatiquement le suivant !
