/**
 * Intégration du système vocal Siri avec le chat
 * Ce fichier fait le pont entre voice-assistant-siri.js et chat.html
 */

// Variables globales pour la compatibilité
let isVoiceActive = false;
let isSilentMode = false;

// Fonction appelée quand l'assistant Siri est prêt
document.addEventListener('DOMContentLoaded', () => {
    // Attendre que siriVoiceAssistant soit initialisé
    setTimeout(() => {
        if (window.siriVoiceAssistant) {
            console.log('✓ Intégration système vocal Siri activée');
            setupVoiceIntegration();
        }
    }, 500);
});

function setupVoiceIntegration() {
    // Intercepter l'envoi de message pour la synthèse vocale
    const originalSendMessage = window.sendMessage;

    window.sendMessage = async function () {
        await originalSendMessage();

        // Après l'envoi, attendre la réponse et la lire
        // La lecture sera gérée dans la fonction qui reçoit la réponse
    };
}

// Fonction pour lire la réponse de l'IA (appelée depuis chat.html)
function speakAIResponse(text) {
    if (window.siriVoiceAssistant && !isSilentMode) {
        siriVoiceAssistant.speak(text);
    }
}

// Toggle conversation vocale (compatible avec l'ancien système)
function toggleVoiceConversation() {
    if (!window.siriVoiceAssistant) {
        console.error('❌ Assistant vocal Siri non disponible');
        return;
    }

    if (siriVoiceAssistant.isListening) {
        siriVoiceAssistant.stopListening();
        isVoiceActive = false;
    } else {
        siriVoiceAssistant.startListening();
        isVoiceActive = true;
    }
}

// Toggle mode mains libres
function toggleHandsFreeMode() {
    if (!window.siriVoiceAssistant) {
        console.error('❌ Assistant vocal Siri non disponible');
        return;
    }

    const isActive = siriVoiceAssistant.toggleHandsFreeMode();

    // Mettre à jour le bouton
    const handsFreeBtn = document.getElementById('handsfree-btn');
    if (handsFreeBtn) {
        if (isActive) {
            handsFreeBtn.innerHTML = '🤚 Mains Libres ON';
            handsFreeBtn.style.background = 'rgba(34, 197, 94, 0.2)';
            handsFreeBtn.style.borderColor = '#22c55e';
            handsFreeBtn.style.color = '#22c55e';
        } else {
            handsFreeBtn.innerHTML = '🤚 Mains Libres';
            handsFreeBtn.style.background = 'rgba(59, 130, 246, 0.1)';
            handsFreeBtn.style.borderColor = 'rgba(59, 130, 246, 0.3)';
            handsFreeBtn.style.color = '#3b82f6';
        }
    }
}

// Toggle mode discret
function toggleSilentMode() {
    if (!window.siriVoiceAssistant) {
        isSilentMode = !isSilentMode;
        updateSilentButton();
        return;
    }

    siriVoiceAssistant.toggleSilentMode();
    isSilentMode = siriVoiceAssistant.silentMode;
    updateSilentButton();
}

function updateSilentButton() {
    const silentBtn = document.getElementById('silentBtn');
    if (silentBtn) {
        if (isSilentMode) {
            silentBtn.classList.add('active');
            silentBtn.textContent = '🔕';
            silentBtn.title = 'Mode discret activé';
        } else {
            silentBtn.classList.remove('active');
            silentBtn.textContent = '🔇';
            silentBtn.title = 'Mode discret';
        }
    }
}

// Toggle paramètres vocaux
function toggleVoiceSettings() {
    const menu = document.getElementById('voiceSettingsMenu');
    if (menu) {
        menu.classList.toggle('active');
    }
}

// Charger les voix disponibles
function loadAvailableVoices() {
    const voiceSelect = document.getElementById('voiceSelect');
    if (!voiceSelect) return;

    const synthesis = window.speechSynthesis;

    function populateVoices() {
        const voices = synthesis.getVoices();
        const frenchVoices = voices.filter(voice => voice.lang.startsWith('fr'));

        voiceSelect.innerHTML = '<option value="">Voix par défaut</option>';

        const voicesToShow = frenchVoices.length > 0 ? frenchVoices : voices;

        voicesToShow.forEach((voice, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${voice.name} (${voice.lang})`;
            voiceSelect.appendChild(option);
        });
    }

    populateVoices();
    if (synthesis.onvoiceschanged !== undefined) {
        synthesis.onvoiceschanged = populateVoices;
    }
}

// Changer la voix
function changeVoice() {
    if (!window.siriVoiceAssistant) return;

    const voiceSelect = document.getElementById('voiceSelect');
    const voices = window.speechSynthesis.getVoices();
    const selectedIndex = voiceSelect.value;

    if (selectedIndex === '') {
        siriVoiceAssistant.voiceSettings.voice = null;
    } else {
        siriVoiceAssistant.voiceSettings.voice = voices[selectedIndex];
    }

    console.log('🎙️ Voix changée:', siriVoiceAssistant.voiceSettings.voice ? siriVoiceAssistant.voiceSettings.voice.name : 'Défaut');
    siriVoiceAssistant.playSound('start');
}

// Changer la vitesse
function changeRate(value) {
    if (!window.siriVoiceAssistant) return;

    siriVoiceAssistant.voiceSettings.rate = parseFloat(value);
    document.getElementById('rateValue').textContent = value + 'x';
    console.log('⏩ Vitesse:', value);
}

// Changer la tonalité
function changePitch(value) {
    if (!window.siriVoiceAssistant) return;

    siriVoiceAssistant.voiceSettings.pitch = parseFloat(value);
    document.getElementById('pitchValue').textContent = value;
    console.log('🎵 Tonalité:', value);
}

// Changer le volume
function changeVolume(value) {
    if (!window.siriVoiceAssistant) return;

    siriVoiceAssistant.voiceSettings.volume = parseFloat(value);
    const percentage = Math.round(value * 100);
    document.getElementById('volumeValue').textContent = percentage + '%';
    console.log('🔊 Volume:', percentage + '%');
}

// Fermer le menu en cliquant en dehors
document.addEventListener('click', function (event) {
    const menu = document.getElementById('voiceSettingsMenu');
    const btn = document.getElementById('voiceSettingsBtn');

    if (menu && btn && !menu.contains(event.target) && !btn.contains(event.target)) {
        menu.classList.remove('active');
    }
});

// Initialiser au chargement
window.addEventListener('load', () => {
    loadAvailableVoices();
});
