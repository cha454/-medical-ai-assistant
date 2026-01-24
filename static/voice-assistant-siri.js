/**
 * Assistant Vocal Style Siri - Version Améliorée
 * Fonctionnalités:
 * - Activation par mot-clé ("Hey Assistant")
 * - Feedback sonore (sons de début/fin)
 * - Visualisation audio (animation)
 * - Commandes vocales (Stop, Répète, etc.)
 * - Mode mains libres (conversation continue)
 * - Paramètres vocaux (voix, vitesse, tonalité)
 */

class SiriVoiceAssistant {
    constructor() {
        // Reconnaissance vocale
        this.recognition = null;
        this.isListening = false;
        this.isWaitingForWakeWord = false;

        // Synthèse vocale
        this.synthesis = window.speechSynthesis;
        this.isSpeaking = false;
        this.currentUtterance = null;

        // Mode conversation
        this.continuousMode = false;
        this.handsFreeModeActive = false;

        // Paramètres vocaux
        this.voiceSettings = {
            rate: 1.0,      // Vitesse (0.5 - 2.0)
            pitch: 1.0,     // Tonalité (0.5 - 2.0)
            volume: 1.0,    // Volume (0 - 1.0)
            voice: null     // Voix sélectionnée
        };

        // Feedback sonore
        this.soundEnabled = true;
        this.sounds = {
            start: this.createSound(800, 0.1, 'sine'),      // Ding
            end: this.createSound(600, 0.1, 'sine'),        // Dong
            error: this.createSound(400, 0.2, 'sawtooth'),  // Erreur
            success: this.createSound(1000, 0.15, 'sine')   // Succès
        };

        // Visualisation audio
        this.audioContext = null;
        this.analyser = null;
        this.visualizationActive = false;

        // Commandes vocales
        this.voiceCommands = {
            'stop': () => {
                console.log('🛑 Commande STOP détectée');
                this.stopSpeaking();
                if (this.handsFreeModeActive) {
                    this.toggleHandsFreeMode();
                }
            },
            'arrête': () => {
                console.log('🛑 Commande ARRÊTE détectée');
                this.stopSpeaking();
                if (this.handsFreeModeActive) {
                    this.toggleHandsFreeMode();
                }
            },
            'répète': () => this.repeatLastResponse(),
            'plus fort': () => this.adjustVolume(0.1),
            'moins fort': () => this.adjustVolume(-0.1),
            'plus vite': () => this.adjustSpeed(0.2),
            'moins vite': () => this.adjustSpeed(-0.2),
            'mode discret': () => this.toggleSilentMode(),
            'nouveau': () => this.newConversation()
        };

        // Historique
        this.lastResponse = '';
        this.conversationHistory = [];

        // Langue
        this.language = 'fr-FR';

        // Mode discret (pas de synthèse vocale)
        this.silentMode = false;

        // Initialiser
        this.init();
    }

    init() {
        // Vérifier la compatibilité
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.error('❌ Reconnaissance vocale non supportée');
            this.showNotification('Votre navigateur ne supporte pas la reconnaissance vocale', 'error');
            return;
        }

        // Initialiser la reconnaissance
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();

        // Configuration
        this.recognition.lang = this.language;
        this.recognition.continuous = true;  // Écoute continue
        this.recognition.interimResults = true;
        this.recognition.maxAlternatives = 1;

        // Événements
        this.setupRecognitionEvents();

        // Charger les voix disponibles
        this.loadVoices();

        // Initialiser l'audio context pour la visualisation
        this.initAudioContext();

        console.log('✓ Assistant vocal Siri initialisé');
    }

    setupRecognitionEvents() {
        this.recognition.onstart = () => {
            console.log('🎤 Écoute démarrée');
            this.isListening = true;
            this.playSound('start');
            this.updateUI('listening');
            this.startVisualization();
        };

        this.recognition.onresult = (event) => {
            const results = Array.from(event.results);
            const lastResult = results[results.length - 1];
            const transcript = lastResult[0].transcript.trim().toLowerCase();
            const isFinal = lastResult.isFinal;

            // Afficher le texte intermédiaire
            if (!isFinal) {
                this.showInterimTranscript(transcript);
                return;
            }

            console.log('📝 Texte reconnu:', transcript);

            // Vérifier les commandes vocales
            if (this.handleVoiceCommand(transcript)) {
                return;
            }

            // Mode activation par mot-clé
            if (this.isWaitingForWakeWord) {
                if (transcript.includes('hey assistant') || transcript.includes('ok assistant')) {
                    this.isWaitingForWakeWord = false;
                    this.playSound('success');
                    this.showNotification('Je vous écoute...', 'success');
                }
                return;
            }

            // Traiter le message
            this.handleTranscript(transcript);
        };

        this.recognition.onend = () => {
            console.log('🎤 Écoute terminée');
            this.isListening = false;
            this.stopVisualization();

            // Redémarrer en mode continu (mais PAS en mode mains libres)
            if (this.continuousMode && !this.isSpeaking && !this.handsFreeModeActive) {
                setTimeout(() => this.startListening(), 300);
            }

            // En mode mains libres, l'écoute redémarre APRÈS la synthèse vocale
            // (voir utterance.onend dans la fonction speak())

            this.updateUI('idle');
        };

        this.recognition.onerror = (event) => {
            console.error('❌ Erreur:', event.error);
            this.isListening = false;
            this.stopVisualization();

            if (event.error === 'no-speech') {
                // Pas d'erreur affichée, c'est normal
            } else if (event.error === 'not-allowed') {
                this.showNotification('Microphone non autorisé', 'error');
                this.playSound('error');
            } else {
                this.playSound('error');
            }

            this.updateUI('idle');
        };
    }

    // Démarrer l'écoute
    startListening() {
        if (this.isListening) return;

        if (this.isSpeaking) {
            this.stopSpeaking();
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('❌ Erreur démarrage:', error);
        }
    }

    // Arrêter l'écoute
    stopListening() {
        if (!this.isListening) return;

        try {
            this.recognition.stop();
            this.playSound('end');
        } catch (error) {
            console.error('❌ Erreur arrêt:', error);
        }
    }

    // Gérer le texte reconnu
    handleTranscript(transcript) {
        const text = transcript.trim();
        console.log('🎯 handleTranscript appelé avec:', text);

        if (!text) {
            console.warn('⚠️ Texte vide, abandon');
            return;
        }

        // Vérifier les commandes vocales AVANT d'envoyer le message
        if (this.handleVoiceCommand(text)) {
            console.log('✅ Commande vocale traitée, pas d\'envoi de message');
            return;
        }

        console.log('📤 Préparation envoi du message:', text);

        // Afficher dans l'input
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.value = text;
            console.log('✅ Texte mis dans l\'input');
        } else {
            console.error('❌ Input messageInput non trouvé');
        }

        // Envoyer le message directement
        console.log('🚀 Tentative d\'envoi...');
        this.sendMessage(text);

        // Ajouter à l'historique
        this.conversationHistory.push({
            type: 'user',
            text: text,
            timestamp: new Date()
        });
        console.log('✅ Message ajouté à l\'historique');
    }

    // Envoyer le message
    sendMessage(text) {
        console.log('📨 sendMessage appelé pour:', text);

        // Appeler directement window.sendMessage (elle est maintenant chargée avant ce script)
        if (typeof window.sendMessage === 'function') {
            console.log('✅ Appel de window.sendMessage()');
            window.sendMessage();
        } else {
            console.error('❌ window.sendMessage non disponible (chat-functions.js pas chargé)');
        }
    }

    // Synthèse vocale (Text-to-Speech)
    speak(text, options = {}) {
        if (!text || this.silentMode) return;

        // IMPORTANT: Arrêter l'écoute pour éviter de reconnaître sa propre voix
        if (this.isListening) {
            console.log('🛑 Arrêt de l\'écoute avant la synthèse');
            this.stopListening();
        }

        // Arrêter toute synthèse en cours
        this.synthesis.cancel();

        // Nettoyer le texte
        const cleanText = this.cleanTextForSpeech(text);

        // Créer l'utterance
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = this.language;
        utterance.rate = options.rate || this.voiceSettings.rate;
        utterance.pitch = options.pitch || this.voiceSettings.pitch;
        utterance.volume = options.volume || this.voiceSettings.volume;

        // Sélectionner la voix
        if (this.voiceSettings.voice) {
            utterance.voice = this.voiceSettings.voice;
        }

        // Événements
        utterance.onstart = () => {
            console.log('🔊 Synthèse démarrée');
            this.isSpeaking = true;
            this.currentUtterance = utterance;
            this.updateUI('speaking');
            this.startSpeakingVisualization();
        };

        utterance.onend = () => {
            console.log('🔊 Synthèse terminée');
            this.isSpeaking = false;
            this.currentUtterance = null;
            this.stopSpeakingVisualization();
            this.updateUI('idle');

            // Redémarrer l'écoute en mode mains libres (avec délai plus long)
            if (this.handsFreeModeActive) {
                setTimeout(() => {
                    if (this.handsFreeModeActive && !this.isSpeaking) {
                        this.startListening();
                    }
                }, 1000); // 1 seconde de délai
            }
        };

        utterance.onerror = (event) => {
            console.error('❌ Erreur synthèse:', event.error);
            this.isSpeaking = false;
            this.currentUtterance = null;
            this.stopSpeakingVisualization();
            this.updateUI('idle');
        };

        // Sauvegarder la dernière réponse
        this.lastResponse = text;
        this.conversationHistory.push({
            type: 'assistant',
            text: text,
            timestamp: new Date()
        });

        // Lancer la synthèse
        this.synthesis.speak(utterance);
    }

    // Arrêter la synthèse
    stopSpeaking() {
        this.synthesis.cancel();
        this.isSpeaking = false;
        this.currentUtterance = null;
        this.stopSpeakingVisualization();
        this.updateUI('idle');
        this.showNotification('Synthèse arrêtée', 'info');
    }

    // Répéter la dernière réponse
    repeatLastResponse() {
        if (this.lastResponse) {
            this.speak(this.lastResponse);
            this.showNotification('Répétition...', 'info');
        }
    }

    // Gérer les commandes vocales
    handleVoiceCommand(transcript) {
        for (const [command, action] of Object.entries(this.voiceCommands)) {
            if (transcript.includes(command)) {
                console.log(`🎯 Commande détectée: ${command}`);
                action();
                return true;
            }
        }
        return false;
    }

    // Ajuster le volume
    adjustVolume(delta) {
        this.voiceSettings.volume = Math.max(0, Math.min(1, this.voiceSettings.volume + delta));
        this.showNotification(`Volume: ${Math.round(this.voiceSettings.volume * 100)}%`, 'info');
    }

    // Ajuster la vitesse
    adjustSpeed(delta) {
        this.voiceSettings.rate = Math.max(0.5, Math.min(2.0, this.voiceSettings.rate + delta));
        this.showNotification(`Vitesse: ${this.voiceSettings.rate.toFixed(1)}x`, 'info');
    }

    // Mode discret (pas de synthèse vocale)
    toggleSilentMode() {
        this.silentMode = !this.silentMode;
        this.showNotification(
            this.silentMode ? 'Mode discret activé' : 'Mode discret désactivé',
            'info'
        );

        if (this.silentMode) {
            this.stopSpeaking();
        }
    }

    // Nouvelle conversation
    newConversation() {
        this.conversationHistory = [];
        this.lastResponse = '';
        this.showNotification('Nouvelle conversation', 'info');
    }

    // Mode mains libres
    toggleHandsFreeMode() {
        this.handsFreeModeActive = !this.handsFreeModeActive;

        if (this.handsFreeModeActive) {
            this.startListening();
            this.showNotification('Mode mains libres activé', 'success');
        } else {
            this.stopListening();
            this.showNotification('Mode mains libres désactivé', 'info');
        }

        return this.handsFreeModeActive;
    }

    // Nettoyer le texte pour la synthèse
    cleanTextForSpeech(text) {
        return text
            .replace(/\*\*(.+?)\*\*/g, '$1')
            .replace(/\*(.+?)\*/g, '$1')
            .replace(/\[(.+?)\]\(.+?\)/g, '$1')
            .replace(/`(.+?)`/g, '$1')
            .replace(/```[\s\S]*?```/g, '')
            .replace(/#{1,6}\s/g, '')
            .replace(/>\s/g, '')
            .replace(/[-*+]\s/g, '')
            .replace(/\d+\.\s/g, '')
            .replace(/[\u{1F600}-\u{1F64F}]/gu, '')
            .replace(/[\u{1F300}-\u{1F5FF}]/gu, '')
            .replace(/[\u{1F680}-\u{1F6FF}]/gu, '')
            .replace(/[\u{2600}-\u{26FF}]/gu, '')
            .replace(/\s+/g, ' ')
            .trim();
    }

    // Créer un son
    createSound(frequency, duration, type = 'sine') {
        return () => {
            if (!this.soundEnabled) return;

            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = type;

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        };
    }

    // Jouer un son
    playSound(soundName) {
        if (this.sounds[soundName]) {
            this.sounds[soundName]();
        }
    }

    // Initialiser l'audio context pour la visualisation
    initAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
        } catch (error) {
            console.error('❌ Erreur audio context:', error);
        }
    }

    // Démarrer la visualisation audio
    startVisualization() {
        this.visualizationActive = true;
        const visualizer = document.getElementById('audio-visualizer');
        if (visualizer) {
            visualizer.style.display = 'flex';
            this.animateVisualizer();
        }
    }

    // Arrêter la visualisation
    stopVisualization() {
        this.visualizationActive = false;
        const visualizer = document.getElementById('audio-visualizer');
        if (visualizer) {
            visualizer.style.display = 'none';
        }
    }

    // Animer le visualiseur
    animateVisualizer() {
        if (!this.visualizationActive) return;

        const bars = document.querySelectorAll('.visualizer-bar');
        bars.forEach((bar, index) => {
            const height = Math.random() * 100;
            bar.style.height = `${height}%`;
            bar.style.animationDelay = `${index * 0.1}s`;
        });

        requestAnimationFrame(() => this.animateVisualizer());
    }

    // Visualisation pendant la synthèse
    startSpeakingVisualization() {
        const visualizer = document.getElementById('audio-visualizer');
        if (visualizer) {
            visualizer.style.display = 'flex';
            visualizer.classList.add('speaking');
        }
    }

    stopSpeakingVisualization() {
        const visualizer = document.getElementById('audio-visualizer');
        if (visualizer) {
            visualizer.classList.remove('speaking');
            setTimeout(() => {
                if (!this.isListening) {
                    visualizer.style.display = 'none';
                }
            }, 300);
        }
    }

    // Charger les voix disponibles
    loadVoices() {
        const voices = this.synthesis.getVoices();
        if (voices.length > 0) {
            // Sélectionner une voix française par défaut
            const frenchVoice = voices.find(voice => voice.lang.startsWith('fr'));
            if (frenchVoice) {
                this.voiceSettings.voice = frenchVoice;
            }
        }

        // Recharger si les voix ne sont pas encore disponibles
        if (voices.length === 0) {
            this.synthesis.onvoiceschanged = () => {
                this.loadVoices();
            };
        }
    }

    // Afficher le texte intermédiaire
    showInterimTranscript(text) {
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.value = text;
            messageInput.style.color = '#9ca3af';
        }
    }

    // Afficher une notification
    showNotification(message, type = 'info') {
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

    // Mettre à jour l'interface
    updateUI(state) {
        const voiceBtn = document.getElementById('voice-btn');
        if (!voiceBtn) return;

        switch (state) {
            case 'listening':
                voiceBtn.innerHTML = '🎤 Écoute...';
                voiceBtn.style.background = 'rgba(239, 68, 68, 0.2)';
                voiceBtn.style.borderColor = '#ef4444';
                voiceBtn.style.color = '#ef4444';
                voiceBtn.classList.add('pulse');
                break;

            case 'speaking':
                voiceBtn.innerHTML = '🔊 Parle...';
                voiceBtn.style.background = 'rgba(59, 130, 246, 0.2)';
                voiceBtn.style.borderColor = '#3b82f6';
                voiceBtn.style.color = '#3b82f6';
                voiceBtn.classList.add('pulse');
                break;

            case 'idle':
                voiceBtn.innerHTML = '🎤 Vocal';
                voiceBtn.style.background = 'rgba(59, 130, 246, 0.1)';
                voiceBtn.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                voiceBtn.style.color = '#3b82f6';
                voiceBtn.classList.remove('pulse');
                break;
        }
    }
}

// Instance globale
let siriVoiceAssistant = null;

// Fonction d'initialisation robuste
function initSiriVoiceAssistant() {
    if (siriVoiceAssistant) {
        console.log('✓ Assistant vocal déjà initialisé');
        return;
    }

    try {
        siriVoiceAssistant = new SiriVoiceAssistant();
        window.siriVoiceAssistant = siriVoiceAssistant; // Rendre global
        console.log('✓ Assistant vocal Siri prêt');
    } catch (error) {
        console.error('❌ Erreur initialisation:', error);
    }
}

// Initialiser immédiatement si le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSiriVoiceAssistant);
} else {
    // DOM déjà chargé
    initSiriVoiceAssistant();
}

// Backup: initialiser après 500ms si pas encore fait
setTimeout(() => {
    if (!siriVoiceAssistant) {
        console.log('⚠️ Initialisation de secours...');
        initSiriVoiceAssistant();
    }
}, 500);

// Fonctions globales
function toggleVoiceListening() {
    if (!siriVoiceAssistant) return;

    if (siriVoiceAssistant.isListening) {
        siriVoiceAssistant.stopListening();
    } else {
        siriVoiceAssistant.startListening();
    }
}

function toggleHandsFreeMode() {
    if (!siriVoiceAssistant) return;

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

function speakAIResponse(text) {
    if (siriVoiceAssistant) {
        siriVoiceAssistant.speak(text);
    }
}

function toggleSilentMode() {
    if (siriVoiceAssistant) {
        siriVoiceAssistant.toggleSilentMode();
    }
}
