/**
 * Système Vocal Simple - Basé sur le code fonctionnel de teach.html
 * UN CLIC = CONVERSATION AUTOMATIQUE
 */

let voiceRecognition = null;
let voiceSynthesis = window.speechSynthesis;
let isVoiceActive = false;
let isSpeaking = false;

// Initialiser la reconnaissance vocale
function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        voiceRecognition = new SpeechRecognition();
        voiceRecognition.lang = 'fr-FR';
        voiceRecognition.continuous = false;
        voiceRecognition.interimResults = false;

        voiceRecognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('📝 Texte reconnu:', transcript);
            document.getElementById('messageInput').value = transcript;

            // Envoyer automatiquement
            if (window.sendMessage) {
                window.sendMessage();
            }
        };

        voiceRecognition.onend = () => {
            console.log('🎤 Écoute terminée');
            if (isVoiceActive && !isSpeaking) {
                // Redémarrer l'écoute après un court délai
                setTimeout(() => {
                    if (isVoiceActive && !isSpeaking) {
                        startListening();
                    }
                }, 500);
            } else {
                updateVoiceButton('idle');
            }
        };

        voiceRecognition.onerror = (event) => {
            console.error('❌ Erreur reconnaissance:', event.error);
            if (event.error !== 'no-speech' && isVoiceActive && !isSpeaking) {
                // Réessayer après une erreur
                setTimeout(() => {
                    if (isVoiceActive && !isSpeaking) {
                        startListening();
                    }
                }, 1000);
            }
        };

        console.log('✅ Reconnaissance vocale initialisée');
    } else {
        console.error('❌ Reconnaissance vocale non supportée');
    }
}

// Démarrer l'écoute
function startListening() {
    if (!voiceRecognition) {
        initVoiceRecognition();
    }
    if (voiceRecognition && !isSpeaking) {
        try {
            voiceRecognition.start();
            updateVoiceButton('listening');
            console.log('🎤 Écoute démarrée');
        } catch (error) {
            console.error('❌ Erreur démarrage:', error);
        }
    }
}

// Arrêter l'écoute
function stopListening() {
    if (voiceRecognition) {
        try {
            voiceRecognition.stop();
            console.log('🛑 Écoute arrêtée');
        } catch (error) {
            console.error('❌ Erreur arrêt:', error);
        }
    }
    updateVoiceButton('idle');
}

// Synthèse vocale (lire le texte)
function speakText(text) {
    return new Promise((resolve) => {
        // Annuler toute synthèse en cours
        voiceSynthesis.cancel();

        // Nettoyer le texte (enlever markdown, emojis, etc.)
        const cleanText = text
            .replace(/\*\*(.+?)\*\*/g, '$1')  // Gras
            .replace(/\*(.+?)\*/g, '$1')      // Italique
            .replace(/\[(.+?)\]\(.+?\)/g, '$1') // Liens
            .replace(/`(.+?)`/g, '$1')        // Code inline
            .replace(/```[\s\S]*?```/g, '')   // Blocs de code
            .replace(/#{1,6}\s/g, '')         // Titres
            .replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emojis visages
            .replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // Emojis symboles
            .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Emojis transport
            .replace(/[\u{2600}-\u{26FF}]/gu, '')   // Emojis divers
            .replace(/\s+/g, ' ')             // Espaces multiples
            .trim();

        if (!cleanText) {
            resolve();
            return;
        }

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'fr-FR';
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        utterance.onstart = () => {
            isSpeaking = true;
            updateVoiceButton('speaking');
            console.log('🔊 Synthèse démarrée');
        };

        utterance.onend = () => {
            isSpeaking = false;
            console.log('🔊 Synthèse terminée');

            // Redémarrer l'écoute si le mode vocal est actif
            if (isVoiceActive) {
                setTimeout(() => {
                    if (isVoiceActive && !isSpeaking) {
                        startListening();
                    }
                }, 500);
            } else {
                updateVoiceButton('idle');
            }
            resolve();
        };

        utterance.onerror = (event) => {
            console.error('❌ Erreur synthèse vocale:', event.error);
            isSpeaking = false;
            resolve();
        };

        voiceSynthesis.speak(utterance);
    });
}

// Mettre à jour le bouton vocal
function updateVoiceButton(state) {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!voiceBtn) return;

    voiceBtn.classList.remove('listening', 'speaking', 'hands-free');

    switch (state) {
        case 'listening':
            voiceBtn.classList.add('listening', 'hands-free');
            break;
        case 'speaking':
            voiceBtn.classList.add('speaking', 'hands-free');
            break;
        case 'idle':
        default:
            if (isVoiceActive) {
                voiceBtn.classList.add('hands-free');
            }
            break;
    }
}

// Fonction principale - Démarrer/Arrêter la conversation vocale
function startVoiceConversation() {
    console.log('🎤 Clic sur le bouton vocal...');

    if (!voiceRecognition) {
        initVoiceRecognition();
    }

    if (!isVoiceActive) {
        // Activer le mode vocal
        isVoiceActive = true;
        startListening();
        console.log('✅ Mode vocal activé');

        // Afficher une notification
        if (window.showNotification) {
            showNotification('🎤 Mode vocal activé - Parlez maintenant !', 'success');
        }
    } else {
        // Désactiver le mode vocal
        isVoiceActive = false;
        stopListening();
        voiceSynthesis.cancel();
        isSpeaking = false;
        updateVoiceButton('idle');
        console.log('🛑 Mode vocal désactivé');

        // Afficher une notification
        if (window.showNotification) {
            showNotification('Mode vocal désactivé', 'info');
        }
    }
}

// Fonction de compatibilité
function toggleVoiceConversation() {
    startVoiceConversation();
}

// Intercepter la fonction sendMessage pour ajouter la synthèse vocale
window.addEventListener('load', () => {
    console.log('🎤 Initialisation système vocal simple...');
    initVoiceRecognition();

    // Attendre que sendMessage soit définie
    const checkSendMessage = setInterval(() => {
        if (window.sendMessage && typeof window.sendMessage === 'function') {
            console.log('✅ sendMessage trouvée, ajout de la synthèse vocale');
            clearInterval(checkSendMessage);

            // Sauvegarder la fonction originale
            const originalSendMessage = window.sendMessage;

            // Remplacer par une version qui ajoute la synthèse vocale
            window.sendMessage = async function () {
                // Appeler la fonction originale
                await originalSendMessage();

                // Attendre un peu que la réponse soit ajoutée au DOM
                setTimeout(() => {
                    // Trouver le dernier message du bot
                    const messages = document.querySelectorAll('.message');
                    if (messages.length > 0) {
                        const lastMessage = messages[messages.length - 1];
                        const isBot = lastMessage.querySelector('.avatar-bot');

                        if (isBot && isVoiceActive) {
                            const content = lastMessage.querySelector('.message-content');
                            if (content) {
                                const text = content.innerText || content.textContent;
                                console.log('🔊 Lecture de la réponse:', text.substring(0, 50) + '...');
                                speakText(text);
                            }
                        }
                    }
                }, 500);
            };

            console.log('✅ Synthèse vocale intégrée à sendMessage');
        }
    }, 100);

    // Arrêter après 10 secondes si sendMessage n'est pas trouvée
    setTimeout(() => {
        clearInterval(checkSendMessage);
    }, 10000);
});

// Rendre les fonctions globales
window.startVoiceConversation = startVoiceConversation;
window.toggleVoiceConversation = toggleVoiceConversation;
window.speakText = speakText;

console.log('✅ Système vocal simple chargé');
