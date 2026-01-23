/**
 * Interface Vocale Simplifiée Style Siri
 * UN SEUL BOUTON avec menu contextuel
 */

// État global
let isHandsFreeModeActive = false;
let isSilentModeActive = false;

// Afficher le menu contextuel
function showVoiceMenu(event) {
    event.preventDefault();

    const menu = document.getElementById('voiceContextMenu');
    if (!menu) return;

    // Positionner le menu
    menu.style.left = event.pageX + 'px';
    menu.style.top = event.pageY + 'px';
    menu.classList.add('active');

    // Mettre à jour les textes
    updateMenuTexts();

    // Fermer le menu en cliquant ailleurs
    setTimeout(() => {
        document.addEventListener('click', closeVoiceMenu);
    }, 100);
}

// Fermer le menu contextuel
function closeVoiceMenu() {
    const menu = document.getElementById('voiceContextMenu');
    if (menu) {
        menu.classList.remove('active');
    }
    document.removeEventListener('click', closeVoiceMenu);
}

// Mettre à jour les textes du menu
function updateMenuTexts() {
    // Mode Mains Libres
    const handsFreeText = document.getElementById('handsFreeModeText');
    if (handsFreeText) {
        handsFreeText.textContent = isHandsFreeModeActive ?
            'Désactiver Mains Libres' : 'Mode Mains Libres';
    }

    // Mode Discret
    const silentIcon = document.getElementById('silentModeIcon');
    const silentText = document.getElementById('silentModeText');
    if (silentIcon && silentText) {
        silentIcon.textContent = isSilentModeActive ? '🔕' : '🔇';
        silentText.textContent = isSilentModeActive ?
            'Désactiver Mode Discret' : 'Mode Discret';
    }
}

// Toggle Mode Mains Libres
function toggleHandsFreeMode() {
    closeVoiceMenu();

    if (!window.siriVoiceAssistant) {
        console.error('❌ Assistant vocal non disponible');
        return;
    }

    isHandsFreeModeActive = siriVoiceAssistant.toggleHandsFreeMode();

    // Mettre à jour le bouton principal
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        if (isHandsFreeModeActive) {
            voiceBtn.classList.add('hands-free');
            showNotification('🤚 Mode Mains Libres activé', 'success');
        } else {
            voiceBtn.classList.remove('hands-free');
            showNotification('Mode Mains Libres désactivé', 'info');
        }
    }
}

// Toggle Mode Discret
function toggleSilentMode() {
    closeVoiceMenu();

    if (!window.siriVoiceAssistant) {
        isSilentModeActive = !isSilentModeActive;
        showNotification(
            isSilentModeActive ? '🔕 Mode Discret activé' : 'Mode Discret désactivé',
            'info'
        );
        return;
    }

    siriVoiceAssistant.toggleSilentMode();
    isSilentModeActive = siriVoiceAssistant.silentMode;

    showNotification(
        isSilentModeActive ? '🔕 Mode Discret activé' : 'Mode Discret désactivé',
        'info'
    );
}

// Toggle Conversation Vocale
function toggleVoiceConversation() {
    if (!window.siriVoiceAssistant) {
        console.error('❌ Assistant vocal non disponible');
        return;
    }

    const voiceBtn = document.getElementById('voiceBtn');

    if (siriVoiceAssistant.isListening) {
        siriVoiceAssistant.stopListening();
        if (voiceBtn) {
            voiceBtn.classList.remove('listening');
        }
    } else {
        siriVoiceAssistant.startListening();
        if (voiceBtn) {
            voiceBtn.classList.add('listening');
        }
    }
}

// Mettre à jour l'UI du bouton vocal
function updateVoiceButton(state) {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!voiceBtn) return;

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
            // Garder la classe hands-free si active
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
    // Attendre que siriVoiceAssistant soit initialisé
    setTimeout(() => {
        if (window.siriVoiceAssistant) {
            console.log('✓ Interface vocale simplifiée activée');

            // Remplacer la fonction updateUI du système Siri
            const originalUpdateUI = siriVoiceAssistant.updateUI;
            siriVoiceAssistant.updateUI = function (state) {
                updateVoiceButton(state);
            };
        }
    }, 500);
});

// Fermer le menu en cliquant sur un item
document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.voice-menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            setTimeout(closeVoiceMenu, 100);
        });
    });
});
