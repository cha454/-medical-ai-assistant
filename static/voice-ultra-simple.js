/**
 * Système Vocal Ultra-Simple avec Retry
 * UN CLIC = CONVERSATION AUTOMATIQUE
 */

// Fonction principale - Démarrer la conversation vocale
function startVoiceConversation() {
    console.log('🎤 Clic sur le bouton vocal...');

    // Vérifier si le système vocal est chargé
    if (!window.siriVoiceAssistant) {
        console.warn('⏳ Système vocal en cours de chargement...');
        showNotification('⏳ Chargement du système vocal...', 'info');

        // Réessayer après 1 seconde
        setTimeout(() => {
            if (window.siriVoiceAssistant) {
                console.log('✓ Système vocal chargé !');
                startVoiceConversation();
            } else {
                console.error('❌ Système vocal toujours pas chargé');
                showNotification('⚠️ Veuillez patienter...', 'info');

                // Dernière tentative après 2 secondes
                setTimeout(() => {
                    if (window.siriVoiceAssistant) {
                        startVoiceConversation();
                    } else {
                        alert('Le système vocal n\'est pas disponible.\nVeuillez rafraîchir la page (F5).');
                    }
                }, 2000);
            }
        }, 1000);
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
        }, 2500);
    }
}

// Initialisation avec retry automatique
let initRetryCount = 0;
const maxRetries = 15; // 15 tentatives = 7.5 secondes

function initVoiceSystem() {
    if (window.siriVoiceAssistant) {
        console.log('✓ Système vocal Siri prêt !');

        // Remplacer la fonction updateUI
        const originalUpdateUI = siriVoiceAssistant.updateUI;
        siriVoiceAssistant.updateUI = function (state) {
            updateVoiceButton(state);
            if (originalUpdateUI) {
                originalUpdateUI.call(siriVoiceAssistant, state);
            }
        };

        // Message de bienvenue
        setTimeout(() => {
            showNotification('✅ Système vocal prêt ! Cliquez sur 🎤', 'success');
        }, 1000);

        return true;
    }

    initRetryCount++;
    if (initRetryCount < maxRetries) {
        console.log(`⏳ Attente du système vocal... (${initRetryCount}/${maxRetries})`);
        setTimeout(initVoiceSystem, 500);
    } else {
        console.error('❌ Impossible de charger le système vocal');
        showNotification('❌ Système vocal non disponible - Rafraîchir la page', 'error');
    }

    return false;
}

// Démarrage automatique
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🎤 Initialisation système vocal...');
        setTimeout(initVoiceSystem, 300);
    });
} else {
    // DOM déjà chargé
    console.log('🎤 DOM déjà chargé, initialisation immédiate...');
    setTimeout(initVoiceSystem, 300);
}

// Fonction de compatibilité
function toggleVoiceConversation() {
    startVoiceConversation();
}
