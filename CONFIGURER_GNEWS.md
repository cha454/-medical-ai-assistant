# 🚀 Configurer GNews API - Guide Complet

## 🎯 POURQUOI GNEWS ?

**GNews est meilleur que NewsAPI :**
- ✅ **100 requêtes/jour GRATUIT** (vs 100 pour NewsAPI)
- ✅ **Meilleure couverture internationale**
- ✅ **Plus d'articles par recherche**
- ✅ **API plus rapide et stable**
- ✅ **Pas de limitation par pays**

---

## ⚡ ACTIVATION EN 5 MINUTES

### Étape 1 : Créer un compte (2 min)

1. **Va sur :** https://gnews.io

2. **Clique sur** **"Get API Key"** ou **"Sign Up"**

3. **Inscris-toi avec :**
   - Email
   - Ou Google
   - Ou GitHub

4. **Vérifie ton email** (clique sur le lien de confirmation)

---

### Étape 2 : Obtenir la clé API (1 min)

1. **Une fois connecté**, tu arrives sur le dashboard

2. **Ta clé API est affichée** directement sur la page d'accueil

3. **Copie la clé** :
   - Format : `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Environ 32 caractères

**⚠️ IMPORTANT : Sauvegarde la clé dans un endroit sûr !**

---

### Étape 3 : Tester la clé (1 min) - IMPORTANT

**Test avec curl (Windows PowerShell) :**
```powershell
curl "https://gnews.io/api/v4/search?q=actualités&lang=fr&apikey=TA_CLE_ICI"
```

**Ou test avec Python :**
```python
import requests

api_key = "TA_CLE_ICI"
url = f"https://gnews.io/api/v4/search?q=actualités&lang=fr&apikey={api_key}"

response = requests.get(url)
print(response.status_code)  # Doit être 200
print(response.json())
```

**Si ça marche, tu verras des articles en JSON.**
**Si erreur 401, la clé est invalide → recommence l'étape 2.**

---

### Étape 4 : Ajouter dans Render (1 min)

1. **Va sur Render.com** → Ton service

2. **Onglet Environment**

3. **Clique sur** **"Add Environment Variable"**

4. **Key :** `GNEWS_API_KEY`

5. **Value :** [Colle ta clé GNews]

6. ⚠️ **VÉRIFIE qu'il n'y a pas d'espaces avant/après**

7. **Save Changes**

8. **Attends 2-3 minutes** (Render redémarre)

---

### Étape 5 : Vérifier (30 sec)

1. **Render → Logs**

Tu devrais voir :
```
✓ Service actualités hybride activé (GNews + RSS)
```

2. **Teste sur ton site :**
   - https://medical-ai-assistant-2k1a.onrender.com/chat
   - Demande : "Quelles sont les dernières actualités ?"
   - Tu devrais avoir des articles ! 🎉

---

## 📊 PLANS GNEWS

### Plan Gratuit (Actuel)
- **100 requêtes/jour**
- **10 articles par requête**
- **Toutes les langues**
- **Toutes les catégories**

**Parfait pour commencer ! ✅**

### Plan Starter ($9/mois)
- **10,000 requêtes/jour**
- **10 articles par requête**
- **Support prioritaire**

### Plan Pro ($49/mois)
- **100,000 requêtes/jour**
- **100 articles par requête**
- **Support premium**

**Pour toi : Le plan gratuit est largement suffisant ! 💰**

---

## 🌍 FONCTIONNALITÉS GNEWS

### Recherche par langue
```
lang=fr  → Français
lang=en  → Anglais
lang=es  → Espagnol
```

### Recherche par catégorie
```
topic=health      → Santé
topic=sports      → Sport
topic=technology  → Tech
topic=science     → Science
topic=business    → Business
```

### Recherche par pays
```
country=fr  → France
country=us  → USA
country=ma  → Maroc
```

### Recherche par mots-clés
```
q=Gabon           → Articles sur le Gabon
q=CAN 2025        → Articles sur la CAN
q=santé Afrique   → Articles santé en Afrique
```

---

## 🆘 DÉPANNAGE

### Problème : Erreur 401 - Invalid API Key

**Solution :**
1. Vérifie que la clé est correcte (32 caractères)
2. Vérifie qu'il n'y a pas d'espaces
3. Régénère une nouvelle clé sur https://gnews.io

### Problème : Erreur 429 - Too Many Requests

**Solution :**
- Tu as dépassé 100 requêtes/jour
- Attends 24h (quota se renouvelle)
- Ou passe au plan payant ($9/mois)

### Problème : Pas d'articles trouvés

**Solution :**
- Essaie une recherche plus générale
- Vérifie l'orthographe
- Change la langue (lang=en au lieu de lang=fr)

---

## 💡 COMBINAISON GNEWS + RSS

**Ton app utilise maintenant les DEUX :**

### GNews API (International)
- Actualités mondiales
- Actualités générales
- Actualités par catégorie

### RSS Feeds (Afrique)
- Actualités africaines spécifiques
- Sources locales (Gabon, Maroc, etc.)
- 100% gratuit et illimité

**Résultat : Meilleure couverture ! 🎉**

---

## 📋 CHECKLIST

- [ ] Compte GNews créé
- [ ] Clé API obtenue
- [ ] Clé testée avec curl/Python
- [ ] Clé ajoutée dans Render (`GNEWS_API_KEY`)
- [ ] Render redémarré (2-3 min)
- [ ] Logs vérifiés : `✓ Service actualités hybride activé`
- [ ] App testée : Actualités fonctionnent

---

## 🎉 RÉSULTAT ATTENDU

**Avant (NewsAPI seul) :**
```
⚠️ 100 requêtes/jour
⚠️ Peu d'articles africains
⚠️ Recherche limitée
```

**Après (GNews + RSS) :**
```
✅ 100 requêtes/jour GNews
✅ Illimité RSS (gratuit)
✅ Meilleure couverture africaine
✅ Plus d'articles par recherche
✅ Sources locales africaines
```

**Ton service d'actualités est maintenant 10× meilleur ! 🚀**

---

## 📞 SUPPORT

### GNews
- **Site :** https://gnews.io
- **Docs :** https://gnews.io/docs/v4
- **Dashboard :** https://gnews.io/dashboard

### Besoin d'aide ?
- **Ce guide :** `CONFIGURER_GNEWS.md`
- **Service hybride :** `news_service_v2.py`

---

## 🚀 PRÊT ?

**Commence ici :**

1. **Créer compte :** https://gnews.io
2. **Copier clé API**
3. **Ajouter dans Render :** `GNEWS_API_KEY`
4. **Tester !**

**Temps : 5 minutes**
**Résultat : Actualités 10× meilleures ! 🎉**

---

## 💡 NOTE IMPORTANTE

**GNews est OPTIONNEL :**
- Si tu n'ajoutes pas la clé, l'app utilisera seulement RSS (gratuit et illimité)
- RSS seul donne déjà de bons résultats pour l'Afrique
- GNews améliore les actualités internationales

**Recommandation : Ajoute GNews pour le meilleur résultat ! ✅**
