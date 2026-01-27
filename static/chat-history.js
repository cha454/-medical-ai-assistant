/**
 * Gestion de l'historique des conversations
 * - Sauvegarde dans localStorage
 * - Export PDF
 * - Gestion des conversations multiples
 */

class ChatHistory {
    constructor() {
        this.storageKey = 'medical_ai_conversations';
        this.currentConversationId = null;
        this.init();
    }

    init() {
        // Charger ou créer une conversation
        const savedId = localStorage.getItem('current_conversation_id');
        if (savedId && this.conversationExists(savedId)) {
            this.currentConversationId = savedId;
            this.loadConversation(savedId);
        } else {
            this.createNewConversation();
        }
    }

    // Créer une nouvelle conversation
    createNewConversation() {
        this.currentConversationId = 'conv_' + Date.now();
        localStorage.setItem('current_conversation_id', this.currentConversationId);

        const conversations = this.getAllConversations();
        conversations[this.currentConversationId] = {
            id: this.currentConversationId,
            title: 'Nouvelle conversation',
            messages: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        this.saveAllConversations(conversations);

        // Vider l'affichage
        this.clearDisplay();

        return this.currentConversationId;
    }

    // Sauvegarder un message
    saveMessage(userMessage, assistantResponse) {
        const conversations = this.getAllConversations();
        const conversation = conversations[this.currentConversationId];

        if (!conversation) {
            console.error('Conversation not found');
            return;
        }

        // Ajouter les messages
        conversation.messages.push({
            role: 'user',
            content: userMessage,
            timestamp: new Date().toISOString()
        });

        conversation.messages.push({
            role: 'assistant',
            content: assistantResponse,
            timestamp: new Date().toISOString()
        });

        // Mettre à jour le titre si c'est le premier message
        if (conversation.messages.length === 2) {
            conversation.title = userMessage.substring(0, 50) + (userMessage.length > 50 ? '...' : '');
        }

        conversation.updatedAt = new Date().toISOString();

        this.saveAllConversations(conversations);
    }

    // Charger une conversation
    loadConversation(conversationId) {
        const conversations = this.getAllConversations();
        const conversation = conversations[conversationId];

        if (!conversation) {
            console.error('Conversation not found');
            return;
        }

        this.currentConversationId = conversationId;
        localStorage.setItem('current_conversation_id', conversationId);

        // Vider l'affichage
        this.clearDisplay();

        // Afficher tous les messages
        conversation.messages.forEach(msg => {
            if (typeof addMessage === 'function') {
                addMessage(msg.content, msg.role === 'user');
            }
        });

        return conversation;
    }

    // Supprimer une conversation
    deleteConversation(conversationId) {
        const conversations = this.getAllConversations();
        delete conversations[conversationId];
        this.saveAllConversations(conversations);

        // Si c'est la conversation actuelle, en créer une nouvelle
        if (conversationId === this.currentConversationId) {
            this.createNewConversation();
        }
    }

    // Obtenir toutes les conversations
    getAllConversations() {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : {};
    }

    // Sauvegarder toutes les conversations
    saveAllConversations(conversations) {
        localStorage.setItem(this.storageKey, JSON.stringify(conversations));
    }

    // Vérifier si une conversation existe
    conversationExists(conversationId) {
        const conversations = this.getAllConversations();
        return !!conversations[conversationId];
    }

    // Vider l'affichage
    clearDisplay() {
        const messagesDiv = document.getElementById('messages');
        if (messagesDiv) {
            messagesDiv.innerHTML = `
                <div class="empty-state" id="emptyState">
                    <div class="empty-icon">💬</div>
                    <div class="empty-title">Comment puis-je vous aider ?</div>
                    <div class="empty-subtitle">Posez-moi vos questions</div>
                </div>
            `;
        }
    }

    // Exporter en PDF
    async exportToPDF() {
        const conversation = this.getAllConversations()[this.currentConversationId];

        if (!conversation || conversation.messages.length === 0) {
            alert('Aucune conversation à exporter');
            return;
        }

        try {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            // Configuration
            const pageWidth = doc.internal.pageSize.getWidth();
            const pageHeight = doc.internal.pageSize.getHeight();
            const margin = 20;
            const maxWidth = pageWidth - 2 * margin;
            let yPosition = margin;

            // Titre
            doc.setFontSize(18);
            doc.setFont(undefined, 'bold');
            doc.text('Assistant Médical IA', margin, yPosition);
            yPosition += 10;

            doc.setFontSize(12);
            doc.setFont(undefined, 'normal');
            doc.text(conversation.title, margin, yPosition);
            yPosition += 7;

            doc.setFontSize(10);
            doc.setTextColor(128, 128, 128);
            const date = new Date(conversation.createdAt).toLocaleString('fr-FR');
            doc.text(`Date: ${date}`, margin, yPosition);
            yPosition += 15;

            // Messages
            doc.setTextColor(0, 0, 0);
            conversation.messages.forEach((msg, index) => {
                // Vérifier si on doit ajouter une nouvelle page
                if (yPosition > pageHeight - 40) {
                    doc.addPage();
                    yPosition = margin;
                }

                // Auteur
                doc.setFontSize(11);
                doc.setFont(undefined, 'bold');
                const author = msg.role === 'user' ? '👤 Vous' : '🤖 Assistant';
                doc.text(author, margin, yPosition);
                yPosition += 7;

                // Contenu (nettoyer le Markdown)
                doc.setFont(undefined, 'normal');
                doc.setFontSize(10);
                const cleanContent = msg.content
                    .replace(/#{1,6}\s/g, '')
                    .replace(/\*\*/g, '')
                    .replace(/\*/g, '')
                    .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1');

                const lines = doc.splitTextToSize(cleanContent, maxWidth);
                lines.forEach(line => {
                    if (yPosition > pageHeight - 20) {
                        doc.addPage();
                        yPosition = margin;
                    }
                    doc.text(line, margin, yPosition);
                    yPosition += 5;
                });

                yPosition += 10;
            });

            // Footer
            const totalPages = doc.internal.getNumberOfPages();
            for (let i = 1; i <= totalPages; i++) {
                doc.setPage(i);
                doc.setFontSize(8);
                doc.setTextColor(128, 128, 128);
                doc.text(
                    `Page ${i} sur ${totalPages}`,
                    pageWidth / 2,
                    pageHeight - 10,
                    { align: 'center' }
                );
            }

            // Disclaimer
            doc.setPage(totalPages);
            yPosition = pageHeight - 30;
            doc.setFontSize(8);
            doc.setTextColor(255, 0, 0);
            const disclaimer = doc.splitTextToSize(
                '⚠️ Ces informations sont à but éducatif uniquement. Consultez toujours un professionnel de santé.',
                maxWidth
            );
            disclaimer.forEach(line => {
                doc.text(line, margin, yPosition);
                yPosition += 4;
            });

            // Télécharger
            const filename = `conversation_${new Date().toISOString().split('T')[0]}.pdf`;
            doc.save(filename);

            return true;
        } catch (error) {
            console.error('Erreur lors de l\'export PDF:', error);
            alert('Erreur lors de l\'export PDF. Vérifiez que jsPDF est chargé.');
            return false;
        }
    }

    // Obtenir le nombre de conversations
    getConversationCount() {
        return Object.keys(this.getAllConversations()).length;
    }

    // Obtenir la liste des conversations (triées par date)
    getConversationList() {
        const conversations = this.getAllConversations();
        return Object.values(conversations).sort((a, b) =>
            new Date(b.updatedAt) - new Date(a.updatedAt)
        );
    }
}

// Instance globale
const chatHistory = new ChatHistory();
