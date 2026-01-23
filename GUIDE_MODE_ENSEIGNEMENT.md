# 🎓 Guide du Mode Enseignement

## 🎯 Qu'est-ce que le Mode Enseignement ?

Le Mode Enseignement permet d'**enseigner à l'IA** de nouvelles connaissances qui seront **mémorisées et réutilisées** dans toutes les conversations futures.

---

## ✨ Fonctionnalités

### 1. 🗣️ Enseignement par Conversation
- Discutez naturellement avec l'IA pour lui apprendre
- Système vocal intégré (reconnaissance + synthèse)
- L'IA confirme ce qu'elle a appris
- Sauvegarde automatique dans la base de données

### 2. 📚 Types de Connaissances

#### 🌍 Langues Locales
```
Vous : "En Fang, Nlo signifie fièvre"
IA : "✅ J'ai appris ! Nlo (Fang) = fièvre"

Vous : "Eboga est une plante médicinale"
IA : "✅ Enregistré ! Eboga = plante médicinale"
```

#### 💊 Termes Médicaux
```
Vous : "Le paludisme se dit malaria en anglais"
IA : "✅ Parfait ! Paludisme = malaria (anglais)"
```

#### 🌿 Plantes Médicinales
```
Vous : "Le Kinkeliba soigne le paludisme"
IA : "✅ Mémorisé ! Kinkeliba → traitement paludisme"
```

#### 👤 Informations Personnelles
```
Vous : "Je suis allergique à la pénicilline"
IA : "✅ Noté ! Allergie : pénicilline"
```

### 3. 💾 Sauvegarde Permanente
- Toutes les connaissances sont enregistrées dans une base de données SQLite
- Catégorisation automatique (langue, médical, plante, personnel, etc.)
- Compteur d'utilisation pour chaque connaissance
- Export/Import possible

### 4. 🔄 Réutilisation Automatique
Les connaissances apprises sont automatiquement injectées dans le contexte du chat normal :

```
[Mode Enseignement]
Vous : "Nlo signifie fièvre en Fang"
IA : "✅ Appris !"

[Chat Normal - Plus tard]
Vous : "J'ai le Nlo"
IA : "Vous avez de la fièvre (Nlo en Fang). Voici les conseils..."
```

---

## 🚀 Comment Utiliser

### Étape 1 : Accéder au Mode Enseignement
1. Cliquez sur le bouton **"🎓 Enseigner"** dans le header
2. Vous êtes redirigé vers une page dédiée

### Étape 2 : Enseigner
**Mode Texte :**
1. Tapez ce que vous voulez enseigner
2. Cliquez sur "Enseigner"
3. L'IA confirme et sauvegarde

**Mode Vocal :**
1. Cliquez sur le bouton 🎤
2. Parlez naturellement
3. L'IA répond vocalement et sauvegarde

### Étape 3 : Vérifier
1. Cliquez sur **"📚 Voir les connaissances"**
2. Consultez toutes les connaissances apprises
3. Supprimez ou modifiez si nécessaire

### Étape 4 : Retour au Chat
1. Cliquez sur **"🏠 Retour au chat"**
2. Les connaissances sont automatiquement utilisées

---

## 📋 Exemples d'Utilisation

### Exemple 1 : Enseigner une Langue Locale

**Conversation :**
```
Vous : "Bonjour ! Je veux t'apprendre le Fang"
IA : "🎓 Génial ! Je suis prêt à apprendre le Fang. Enseigne-moi !"

Vous : "En Fang, Nlo signifie fièvre"
IA : "✅ Parfait ! J'ai appris : Nlo (Fang) = fièvre. Veux-tu m'apprendre autre chose ?"

Vous : "Oui, Akoma signifie cœur"
IA : "✅ Enregistré ! Akoma (Fang) = cœur. Continue, j'adore apprendre ! 🌟"

Vous : "Nnem signifie mère"
IA : "✅ Mémorisé ! Nnem (Fang) = mère. Merci pour cet enseignement ! 📚"
```

**Résultat :**
- 3 connaissances sauvegardées
- Catégorie : langue_locale
- Langue : fang

### Exemple 2 : Plantes Médicinales

**Conversation :**
```
Vous : "Je vais t'apprendre les plantes médicinales africaines"
IA : "🎓 Excellent ! Je suis très intéressé. Enseigne-moi !"

Vous : "Le Kinkeliba soigne le paludisme"
IA : "✅ J'ai appris ! Kinkeliba → traitement paludisme. Quelle autre plante ?"

Vous : "L'Artemisia est efficace contre le paludisme aussi"
IA : "✅ Enregistré ! Artemisia → traitement paludisme. Continue ! 🌿"

Vous : "Le Moringa renforce le système immunitaire"
IA : "✅ Mémorisé ! Moringa → renforcement immunitaire. Merci ! 💚"
```

### Exemple 3 : Informations Personnelles

**Conversation :**
```
Vous : "Je veux que tu mémorises mes informations médicales"
IA : "🎓 Bien sûr ! Je vais mémoriser tes informations. Dis-moi tout."

Vous : "Je suis allergique à la pénicilline"
IA : "✅ Noté ! Allergie : pénicilline. Je m'en souviendrai toujours. Autre chose ?"

Vous : "J'ai du diabète de type 2"
IA : "✅ Enregistré ! Diabète type 2. Je prendrai ça en compte dans mes conseils."

Vous : "Je prends de la metformine tous les jours"
IA : "✅ Mémorisé ! Traitement : metformine quotidien. Merci pour ces informations ! 💊"
```

---

## 🎤 Utilisation Vocale

### Activer le Mode Vocal
1. Cliquez sur le bouton 🎤
2. Le bouton devient rouge (écoute active)
3. Parlez naturellement
4. L'IA répond vocalement
5. Le micro se réactive automatiquement

### États du Bouton
- 🎤 **Bleu** : Inactif
- 🎤 **Rouge pulsant** : Écoute en cours
- 🔊 **Vert pulsant** : IA parle

### Exemple Vocal
```
[Clic sur 🎤]
Vous : [Parle] "En Ewondo, Nkukuma signifie maladie"
IA : [Répond vocalement] "J'ai bien compris ! Nkukuma en Ewondo signifie maladie. C'est enregistré !"
[Micro se réactive automatiquement]
Vous : [Parle] "Oui, et Nganga signifie guérisseur"
IA : [Répond vocalement] "Parfait ! Nganga en Ewondo signifie guérisseur. Merci !"
```

---

## 📊 Gestion des Connaissances

### Page de Gestion
Accès : Bouton **"📚 Voir les connaissances"**

**Fonctionnalités :**
- 📋 Liste de toutes les connaissances
- 🔍 Recherche par mot-clé
- 🏷️ Filtrage par catégorie
- 🌍 Filtrage par langue
- 🗑️ Suppression
- ✏️ Modification
- 📥 Export JSON
- 📤 Import JSON

### Statistiques
- **Total** : Nombre total de connaissances
- **Par catégorie** : Répartition par type
- **Par langue** : Répartition par langue
- **Dernière mise à jour** : Date du dernier ajout

---

## 🔧 Architecture Technique

### Base de Données
```sql
Table: knowledge
- id (PRIMARY KEY)
- category (langue_locale, medical, plante, personnel, etc.)
- question (ce qui est enseigné)
- answer (la connaissance)
- language (fr, fang, ewondo, etc.)
- context (contexte de l'enseignement)
- tags (mots-clés)
- confidence (niveau de confiance)
- source (teaching_mode, import, etc.)
- date_created
- date_updated
- usage_count (nombre d'utilisations)
```

### Catégories Automatiques
1. **langue_locale** 🌍 : Langues et traductions
2. **medical** 💊 : Connaissances médicales
3. **plante** 🌿 : Plantes médicinales
4. **personnel** 👤 : Informations personnelles
5. **correction** ✏️ : Corrections et feedback
6. **preference** ⚙️ : Préférences utilisateur
7. **culture** 🎭 : Culture et traditions
8. **autre** 📚 : Autres connaissances

### Injection dans le Contexte
Les connaissances sont automatiquement injectées dans le prompt du LLM :

```
📚 CONNAISSANCES PERSONNALISÉES APPRISES :

• Nlo (Fang)
  → fièvre
  (Langue: fang)

• Kinkeliba
  → traite le paludisme
  (Langue: fr)

• Allergie
  → pénicilline
  (Langue: fr)

Utilise ces connaissances pour répondre de manière personnalisée.
```

---

## 🎯 Cas d'Usage

### 1. Médecin en Zone Rurale
```
Enseigner les termes médicaux en langues locales
→ Meilleure communication avec les patients
```

### 2. Étudiant en Médecine
```
Enseigner les plantes médicinales traditionnelles
→ Enrichir ses connaissances
```

### 3. Patient Chronique
```
Enseigner ses informations médicales
→ Conseils personnalisés
```

### 4. Chercheur
```
Enseigner des connaissances spécialisées
→ Assistant personnalisé
```

---

## 🚀 Prochaines Améliorations

### Version 2.0
- [ ] Reconnaissance automatique de la catégorie
- [ ] Suggestions de connaissances similaires
- [ ] Validation collaborative (plusieurs utilisateurs)
- [ ] Niveau de confiance ajustable
- [ ] Historique des modifications

### Version 3.0
- [ ] Apprentissage par images
- [ ] Apprentissage par documents (PDF, etc.)
- [ ] Partage de bases de connaissances
- [ ] API publique pour l'enseignement
- [ ] Gamification (points, badges)

---

## 📞 Support

### Problèmes Courants

**Q : L'IA ne retient pas ce que je lui enseigne**
R : Vérifiez que la base de données `knowledge.db` est créée et accessible

**Q : Le vocal ne fonctionne pas**
R : Vérifiez les permissions microphone et utilisez HTTPS

**Q : Comment supprimer une connaissance ?**
R : Allez dans "📚 Voir les connaissances" et cliquez sur 🗑️

**Q : Puis-je partager mes connaissances ?**
R : Oui, utilisez l'export JSON et partagez le fichier

---

## 🎉 Conclusion

Le Mode Enseignement transforme votre assistant médical en un **outil personnalisé** qui apprend de vous et s'adapte à vos besoins spécifiques.

**Commencez dès maintenant :**
1. Cliquez sur 🎓 Enseigner
2. Parlez ou écrivez
3. L'IA apprend et mémorise !

---

**Créé le** : 23 janvier 2026  
**Version** : 1.0  
**Statut** : ✅ Fonctionnel
