/**
 * Système Vocal Ultra-Simple
 * UN CLIC = CONVERSATION AUTOMATIQUE
 */

// Fonction principale - Démarrer la conversation vocale
function startVoiceConversation() {
    console.log('🎤 Démarrage conversation vocale...');

    if (!window.siriVoiceAssistant) {
        console.error('❌ Assistant vocal non disponible');
        alert('Le système vocal n\'est pas encore chargé. Veuillez rafraîchir la page.');
        return;
    }

    const voiceBtn = document.getElementById('voiceBtn');

    // Si déjà en mode mains libres, arrêter
    if (siriVoiceAssistant.handsFreeModeActive) {
        console.log('🛑 Arrêt conversation vocale');
        siriVoiceAssistant.toggleHandsFreeMode();
        if (voiceBtn) {
            voiceBtn.classList.remove('hands-free', 'listening', 'speaking');
        }
        showNotification('Conversation vocale arrêtée', 'info');
        return;
    }

    // Démarrer le mode mains libres automatiquement
    console.log('🤚 Activation mode mains libres');
    siriVoiceAssistant.toggleHandsFreeMode();

    if (voiceBtn) {
        voiceBtn.classList.add('hands-free');
    }

    showNotification('🎤 Parlez maintenant !', 'success');
}

// Mettre à jour l'UI du bouton
function updateVoiceButton(state) {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!voiceBtn) return;

    // Ne pas enlever la classe hands-free
    const isHandsFree = voiceBtn.classList.contains('hands-free');

    voiceBtn.classList.remove('listening', 'speaking');

    switch (state) {
        case 'listening':
            voiceBtn.classList.add('listening');
            break;
        case 'speaking':
            voiceBtn.classList.add('speaking');
            break;
        case 'idle':
        default:
            if (isHandsFree) {
                voiceBtn.classList.add('hands-free');
            }
            break;
    }
}

// Afficher une notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('voice-notification');
    if (notification) {
        notification.textContent = message;
        notification.className = `voice-notification ${type}`;
        notification.style.display = 'block';

        setTimeout(() => {
            notification.style.display = 'none';
        }, 2000);
    }
}

// Intégration avec le système Siri
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎤 Initialisation système vocal ultra-simple...');

    // Attendre que siriVoiceAssistant soit initialisé
    setTimeout(() => {
        if (window.siriVoiceAssistant) {
            console.log('✓ Système vocal prêt !');

            // Remplacer la fonction updateUI
            siriVoiceAssistant.updateUI = function (state) {
                updateVoiceButton(state);
            };

            // Message de bienvenue
            setTimeout(() => {
                showNotification('Cliquez sur 🎤 pour parler !', 'info');
            }, 1000);
        } else {
            console.error('❌ Assistant vocal non chargé');
        }
    }, 500);
});

// Fonction de compatibilité (au cas où)
function toggleVoiceConversation() {
    startVoiceConversation();
}
