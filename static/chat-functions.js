/**
 * Fonctions de chat (sans système vocal)
 * Le système vocal est géré par voice-assistant-siri.js et voice-integration.js
 */

console.log('🔵 chat-functions.js chargé');

// Configuration de Marked.js pour autoriser le HTML (nécessaire pour la grille d'actualités)
marked.setOptions({
    headerIds: false,
    mangle: false,
    sanitize: false, // Permet le HTML dans le Markdown
    breaks: true    // Supporte les retours à la ligne
});

const API_URL = window.location.origin;
let conversationHistory = [];

// Variables pour compatibilité avec le système vocal
let isVoiceActive = false;

// ============================================
// FONCTIONS DE CHAT
// ============================================

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendSuggestion(text) {
    document.getElementById('messageInput').value = text;
    sendMessage();
}

function hideEmptyState() {
    const emptyState = document.getElementById('emptyState');
    if (emptyState) {
        emptyState.style.display = 'none';
    }
}

function addMessage(content, isUser) {
    hideEmptyState();

    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    const avatar = isUser ? '👤' : '🤖';
    const author = isUser ? 'Vous' : 'Assistant';
    const avatarClass = isUser ? 'avatar-user' : 'avatar-bot';

    // Convertir Markdown en HTML pour les messages du bot
    let formattedContent;
    if (isUser) {
        // Pour l'utilisateur, juste remplacer les retours à la ligne
        formattedContent = content.replace(/\n/g, '<br>');
    } else {
        // Pour le bot, convertir le Markdown en HTML
        console.log('🤖 Réponse du bot (brute):', content.substring(0, 100) + '...');
        
        // Si le contenu commence par une balise HTML (comme la carte météo), 
        // on évite de le passer dans marked.parse qui pourrait ajouter des backticks
        if (content.trim().startsWith('<div')) {
            formattedContent = content;
        } else {
            formattedContent = marked.parse(content);
        }
        
        console.log('🤖 Réponse du bot (formatée):', formattedContent.substring(0, 100) + '...');
    }

    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="avatar ${avatarClass}">${avatar}</div>
            <div class="message-author">${author}</div>
        </div>
        <div class="message-content">${formattedContent}</div>
        ${!isUser ? `
            <div class="message-actions">
                <button class="action-btn" onclick="copyMessage(this)">📋 Copier</button>
                <button class="action-btn" onclick="regenerateResponse()">🔄 Régénérer</button>
            </div>
        ` : ''}
    `;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTyping() {
    hideEmptyState();
    const messagesDiv = document.getElementById('messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing';
    typingDiv.className = 'message';
    typingDiv.innerHTML = `
        <div class="message-header">
            <div class="avatar avatar-bot">🤖</div>
            <div class="message-author">Assistant</div>
        </div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function hideTyping() {
    const typing = document.getElementById('typing');
    if (typing) typing.remove();
}

async function sendMessage() {
    console.log('📬 sendMessage() appelée');

    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    console.log('📝 Message à envoyer:', message);

    if (!message) {
        console.warn('⚠️ Message vide, abandon');
        return;
    }

    console.log('✅ Message valide, envoi en cours...');

    // Add user message
    addMessage(message, true);
    input.value = '';
    input.style.height = 'auto';

    // Disable send button
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;

    // Show typing indicator
    showTyping();

    try {
        console.log('🌐 Envoi requête API...');
        const response = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                language: 'fr'
            })
        });

        console.log('📡 Réponse reçue, status:', response.status);
        const data = await response.json();
        console.log('📦 Données:', data);

        hideTyping();

        if (data.response) {
            console.log('✅ Réponse de l\'IA:', data.response.substring(0, 50) + '...');
            addMessage(data.response, false);
            conversationHistory.push({
                user: message,
                assistant: data.response
            });

            // Sauvegarder dans l'historique persistant
            if (typeof chatHistory !== 'undefined') {
                chatHistory.saveMessage(message, data.response);
            }

            // Lire la réponse à voix haute avec le système Siri
            // UNIQUEMENT si le mode mains libres est actif
            if (window.siriVoiceAssistant && siriVoiceAssistant.handsFreeModeActive) {
                console.log('🔊 Système vocal disponible');
                console.log('🔊 Lecture de la réponse vocale');
                siriVoiceAssistant.speak(data.response);
            } else {
                console.log('⚠️ Mode vocal non actif');
            }
        } else {
            console.error('❌ Pas de réponse dans les données');
            addMessage('Désolé, une erreur est survenue.', false);
        }

    } catch (error) {
        console.error('❌ Erreur:', error);
        hideTyping();
        addMessage('Erreur de connexion. Veuillez réessayer.', false);
    } finally {
        sendBtn.disabled = false;
        input.focus();
        console.log('✅ sendMessage() terminée');
    }
}

// Rendre la fonction globale pour qu'elle soit accessible partout
console.log('🔵 Exposition de sendMessage à window...');
window.sendMessage = sendMessage;
console.log('✅ sendMessage rendue globale, typeof:', typeof window.sendMessage);

// ============================================
// FONCTIONS HISTORIQUE
// ============================================

function showHistoryModal() {
    const modal = document.getElementById('historyModal');
    const conversationsList = document.getElementById('conversationsList');

    // Récupérer toutes les conversations
    const conversations = chatHistory.getConversationList();

    if (conversations.length === 0) {
        conversationsList.innerHTML = `
            <div class="empty-history">
                <div class="empty-history-icon">📭</div>
                <div class="empty-history-text">Aucune conversation sauvegardée</div>
            </div>
        `;
    } else {
        conversationsList.innerHTML = conversations.map(conv => {
            const date = new Date(conv.updatedAt).toLocaleString('fr-FR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            const messageCount = conv.messages.length / 2;
            const isActive = conv.id === chatHistory.currentConversationId;

            return `
                <div class="conversation-item ${isActive ? 'active' : ''}" onclick="loadConversationFromModal('${conv.id}')">
                    <div class="conversation-info">
                        <div class="conversation-title">${conv.title}</div>
                        <div class="conversation-meta">${date} • ${messageCount} message${messageCount > 1 ? 's' : ''}</div>
                    </div>
                    <div class="conversation-actions" onclick="event.stopPropagation()">
                        <button class="conversation-btn delete" onclick="deleteConversationFromModal('${conv.id}')" title="Supprimer">
                            🗑️
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    modal.style.display = 'flex';
}

function closeHistoryModal() {
    const modal = document.getElementById('historyModal');
    modal.style.display = 'none';
}

function loadConversationFromModal(conversationId) {
    chatHistory.loadConversation(conversationId);
    closeHistoryModal();
}

function deleteConversationFromModal(conversationId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette conversation ?')) {
        chatHistory.deleteConversation(conversationId);
        showHistoryModal(); // Rafraîchir la liste
    }
}

// Fermer le modal en cliquant en dehors
document.addEventListener('click', function (event) {
    const modal = document.getElementById('historyModal');
    if (event.target === modal) {
        closeHistoryModal();
    }
});

// ============================================
// FONCTIONS UTILITAIRES
// ============================================

function copyMessage(btn) {
    const messageContent = btn.closest('.message').querySelector('.message-content').innerText;
    navigator.clipboard.writeText(messageContent).then(() => {
        btn.textContent = '✅ Copié';
        setTimeout(() => {
            btn.textContent = '📋 Copier';
        }, 2000);
    });
}

function regenerateResponse() {
    if (conversationHistory.length > 0) {
        const lastMessage = conversationHistory[conversationHistory.length - 1].user;
        document.getElementById('messageInput').value = lastMessage;
        sendMessage();
    }
}

function clearChat() {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = `
        <div class="empty-state" id="emptyState">
            <div class="empty-icon">💬</div>
            <h2 class="empty-title">Comment puis-je vous aider ?</h2>
            <p class="empty-subtitle">Posez-moi vos questions</p>
        </div>
    `;
    conversationHistory = [];
}

// Focus input on load
window.addEventListener('load', () => {
    document.getElementById('messageInput').focus();
});
