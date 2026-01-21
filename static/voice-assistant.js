/**
 * Assistant Vocal - Reconnaissance et Synthèse Vocale
 * Utilise Web Speech API (natif dans les navigateurs modernes)
 */

class VoiceAssistant {
    constructor() {
        // Reconnaissance vocale (Speech-to-Text)
        this.recognition = null;
        this.isListening = false;

        // Synthèse vocale (Text-to-Speech)
        this.synthesis = window.speechSynthesis;
        this.isSpeaking = false;

        // Mode conversation continue
        this.continuousMode = false;

        // Langue
        this.language = 'fr-FR';

        // Initialiser
        this.init();
    }

    init() {
        // Vérifier la compatibilité du navigateur
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('❌ Reconnaissance vocale non supportée par ce navigateur');
            this.showError('Votre navigateur ne supporte pas la reconnaissance vocale. Utilisez Chrome, Edge ou Safari.');
            return;
        }

        // Initialiser la reconnaissance vocale
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();

        // Configuration
        this.recognition.lang = this.language;
        this.recognition.continuous = false; // Une phrase à la fois
        this.recognition.interimResults = true; // Résultats intermédiaires
        this.recognition.maxAlternatives = 1;

        // Événements
        this.setupRecognitionEvents();

        console.log('✓ Assistant vocal initialisé');
    }

    setupRecognitionEvents() {
        // Début de l'écoute
        this.recognition.onstart = () => {
            console.log('🎤 Écoute en cours...');
            this.isListening = true;
            this.updateUI('listening');
        };

        // Résultat (texte reconnu)
        this.recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0])
                .map(result => result.transcript)
                .join('');

            const isFinal = event.results[0].isFinal;

            if (isFinal) {
                console.log('📝 Texte reconnu:', transcript);
                this.handleTranscript(transcript);
            } else {
                // Afficher le texte intermédiaire
                this.showInterimTranscript(transcript);
            }
        };

        // Fin de l'écoute
        this.recognition.onend = () => {
            console.log('🎤 Écoute terminée');
            this.isListening = false;
            this.updateUI('idle');

            // Redémarrer en mode continu
            if (this.continuousMode && !this.isSpeaking) {
                setTimeout(() => this.startListening(), 500);
            }
        };

        // Erreur
        this.recognition.onerror = (event) => {
            console.error('❌ Erreur reconnaissance vocale:', event.error);
            this.isListening = false;
            this.updateUI('error');

            if (event.error === 'no-speech') {
                this.showError('Aucune parole détectée. Réessayez.');
            } else if (event.error === 'not-allowed') {
                this.showError('Microphone non autorisé. Activez-le dans les paramètres du navigateur.');
            } else {
                this.showError(`Erreur: ${event.error}`);
            }
        };
    }

    // Démarrer l'écoute
    startListening() {
        if (this.isListening) {
            console.log('⚠️ Déjà en écoute');
            return;
        }

        if (this.isSpeaking) {
            console.log('⚠️ L\'IA parle, attente...');
            this.synthesis.cancel(); // Arrêter la synthèse
            this.isSpeaking = false;
        }

        try {
            this.recognition.start();
            console.log('🎤 Démarrage de l\'écoute...');
        } catch (error) {
            console.error('❌ Erreur démarrage:', error);
        }
    }

    // Arrêter l'écoute
    stopListening() {
        if (!this.isListening) {
            return;
        }

        try {
            this.recognition.stop();
            console.log('🛑 Arrêt de l\'écoute');
        } catch (error) {
            console.error('❌ Erreur arrêt:', error);
        }
    }

    // Gérer le texte reconnu
    handleTranscript(transcript) {
        // Nettoyer le texte
        const text = transcript.trim();

        if (!text) {
            return;
        }

        // Afficher dans l'input
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.value = text;
            messageInput.style.color = '#f3f4f6'; // Couleur normale
        }

        // Envoyer automatiquement
        this.sendMessage(text);
    }

    // Envoyer le message à l'IA
    sendMessage(text) {
        // Simuler un clic sur le bouton d'envoi
        const sendButton = document.querySelector('.btn-send');
        if (sendButton) {
            sendButton.click();
        }
    }

    // Synthèse vocale (Text-to-Speech)
    speak(text) {
        if (!text) {
            return;
        }

        // Arrêter toute synthèse en cours
        this.synthesis.cancel();

        // Nettoyer le texte (enlever le markdown)
        const cleanText = this.cleanTextForSpeech(text);

        // Créer l'utterance
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = this.language;
        utterance.rate = 1.0; // Vitesse normale
        utterance.pitch = 1.0; // Ton normal
        utterance.volume = 1.0; // Volume max

        // Événements
        utterance.onstart = () => {
            console.log('🔊 Synthèse vocale démarrée');
            this.isSpeaking = true;
            this.updateUI('speaking');
        };

        utterance.onend = () => {
            console.log('🔊 Synthèse vocale terminée');
            this.isSpeaking = false;
            this.updateUI('idle');

            // Redémarrer l'écoute en mode continu
            if (this.continuousMode) {
                setTimeout(() => this.startListening(), 500);
            }
        };

        utterance.onerror = (event) => {
            console.error('❌ Erreur synthèse vocale:', event.error);
            this.isSpeaking = false;
            this.updateUI('error');
        };

        // Lancer la synthèse
        this.synthesis.speak(utterance);
    }

    // Arrêter la synthèse vocale
    stopSpeaking() {
        this.synthesis.cancel();
        this.isSpeaking = false;
        this.updateUI('idle');
    }

    // Nettoyer le texte pour la synthèse vocale
    cleanTextForSpeech(text) {
        return text
            // Enlever le markdown
            .replace(/\*\*(.+?)\*\*/g, '$1') // Gras
            .replace(/\*(.+?)\*/g, '$1') // Italique
            .replace(/\[(.+?)\]\(.+?\)/g, '$1') // Liens
            .replace(/`(.+?)`/g, '$1') // Code inline
            .replace(/```[\s\S]*?```/g, '') // Blocs de code
            .replace(/#{1,6}\s/g, '') // Titres
            .replace(/>\s/g, '') // Citations
            .replace(/[-*+]\s/g, '') // Listes
            .replace(/\d+\.\s/g, '') // Listes numérotées
            // Enlever les emojis (optionnel)
            .replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emoticons
            .replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // Symboles
            .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Transport
            .replace(/[\u{2600}-\u{26FF}]/gu, '') // Divers
            // Nettoyer les espaces
            .replace(/\s+/g, ' ')
            .trim();
    }

    // Activer/Désactiver le mode conversation continue
    toggleContinuousMode() {
        this.continuousMode = !this.continuousMode;
        console.log(`💬 Mode conversation continue: ${this.continuousMode ? 'ON' : 'OFF'}`);

        if (this.continuousMode) {
            this.startListening();
        } else {
            this.stopListening();
        }

        return this.continuousMode;
    }

    // Mettre à jour l'interface utilisateur
    updateUI(state) {
        const voiceBtn = document.getElementById('voice-btn');
        const voiceStatus = document.getElementById('voice-status');

        if (!voiceBtn) return;

        switch (state) {
            case 'listening':
                voiceBtn.innerHTML = '🎤 Écoute...';
                voiceBtn.style.background = 'rgba(239, 68, 68, 0.2)';
                voiceBtn.style.borderColor = '#ef4444';
                voiceBtn.style.color = '#ef4444';
                if (voiceStatus) voiceStatus.textContent = '🎤 Parlez maintenant...';
                break;

            case 'speaking':
                voiceBtn.innerHTML = '🔊 Parle...';
                voiceBtn.style.background = 'rgba(59, 130, 246, 0.2)';
                voiceBtn.style.borderColor = '#3b82f6';
                voiceBtn.style.color = '#3b82f6';
                if (voiceStatus) voiceStatus.textContent = '🔊 L\'IA parle...';
                break;

            case 'idle':
                voiceBtn.innerHTML = '🎤 Vocal';
                voiceBtn.style.background = 'rgba(59, 130, 246, 0.1)';
                voiceBtn.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                voiceBtn.style.color = '#3b82f6';
                if (voiceStatus) voiceStatus.textContent = '';
                break;

            case 'error':
                voiceBtn.innerHTML = '❌ Erreur';
                voiceBtn.style.background = 'rgba(239, 68, 68, 0.1)';
                voiceBtn.style.borderColor = 'rgba(239, 68, 68, 0.3)';
                voiceBtn.style.color = '#ef4444';
                if (voiceStatus) voiceStatus.textContent = '';
                setTimeout(() => this.updateUI('idle'), 2000);
                break;
        }
    }

    // Afficher le texte intermédiaire
    showInterimTranscript(text) {
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.value = text;
            messageInput.style.color = '#9ca3af'; // Gris pour indiquer que c'est temporaire
        }
    }

    // Afficher une erreur
    showError(message) {
        const voiceStatus = document.getElementById('voice-status');
        if (voiceStatus) {
            voiceStatus.textContent = `❌ ${message}`;
            voiceStatus.style.color = '#ef4444';
            setTimeout(() => {
                voiceStatus.textContent = '';
                voiceStatus.style.color = '';
            }, 3000);
        } else {
            alert(message);
        }
    }

    // Changer la langue
    setLanguage(lang) {
        this.language = lang;
        if (this.recognition) {
            this.recognition.lang = lang;
        }
        console.log(`🌍 Langue changée: ${lang}`);
    }
}

// Instance globale
let voiceAssistant = null;

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    voiceAssistant = new VoiceAssistant();
    console.log('✓ Assistant vocal prêt');
});

// Fonction pour lire la réponse de l'IA
function speakAIResponse(text) {
    if (voiceAssistant) {
        voiceAssistant.speak(text);
    }
}

// Fonction pour démarrer/arrêter l'écoute
function toggleVoiceListening() {
    if (!voiceAssistant) {
        console.error('❌ Assistant vocal non initialisé');
        return;
    }

    if (voiceAssistant.isListening) {
        voiceAssistant.stopListening();
    } else {
        voiceAssistant.startListening();
    }
}

// Fonction pour activer/désactiver le mode conversation continue
function toggleContinuousMode() {
    if (!voiceAssistant) {
        console.error('❌ Assistant vocal non initialisé');
        return;
    }

    const isActive = voiceAssistant.toggleContinuousMode();

    // Mettre à jour le bouton
    const continuousBtn = document.getElementById('continuous-btn');
    if (continuousBtn) {
        if (isActive) {
            continuousBtn.innerHTML = '💬 Mode Continu ON';
            continuousBtn.style.background = 'rgba(34, 197, 94, 0.2)';
            continuousBtn.style.borderColor = '#22c55e';
            continuousBtn.style.color = '#22c55e';
        } else {
            continuousBtn.innerHTML = '💬 Mode Continu';
            continuousBtn.style.background = 'rgba(59, 130, 246, 0.1)';
            continuousBtn.style.borderColor = 'rgba(59, 130, 246, 0.3)';
            continuousBtn.style.color = '#3b82f6';
        }
    }
}
