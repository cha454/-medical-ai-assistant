# 🧪 Guide de Test - Système Vocal Amélioré

## 🎯 Objectif
Tester toutes les nouvelles fonctionnalités vocales implémentées.

---

## ⚙️ Prérequis

### 1. Navigateur
- ✅ Chrome ou Edge (recommandé)
- ⚠️ Safari (support limité)
- ❌ Firefox (non recommandé)

### 2. Permissions
- 🎤 Autoriser l'accès au microphone
- 🔊 Activer le son du système
- 🔒 Utiliser HTTPS (déjà configuré sur Render)

### 3. Environnement
- Endroit calme pour les tests vocaux
- Microphone fonctionnel
- Haut-parleurs ou casque

---

## 📋 Tests à Effectuer

### TEST 1 : Feedback Sonore 🔊

**Objectif** : Vérifier que les sons se jouent correctement

#### Étapes :
1. Ouvrir la page de chat
2. Cliquer sur le bouton 🎤
3. **Vérifier** : Son "Ding" (800 Hz) au démarrage
4. Parler quelques mots
5. Attendre la fin de la reconnaissance
6. **Vérifier** : Son "Bip" (600 Hz) à la fin
7. **Vérifier** : Son "Swoosh" (1000→200 Hz) à l'envoi
8. Provoquer une erreur (refuser le micro)
9. **Vérifier** : Son d'erreur (300 Hz)

#### Résultat Attendu :
- ✅ 4 sons distincts et audibles
- ✅ Sons joués au bon moment
- ✅ Pas de latence excessive

#### En cas d'échec :
- Vérifier le volume du système
- Vérifier que le navigateur peut jouer des sons
- Ouvrir la console (F12) pour voir les erreurs

---

### TEST 2 : Visualisation Audio 📊

**Objectif** : Vérifier l'animation des barres audio

#### Étapes :
1. Cliquer sur le bouton 🎤
2. **Vérifier** : 6 barres apparaissent en bas du bouton
3. **Vérifier** : Barres animées avec effet de vague
4. **Vérifier** : Couleur rouge pendant l'écoute
5. Parler et attendre la réponse de l'IA
6. **Vérifier** : Couleur verte pendant que l'IA parle
7. **Vérifier** : Barres disparaissent quand inactif

#### Résultat Attendu :
- ✅ 6 barres visibles et animées
- ✅ Animation fluide (pas de saccades)
- ✅ Couleurs correctes (rouge/vert)
- ✅ Synchronisation avec l'état vocal

#### En cas d'échec :
- Vérifier que le CSS est chargé
- Rafraîchir la page (Ctrl+F5)
- Vérifier la console pour erreurs CSS

---

### TEST 3 : Commandes Vocales 🗣️

**Objectif** : Tester les 10 commandes vocales

#### Test 3.1 : Commande "Stop"
1. Démarrer la conversation vocale (🎤)
2. Dire clairement : **"Stop"**
3. **Vérifier** : Conversation arrêtée
4. **Vérifier** : Bouton redevient bleu
5. **Vérifier** : Son "Swoosh" joué

#### Test 3.2 : Commande "Répète"
1. Poser une question : "Quels sont les symptômes du diabète ?"
2. Attendre la réponse
3. Dire : **"Répète"**
4. **Vérifier** : Même réponse rejouée
5. **Vérifier** : Son "Swoosh" joué

#### Test 3.3 : Commande "Plus fort"
1. En conversation vocale
2. Dire : **"Plus fort"**
3. **Vérifier** : Volume augmente
4. **Vérifier** : Son "Ding" joué
5. Répéter 2-3 fois
6. **Vérifier** : Volume maximum à 100%

#### Test 3.4 : Commande "Moins fort"
1. Dire : **"Moins fort"**
2. **Vérifier** : Volume diminue
3. **Vérifier** : Son "Bip" joué
4. Répéter 2-3 fois
5. **Vérifier** : Volume minimum à 20%

#### Test 3.5 : Commande "Plus vite"
1. Dire : **"Plus vite"**
2. **Vérifier** : Vitesse augmente
3. **Vérifier** : Son "Ding" joué
4. Poser une question pour tester
5. **Vérifier** : Réponse plus rapide

#### Test 3.6 : Commande "Moins vite"
1. Dire : **"Moins vite"**
2. **Vérifier** : Vitesse diminue
3. **Vérifier** : Son "Bip" joué
4. Poser une question pour tester
5. **Vérifier** : Réponse plus lente

#### Test 3.7 : Commande "Mode discret"
1. Dire : **"Mode discret"**
2. **Vérifier** : Bouton 🔇 devient 🔕 (jaune)
3. **Vérifier** : Son "Swoosh" joué
4. Poser une question
5. **Vérifier** : Réponse en texte uniquement (pas de voix)

#### Test 3.8 : Commande "Nouveau"
1. Avoir quelques messages dans le chat
2. Dire : **"Nouveau"**
3. **Vérifier** : Chat effacé
4. **Vérifier** : Empty state affiché
5. **Vérifier** : Son "Swoosh" joué

#### Résultat Attendu :
- ✅ Toutes les commandes reconnues
- ✅ Actions exécutées correctement
- ✅ Feedback sonore approprié
- ✅ Pas d'envoi de message pour les commandes

#### En cas d'échec :
- Parler plus clairement et distinctement
- Vérifier la langue du navigateur (fr-FR)
- Ouvrir la console pour voir les logs
- Vérifier que `detectVoiceCommand()` fonctionne

---

### TEST 4 : Paramètres Vocaux ⚙️

**Objectif** : Tester le menu de configuration

#### Test 4.1 : Ouverture du Menu
1. Cliquer sur le bouton ⚙️
2. **Vérifier** : Menu apparaît avec animation
3. **Vérifier** : 4 sections visibles :
   - Voix (menu déroulant)
   - Vitesse (curseur)
   - Tonalité (curseur)
   - Volume (curseur)

#### Test 4.2 : Changement de Voix
1. Ouvrir le menu ⚙️
2. Cliquer sur le menu déroulant "Voix"
3. **Vérifier** : Liste de voix françaises
4. Sélectionner une voix différente
5. **Vérifier** : Son "Ding" joué
6. Fermer le menu (clic en dehors)
7. Poser une question vocale
8. **Vérifier** : Nouvelle voix utilisée

#### Test 4.3 : Ajustement Vitesse
1. Ouvrir le menu ⚙️
2. Déplacer le curseur "Vitesse"
3. **Vérifier** : Valeur affichée change (ex: 1.2x)
4. Tester avec 0.5x (très lent)
5. Tester avec 2.0x (très rapide)
6. Poser une question
7. **Vérifier** : Vitesse appliquée

#### Test 4.4 : Ajustement Tonalité
1. Ouvrir le menu ⚙️
2. Déplacer le curseur "Tonalité"
3. **Vérifier** : Valeur affichée change (ex: 0.9)
4. Tester avec 0.5 (grave)
5. Tester avec 2.0 (aigu)
6. Poser une question
7. **Vérifier** : Tonalité appliquée

#### Test 4.5 : Ajustement Volume
1. Ouvrir le menu ⚙️
2. Déplacer le curseur "Volume"
3. **Vérifier** : Valeur affichée change (ex: 80%)
4. Tester avec 0% (muet)
5. Tester avec 100% (maximum)
6. Poser une question
7. **Vérifier** : Volume appliqué

#### Test 4.6 : Fermeture du Menu
1. Menu ouvert
2. Cliquer en dehors du menu
3. **Vérifier** : Menu se ferme
4. Cliquer sur ⚙️ à nouveau
5. **Vérifier** : Menu se rouvre avec les valeurs sauvegardées

#### Résultat Attendu :
- ✅ Menu s'ouvre/ferme correctement
- ✅ Tous les curseurs fonctionnent
- ✅ Valeurs affichées en temps réel
- ✅ Paramètres appliqués immédiatement
- ✅ Paramètres persistants (sauvegardés)

#### En cas d'échec :
- Vérifier que le JavaScript est chargé
- Vérifier la console pour erreurs
- Rafraîchir la page
- Vérifier que `voiceSettings` est défini

---

### TEST 5 : Mode Discret 🔕

**Objectif** : Tester le mode silencieux

#### Test 5.1 : Activation Manuelle
1. Cliquer sur le bouton 🔇
2. **Vérifier** : Bouton devient 🔕 (jaune)
3. **Vérifier** : Titre change : "Mode discret activé"
4. Démarrer conversation vocale
5. Poser une question
6. **Vérifier** : Réponse en texte uniquement
7. **Vérifier** : Pas de synthèse vocale
8. **Vérifier** : Micro se réactive quand même

#### Test 5.2 : Désactivation
1. Mode discret activé (🔕 jaune)
2. Cliquer à nouveau sur 🔕
3. **Vérifier** : Bouton redevient 🔇 (gris)
4. **Vérifier** : Titre : "Mode discret"
5. Poser une question
6. **Vérifier** : Réponse vocale normale

#### Test 5.3 : Activation Vocale
1. En conversation vocale
2. Dire : **"Mode discret"**
3. **Vérifier** : Bouton devient 🔕 (jaune)
4. **Vérifier** : Son "Swoosh" joué
5. Poser une question
6. **Vérifier** : Réponse silencieuse

#### Test 5.4 : Combinaison avec Paramètres
1. Activer mode discret
2. Ouvrir menu ⚙️
3. Changer vitesse, tonalité, volume
4. Désactiver mode discret
5. Poser une question
6. **Vérifier** : Paramètres appliqués

#### Résultat Attendu :
- ✅ Bouton change d'apparence
- ✅ Mode activable par clic ou voix
- ✅ Pas de synthèse vocale en mode discret
- ✅ Reconnaissance vocale continue de fonctionner
- ✅ Paramètres sauvegardés

#### En cas d'échec :
- Vérifier que `isSilentMode` est défini
- Vérifier la fonction `speakText()`
- Vérifier la console pour erreurs
- Vérifier le CSS du bouton

---

## 🎭 Tests de Scénarios Complets

### SCÉNARIO 1 : Consultation Médicale Complète
```
1. Cliquer sur 🎤 → Son "Ding"
2. Dire : "Quels sont les symptômes du diabète ?"
3. Écouter la réponse → Barres vertes animées
4. Dire : "Plus lent" → Son "Bip"
5. Dire : "Répète" → Réponse rejouée plus lentement
6. Dire : "Merci" → Réponse normale
7. Dire : "Stop" → Son "Swoosh", conversation arrêtée
```

### SCÉNARIO 2 : Personnalisation Avancée
```
1. Cliquer sur ⚙️
2. Sélectionner voix féminine
3. Vitesse : 1.2x
4. Tonalité : 0.9
5. Volume : 80%
6. Fermer le menu
7. Cliquer sur 🎤
8. Poser une question
9. Vérifier que tous les paramètres sont appliqués
```

### SCÉNARIO 3 : Mode Discret en Public
```
1. Cliquer sur 🔇 → Devient 🔕 (jaune)
2. Cliquer sur 🎤
3. Dire : "Comment traiter une migraine ?"
4. Lire la réponse en texte
5. Dire : "Répète"
6. Relire la réponse
7. Dire : "Mode discret" → Désactive (🔇 gris)
8. Dire : "Merci" → Réponse vocale
```

### SCÉNARIO 4 : Contrôle Vocal Total
```
1. Cliquer sur 🎤
2. Dire : "Plus vite"
3. Dire : "Plus fort"
4. Poser une question
5. Dire : "Répète"
6. Dire : "Moins vite"
7. Dire : "Moins fort"
8. Dire : "Nouveau" → Chat effacé
9. Dire : "Stop"
```

---

## 📊 Checklist de Test

### Feedback Sonore
- [ ] Son "Ding" au démarrage
- [ ] Son "Bip" à la fin
- [ ] Son "Swoosh" à l'envoi
- [ ] Son d'erreur en cas de problème

### Visualisation Audio
- [ ] 6 barres visibles
- [ ] Animation fluide
- [ ] Couleur rouge (écoute)
- [ ] Couleur verte (parle)

### Commandes Vocales
- [ ] "Stop" / "Arrête"
- [ ] "Répète" / "Encore"
- [ ] "Plus fort"
- [ ] "Moins fort"
- [ ] "Plus vite"
- [ ] "Moins vite"
- [ ] "Mode discret"
- [ ] "Nouveau"

### Paramètres Vocaux
- [ ] Menu s'ouvre/ferme
- [ ] Sélection de voix
- [ ] Curseur vitesse
- [ ] Curseur tonalité
- [ ] Curseur volume
- [ ] Valeurs affichées
- [ ] Paramètres appliqués

### Mode Discret
- [ ] Activation par clic
- [ ] Activation vocale
- [ ] Bouton change d'apparence
- [ ] Pas de synthèse vocale
- [ ] Reconnaissance continue

---

## 🐛 Problèmes Connus et Solutions

### Problème 1 : Microphone non autorisé
**Symptôme** : Erreur "not-allowed"  
**Solution** : 
1. Chrome : chrome://settings/content/microphone
2. Autoriser le site
3. Rafraîchir la page

### Problème 2 : Pas de son
**Symptôme** : Aucun feedback sonore  
**Solution** :
1. Vérifier volume système
2. Vérifier volume navigateur
3. Tester avec un autre site audio
4. Vérifier console pour erreurs Web Audio API

### Problème 3 : Commandes non reconnues
**Symptôme** : Commandes envoyées comme messages  
**Solution** :
1. Parler plus clairement
2. Utiliser les commandes exactes
3. Vérifier langue navigateur (fr-FR)
4. Ouvrir console pour voir les logs

### Problème 4 : Voix robotique
**Symptôme** : Synthèse vocale de mauvaise qualité  
**Solution** :
1. Changer de voix dans ⚙️
2. Ajuster vitesse (0.9x - 1.1x)
3. Ajuster tonalité (0.9 - 1.1)
4. Utiliser Chrome/Edge

### Problème 5 : Menu ne s'ouvre pas
**Symptôme** : Clic sur ⚙️ sans effet  
**Solution** :
1. Vérifier console pour erreurs
2. Rafraîchir la page (Ctrl+F5)
3. Vérifier que JavaScript est activé
4. Vider le cache

---

## 📝 Rapport de Test

### Informations
- **Date** : _______________
- **Navigateur** : _______________
- **Version** : _______________
- **OS** : _______________

### Résultats
- Feedback Sonore : ⬜ OK ⬜ KO
- Visualisation Audio : ⬜ OK ⬜ KO
- Commandes Vocales : ⬜ OK ⬜ KO
- Paramètres Vocaux : ⬜ OK ⬜ KO
- Mode Discret : ⬜ OK ⬜ KO

### Notes
```
_________________________________________________
_________________________________________________
_________________________________________________
```

### Bugs Trouvés
```
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## 🚀 Prochaines Étapes

Si tous les tests passent :
1. ✅ Déployer sur Render
2. ✅ Tester en production (HTTPS)
3. ✅ Partager avec les utilisateurs
4. ✅ Collecter les retours

Si des bugs sont trouvés :
1. ❌ Noter les détails dans le rapport
2. ❌ Ouvrir la console pour les erreurs
3. ❌ Prendre des captures d'écran
4. ❌ Signaler les problèmes

---

**Bon test ! 🎉**
