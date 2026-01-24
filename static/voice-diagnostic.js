/**
 * Diagnostic du système vocal
 * Ce fichier aide à identifier pourquoi le système vocal ne se charge pas
 */

console.log('=== DIAGNOSTIC SYSTÈME VOCAL ===');
console.log('1. Vérification des fichiers chargés...');

// Vérifier si les classes/fonctions sont disponibles
setTimeout(() => {
    console.log('2. Vérification après 1 seconde:');
    console.log('   - SiriVoiceAssistant class:', typeof SiriVoiceAssistant);
    console.log('   - siriVoiceAssistant instance:', typeof window.siriVoiceAssistant);
    console.log('   - startVoiceConversation:', typeof startVoiceConversation);

    if (typeof SiriVoiceAssistant === 'undefined') {
        console.error('❌ PROBLÈME: La classe SiriVoiceAssistant n\'est pas définie');
        console.error('   → Le fichier voice-assistant-siri.js n\'est pas chargé ou a une erreur');
    }

    if (!window.siriVoiceAssistant) {
        console.error('❌ PROBLÈME: L\'instance siriVoiceAssistant n\'existe pas');
        console.error('   → L\'initialisation a échoué');

        // Essayer de créer l'instance manuellement
        if (typeof SiriVoiceAssistant !== 'undefined') {
            console.log('⚠️ Tentative de création manuelle...');
            try {
                window.siriVoiceAssistant = new SiriVoiceAssistant();
                console.log('✅ Instance créée manuellement !');
            } catch (error) {
                console.error('❌ Erreur lors de la création:', error);
            }
        }
    } else {
        console.log('✅ Système vocal correctement chargé !');
    }
}, 1000);

// Vérifier après 3 secondes
setTimeout(() => {
    console.log('3. Vérification finale après 3 secondes:');
    console.log('   - siriVoiceAssistant:', window.siriVoiceAssistant ? '✅ OK' : '❌ MANQUANT');
    console.log('   - window.sendMessage:', typeof window.sendMessage === 'function' ? '✅ OK' : '❌ MANQUANT');

    if (!window.siriVoiceAssistant) {
        console.error('❌ ÉCHEC FINAL: Le système vocal n\'est pas disponible');
        console.error('   Solutions possibles:');
        console.error('   1. Vérifier la console pour des erreurs JavaScript');
        console.error('   2. Vérifier que voice-assistant-siri.js se charge (onglet Network)');
        console.error('   3. Vider le cache du navigateur (Ctrl+Shift+Delete)');
    }

    if (typeof window.sendMessage !== 'function') {
        console.error('❌ ÉCHEC: window.sendMessage n\'est pas disponible');
        console.error('   → Le fichier chat-functions.js n\'est pas chargé ou a une erreur');
    }
}, 3000);
