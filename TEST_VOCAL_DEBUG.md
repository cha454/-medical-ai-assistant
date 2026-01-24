# 🔍 Test Vocal - Guide de Débogage

## Étapes de Test

### 1. Ouvrir la Console du Navigateur
- Appuyez sur **F12** (ou Ctrl+Shift+I)
- Allez dans l'onglet **Console**

### 2. Vérifier le Chargement des Scripts
Dans la console, tapez ces commandes une par une :

```javascript
// Vérifier que les scripts sont chargés
typeof window.sendMessage
// Devrait afficher: "function"

typeof window.siriVoiceAssistant
// Devrait afficher: "object"

typeof startVoiceConversation
// Devrait afficher: "function"

typeof SiriVoiceAssistant
// Devrait afficher: "function"
```

### 3. Tester le Bouton Manuellement
Dans la console, tapez :

```javascript
// Tester directement la fonction
startVoiceConversation()
```

### 4. Vérifier les Permissions du Micro
Dans la console, tapez :

```javascript
// Vérifier les permissions
navigator.permissions.query({name: 'microphone'}).then(result => {
    console.log('Permission micro:', result.state);
});
```

### 5. Tester la Reconnaissance Vocale
Dans la console, tapez :

```javascript
// Vérifier si la reconnaissance vocale est supportée
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    console.log('✅ Reconnaissance vocale supportée');
} else {
    console.log('❌ Reconnaissance vocale NON supportée');
}
```

## Erreurs Possibles

### Erreur 1: "startVoiceConversation is not defined"
**Cause**: Le script `voice-integration.js` n'est pas chargé
**Solution**: Rafraîchir la page (Ctrl+F5)

### Erreur 2: "siriVoiceAssistant is null"
**Cause**: Le script `voice-assistant-siri.js` n'a pas initialisé l'assistant
**Solution**: Attendre 1 seconde et réessayer

### Erreur 3: "Microphone non autorisé"
**Cause**: Les permissions du micro ne sont pas accordées
**Solution**: 
1. Cliquer sur l'icône 🔒 dans la barre d'adresse
2. Autoriser le microphone
3. Rafraîchir la page

### Erreur 4: "Reconnaissance vocale non supportée"
**Cause**: Le navigateur ne supporte pas la Web Speech API
**Solution**: Utiliser Chrome, Edge ou Safari

## Test Complet

Copiez-collez ce code dans la console pour un test complet :

```javascript
console.log('=== TEST VOCAL COMPLET ===');

// 1. Scripts chargés
console.log('1. Scripts:');
console.log('   - sendMessage:', typeof window.sendMessage);
console.log('   - siriVoiceAssistant:', typeof window.siriVoiceAssistant);
console.log('   - startVoiceConversation:', typeof startVoiceConversation);
console.log('   - SiriVoiceAssistant:', typeof SiriVoiceAssistant);

// 2. Support navigateur
console.log('2. Support navigateur:');
const hasRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
console.log('   - Reconnaissance vocale:', hasRecognition ? '✅' : '❌');
console.log('   - Synthèse vocale:', 'speechSynthesis' in window ? '✅' : '❌');

// 3. État de l'assistant
if (window.siriVoiceAssistant) {
    console.log('3. État assistant:');
    console.log('   - isListening:', siriVoiceAssistant.isListening);
    console.log('   - isSpeaking:', siriVoiceAssistant.isSpeaking);
    console.log('   - handsFreeModeActive:', siriVoiceAssistant.handsFreeModeActive);
} else {
    console.log('3. ❌ Assistant non initialisé');
}

// 4. Bouton
const voiceBtn = document.getElementById('voiceBtn');
console.log('4. Bouton vocal:');
console.log('   - Trouvé:', voiceBtn ? '✅' : '❌');
if (voiceBtn) {
    console.log('   - onclick:', voiceBtn.onclick ? '✅' : '❌');
}

console.log('=== FIN TEST ===');
```

## Résultats Attendus

Si tout fonctionne, vous devriez voir :
```
=== TEST VOCAL COMPLET ===
1. Scripts:
   - sendMessage: function
   - siriVoiceAssistant: object
   - startVoiceConversation: function
   - SiriVoiceAssistant: function
2. Support navigateur:
   - Reconnaissance vocale: ✅
   - Synthèse vocale: ✅
3. État assistant:
   - isListening: false
   - isSpeaking: false
   - handsFreeModeActive: false
4. Bouton vocal:
   - Trouvé: ✅
   - onclick: ✅
=== FIN TEST ===
```

## Actions Correctives

### Si sendMessage est "undefined"
Le fichier `chat-functions.js` n'est pas chargé. Vérifiez la console pour des erreurs de chargement.

### Si siriVoiceAssistant est "undefined"
Le fichier `voice-assistant-siri.js` n'est pas chargé ou a une erreur. Vérifiez la console.

### Si startVoiceConversation est "undefined"
Le fichier `voice-integration.js` n'est pas chargé. Rafraîchissez la page avec Ctrl+F5.

### Si le bouton n'a pas de onclick
Le HTML n'est pas à jour. Videz le cache du navigateur (Ctrl+Shift+Delete).

---

**Date**: 24 janvier 2026  
**URL de test**: https://medical-ai-assistant-production.up.railway.app/chat
