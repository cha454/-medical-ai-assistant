"""
Routes pour le mode enseignement
Permet à l'utilisateur d'enseigner de nouvelles connaissances à l'IA
"""

from flask import Blueprint, render_template, request, jsonify
from src.knowledge_base import KnowledgeBase
from src.llm_provider import llm
import re

teach_bp = Blueprint('teach', __name__)
kb = KnowledgeBase()

# Prompt système pour le mode enseignement
TEACHING_SYSTEM_PROMPT = """Tu es un assistant en mode apprentissage. Ton rôle est d'apprendre de nouvelles informations de l'utilisateur.

Quand l'utilisateur t'enseigne quelque chose, tu dois :
1. Confirmer que tu as bien compris
2. Résumer ce que tu as appris
3. Demander si c'est correct
4. Encourager l'utilisateur à t'enseigner plus

Exemples de ce que tu peux apprendre :
- Langues locales : "Nlo signifie fièvre en Fang"
- Termes médicaux : "Le paludisme se dit malaria en anglais"
- Plantes médicinales : "Le Kinkeliba soigne le paludisme"
- Informations personnelles : "Je suis allergique à la pénicilline"
- Corrections : "Non, la bonne réponse est..."

Réponds toujours de manière encourageante et positive.
Utilise des emojis pour rendre la conversation agréable : ✅ 📚 🎓 💡 🌟
"""

def extract_knowledge(user_message, ai_response):
    """
    Extrait les connaissances d'une conversation d'enseignement
    Retourne: (question, answer, category, language)
    """
    # Patterns pour détecter les enseignements
    patterns = {
        'langue_locale': [
            r'(.+?)\s+(?:signifie|veut dire|se dit|c\'est)\s+(.+?)\s+en\s+(\w+)',
            r'en\s+(\w+),?\s+(.+?)\s+(?:signifie|veut dire|se dit|c\'est)\s+(.+)',
        ],
        'medical': [
            r'(?:le|la|les)\s+(.+?)\s+(?:soigne|traite|guérit)\s+(.+)',
            r'(.+?)\s+est\s+(?:un|une)\s+(?:maladie|symptôme|traitement)',
        ],
        'plante': [
            r'(?:le|la)\s+(.+?)\s+est\s+une\s+plante\s+médicinale',
            r'(.+?)\s+(?:soigne|traite|guérit)',
        ],
        'personnel': [
            r'je\s+suis\s+allergique\s+(?:à|au|aux)\s+(.+)',
            r'j\'ai\s+(?:du|de la|des)\s+(.+)',
        ]
    }
    
    message_lower = user_message.lower()
    
    # Détecter la catégorie et extraire les informations
    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                if category == 'langue_locale':
                    if len(match.groups()) == 3:
                        if 'en' in message_lower.split()[:5]:
                            # Format: "en Fang, Nlo signifie fièvre"
                            language = match.group(1)
                            term = match.group(2)
                            meaning = match.group(3)
                        else:
                            # Format: "Nlo signifie fièvre en Fang"
                            term = match.group(1)
                            meaning = match.group(2)
                            language = match.group(3)
                        
                        question = f"{term} ({language})"
                        answer = meaning
                        return (question, answer, category, language.lower())
                
                elif category == 'medical':
                    question = user_message
                    answer = ai_response
                    return (question, answer, category, 'fr')
                
                elif category == 'plante':
                    question = user_message
                    answer = ai_response
                    return (question, answer, category, 'fr')
                
                elif category == 'personnel':
                    question = user_message
                    answer = ai_response
                    return (question, answer, category, 'fr')
    
    # Si aucun pattern ne correspond, catégorie "autre"
    return (user_message, ai_response, 'autre', 'fr')

@teach_bp.route('/teach')
def teach_page():
    """Page du mode enseignement"""
    return render_template('teach.html')

@teach_bp.route('/api/teach', methods=['POST'])
def teach_api():
    """API pour le mode enseignement"""
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Construire le contexte de conversation
        context = TEACHING_SYSTEM_PROMPT + "\n\n"
        
        # Ajouter l'historique
        for h in history[-5:]:  # Garder les 5 derniers échanges
            context += f"Utilisateur: {h['user']}\n"
            context += f"Assistant: {h['assistant']}\n\n"
        
        context += f"Utilisateur: {user_message}\n"
        context += "Assistant:"
        
        # Obtenir la réponse du LLM
        if llm and llm.is_available():
            ai_response = llm.generate_response(context, [], language='fr')
        else:
            # Mode basique si LLM non disponible
            ai_response = f"Merci ! J'ai bien noté : {user_message}"
        
        # Extraire et sauvegarder la connaissance
        question, answer, category, language = extract_knowledge(user_message, ai_response)
        
        # Sauvegarder dans la base de connaissances
        knowledge_id = kb.add_knowledge(
            question=question,
            answer=answer,
            category=category,
            language=language,
            context=user_message,
            source='teaching_mode'
        )
        
        # Obtenir les statistiques
        stats = kb.get_statistics()
        
        return jsonify({
            'response': ai_response,
            'knowledge_id': knowledge_id,
            'knowledge_count': stats['total'],
            'category': category,
            'language': language
        })
        
    except Exception as e:
        print(f"Erreur API teach: {e}")
        return jsonify({'error': str(e)}), 500

@teach_bp.route('/api/knowledge/stats')
def knowledge_stats():
    """Récupère les statistiques de la base de connaissances"""
    try:
        stats = kb.get_statistics()
        return jsonify(stats)
    except Exception as e:
        print(f"Erreur stats: {e}")
        return jsonify({'error': str(e)}), 500

@teach_bp.route('/knowledge')
def knowledge_page():
    """Page de gestion des connaissances"""
    try:
        # Récupérer toutes les connaissances
        knowledge_list = kb.get_all_knowledge(limit=1000)
        stats = kb.get_statistics()
        
        return render_template('knowledge.html', 
                             knowledge=knowledge_list,
                             stats=stats)
    except Exception as e:
        print(f"Erreur page knowledge: {e}")
        return f"Erreur: {e}", 500

@teach_bp.route('/api/knowledge/<int:knowledge_id>', methods=['DELETE'])
def delete_knowledge(knowledge_id):
    """Supprime une connaissance"""
    try:
        kb.delete_knowledge(knowledge_id)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Erreur suppression: {e}")
        return jsonify({'error': str(e)}), 500

@teach_bp.route('/api/knowledge/export')
def export_knowledge():
    """Exporte toutes les connaissances en JSON"""
    try:
        filepath = kb.export_knowledge()
        return jsonify({
            'success': True,
            'filepath': filepath
        })
    except Exception as e:
        print(f"Erreur export: {e}")
        return jsonify({'error': str(e)}), 500
