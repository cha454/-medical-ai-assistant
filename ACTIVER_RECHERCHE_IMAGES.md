# 🖼️ Activer la Recherche d'Images - Guide Rapide

## ✅ Votre Fonctionnalité Fonctionne !

Le message que vous avez vu est **normal** - la fonctionnalité est bien intégrée, il faut juste ajouter une clé API.

## 🚀 Activation en 3 Minutes (Pixabay - GRATUIT)

### Étape 1 : Obtenir la Clé API (2 minutes)

1. **Allez sur** : https://pixabay.com/accounts/register/
2. **Créez un compte gratuit** (email + mot de passe)
3. **Allez sur** : https://pixabay.com/api/docs/
4. **Votre clé API s'affiche directement** en haut de la page
5. **Copiez la clé** (format : `12345678-abc123def456...`)

### Étape 2 : Ajouter la Clé dans Render (1 minute)

1. **Allez sur** : https://dashboard.render.com/
2. **Cliquez sur votre service** : medical-ai-assistant
3. **Allez dans** : Environment
4. **Cliquez sur** : Add Environment Variable
5. **Ajoutez** :
   - Key : `PIXABAY_API_KEY`
   - Value : `votre_cle_copiee`
6. **Cliquez sur** : Save Changes

### Étape 3 : Redéployer (automatique)

Render va automatiquement redéployer votre application avec la nouvelle variable.

**Attendez 2-3 minutes** que le déploiement se termine.

### Étape 4 : Tester ! 🎉

Retournez sur votre site et demandez :
```
"Montre-moi une image de la tour Eiffel"
"Photo du cœur humain"
"Image de poumons"
```

L'IA va maintenant afficher 6 images avec détails ! 🖼️

---

## 📊 Limites Pixabay (Gratuit)

- ✅ **5000 requêtes/heure** (largement suffisant)
- ✅ **Totalement gratuit**
- ✅ **Pas de carte bancaire requise**
- ✅ **Images libres de droits**

---

## 🎯 Exemples de Demandes

Une fois activé, vous pourrez demander :

### Images Médicales
```
"Montre-moi une image du cœur humain"
"Photo de poumons"
"Image d'un cerveau"
"À quoi ressemble une fracture"
"Affiche-moi des cellules"
```

### Images Générales
```
"Photo de la tour Eiffel"
"Image d'un chat"
"Montre-moi un coucher de soleil"
"Photo de montagne"
```

### Réponse de l'IA

```
🖼️ **6 images trouvées** (source: Pixabay)

**Recherche:** tour Eiffel

**Image 1:**
- 📸 Titre: Eiffel Tower Paris France
- 🔗 URL: https://pixabay.com/photos/...
- 📏 Dimensions: 1920x1280
- 👤 Photographe: JohnDoe

**Image 2:**
[...]

⚠️ **Note importante:**
- Ces images proviennent du web et sont à but éducatif uniquement
- Pour un diagnostic médical, consultez toujours un professionnel de santé
```

---

## 🐛 Problèmes ?

### "Aucune image trouvée"

**Vérifiez que :**
1. ✅ Vous avez bien ajouté `PIXABAY_API_KEY` dans Render
2. ✅ La clé est correcte (pas d'espaces avant/après)
3. ✅ Le déploiement est terminé (attendez 2-3 minutes)
4. ✅ Vous avez rafraîchi la page du chat

### "API Error"

**Solutions :**
1. Vérifiez que votre compte Pixabay est actif
2. Régénérez une nouvelle clé API
3. Vérifiez que vous n'avez pas dépassé la limite (5000/heure)

---

## 🎉 C'est Tout !

Une fois la clé ajoutée, la recherche d'images fonctionnera **immédiatement** !

**Temps total : 3 minutes** ⏱️

---

## 💡 Alternatives (Si Pixabay ne Fonctionne Pas)

### Option 2 : Google Images (Meilleure Qualité)

**Avantages :** Meilleurs résultats, filtrage médical
**Inconvénient :** Configuration plus complexe

**Configuration :**
1. Allez sur : https://console.cloud.google.com/
2. Créez un projet
3. Activez "Custom Search API"
4. Créez une clé API
5. Créez un moteur sur : https://programmablesearchengine.google.com/
6. Ajoutez dans Render :
   - `GOOGLE_SEARCH_API_KEY=votre_cle`
   - `GOOGLE_SEARCH_CX=votre_cx`

**Limite :** 100 requêtes/jour gratuit

### Option 3 : Bing Images

**Avantages :** Bonne qualité, 1000 requêtes/mois
**Inconvénient :** Nécessite Azure

**Configuration :**
1. Allez sur : https://portal.azure.com/
2. Créez "Bing Search v7"
3. Récupérez la clé
4. Ajoutez dans Render : `BING_SEARCH_API_KEY=votre_cle`

**Limite :** 1000 requêtes/mois gratuit

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **GUIDE_RECHERCHE_IMAGES.md** - Guide complet
- **RESUME_RECHERCHE_IMAGES.md** - Résumé technique

---

## ✅ Checklist Rapide

- [ ] Créer un compte Pixabay
- [ ] Copier la clé API
- [ ] Ajouter `PIXABAY_API_KEY` dans Render
- [ ] Attendre le redéploiement (2-3 min)
- [ ] Tester : "Montre-moi une image de..."
- [ ] 🎉 Profiter !

**Bonne recherche d'images ! 🖼️✨**
