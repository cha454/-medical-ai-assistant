/**
 * Fonctions de chat (sans système vocal)
 * Le système vocal est géré par voice-assistant-siri.js et voice-integration.js
 */

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
        formattedContent = marked.parse(content);
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
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message) return;

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
        const response = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                language: 'fr'
            })
        });

        const data = await response.json();

        hideTyping();

        if (data.response) {
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
            if (window.siriVoiceAssistant && window.siriVoiceAssistant.handsFreeModeActive) {
                window.siriVoiceAssistant.speak(data.response);
            }
        } else {
            addMessage('Désolé, une erreur est survenue.', false);
        }

    } catch (error) {
        hideTyping();
        addMessage('Erreur de connexion. Veuillez réessayer.', false);
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

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
            <div class="empty-title">Comment puis-je vous aider ?</div>
            <div class="empty-subtitle">Posez-moi vos questions médicales</div>
            
            <div class="suggestions">
                <div class="suggestion" onclick="sendSuggestion('Quels sont les symptômes du diabète ?')">
                    <div class="suggestion-icon">🩺</div>
                    <div class="suggestion-text">Symptômes du diabète</div>
                </div>
                <div class="suggestion" onclick="sendSuggestion('Comment traiter une migraine ?')">
                    <div class="suggestion-icon">💊</div>
                    <div class="suggestion-text">Traiter une migraine</div>
                </div>
                <div class="suggestion" onclick="sendSuggestion('Puis-je prendre ibuprofène et aspirine ensemble ?')">
                    <div class="suggestion-icon">⚠️</div>
                    <div class="suggestion-text">Interactions médicamenteuses</div>
                </div>
                <div class="suggestion" onclick="sendSuggestion('Que faire en cas de fièvre ?')">
                    <div class="suggestion-icon">🌡️</div>
                    <div class="suggestion-text">Fièvre - Que faire ?</div>
                </div>
            </div>
        </div>
    `;
    conversationHistory = [];
}

// Focus input on load
window.addEventListener('load', () => {
    document.getElementById('messageInput').focus();
});
