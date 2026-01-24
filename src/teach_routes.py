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
    Retourne: (question, answer, category, language) ou None si pas d'enseignement détecté
    """
    message_lower = user_message.lower()
    
    # ============================================
    # FILTRER LES NON-ENSEIGNEMENTS
    # ============================================
    # Ne pas enregistrer les salutations simples (UN SEUL MOT)
    simple_greetings = ["bonjour", "salut", "hello", "bonsoir", "hey", "coucou", "hi", "bsr"]
    if message_lower.strip() in simple_greetings:
        print(f"⚠️ Salutation simple ignorée: {user_message}")
        return None
    
    # Ne pas enregistrer les questions sans information (SAUF si contient des mots-clés d'enseignement)
    teaching_keywords = ["signifie", "veut dire", "se dit", "c'est", "=", "soigne", "traite", "guérit"]
    has_teaching_keyword = any(kw in message_lower for kw in teaching_keywords)
    
    question_keywords = ["comment", "pourquoi", "quoi", "quel", "quelle", "qui", "où", "quand", "?"]
    if any(kw in message_lower for kw in question_keywords) and not has_teaching_keyword:
        print(f"⚠️ Question sans enseignement ignorée: {user_message}")
        return None
    
    # Ne pas enregistrer les phrases trop courtes (< 10 caractères)
    if len(user_message.strip()) < 10:
        print(f"⚠️ Message trop court ignoré: {user_message}")
        return None
    
    # Ne pas enregistrer les phrases qui commencent par "je veux" sans information
    if message_lower.startswith("je veux") and not has_teaching_keyword:
        print(f"⚠️ 'Je veux' sans enseignement ignoré: {user_message}")
        return None
    
    # ============================================
    # PATTERNS D'ENSEIGNEMENT
    # ============================================
    patterns = {
        'langue_locale': [
            # Format: "Mbolo = bonjour" ou "Mbolo=bonjour"
            r'^([^\s=]+)\s*=\s*(.+)$',
            # Format: "Nlo signifie fièvre en Fang"
            r'(.+?)\s+(?:signifie|veut dire|c\'est)\s+(.+?)\s+en\s+(\w+)',
            # Format: "bonjour se dit MBOLO en langue fang" (NOUVEAU - ordre différent)
            r'(.+?)\s+se\s+dit\s+(.+?)\s+en\s+(?:langue\s+)?(\w+)',
            # Format: "bonjour en langue fang se dit MBOLO"
            r'(.+?)\s+en\s+(?:langue\s+)?(\w+)\s+(?:signifie|veut dire|se dit|c\'est)\s+(.+)',
            # Format: "en Fang, Nlo signifie fièvre"
            r'en\s+(\w+),?\s+(.+?)\s+(?:signifie|veut dire|se dit|c\'est)\s+(.+)',
            # Format: "bonjour en Fang = Mbolo"
            r'(.+?)\s+en\s+(\w+)\s*=\s*(.+)',
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
    
    # ============================================
    # DÉTECTER ET EXTRAIRE
    # ============================================
    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                if category == 'langue_locale':
                    groups = match.groups()
                    
                    # Format simple: "Mbolo = bonjour"
                    if len(groups) == 2 and '=' in user_message:
                        term = groups[0].strip()
                        meaning = groups[1].strip()
                        # Détecter la langue dans le contexte ou utiliser "langue locale"
                        language = "langue_locale"
                        question = f"Comment dit-on {meaning} ?"
                        answer = f"{term} (en {language})"
                        return (question, answer, category, language)
                    
                    # Format: "Nlo signifie fièvre en Fang" OU "bonjour en langue fang se dit MBOLO"
                    elif len(groups) == 3:
                        # Déterminer le format en fonction de la position de "se dit" dans la phrase
                        words = message_lower.split()
                        
                        # Format: "bonjour se dit MBOLO en langue fang"
                        if 'se' in words and 'dit' in words and words.index('se') < 3:
                            meaning = groups[0].strip()
                            term = groups[1].strip()
                            language = groups[2].strip()
                        # Format: "bonjour en langue fang se dit MBOLO"
                        elif 'en' in words and ('se' in words and 'dit' in words):
                            en_pos = words.index('en')
                            se_pos = words.index('se') if 'se' in words else 999
                            
                            if en_pos < se_pos:
                                # "en" vient avant "se dit" → bonjour en fang se dit MBOLO
                                meaning = groups[0].strip()
                                language = groups[1].strip()
                                term = groups[2].strip()
                            else:
                                # Format par défaut
                                term = groups[0].strip()
                                meaning = groups[1].strip()
                                language = groups[2].strip()
                        # Format: "Nlo signifie fièvre en Fang"
                        else:
                            term = groups[0].strip()
                            meaning = groups[1].strip()
                            language = groups[2].strip()
                        
                        question = f"Comment dit-on {meaning} en {language} ?"
                        answer = term
                        print(f"✅ Pattern détecté: meaning='{meaning}', term='{term}', language='{language}'")
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
    
    # Si aucun pattern ne correspond, NE PAS enregistrer
    return None

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
        
        # NOUVEAU: Chercher d'abord dans la base de connaissances
        knowledge_context = kb.get_context_for_llm(user_message, limit=5)
        
        # Construire le contexte de conversation
        context = TEACHING_SYSTEM_PROMPT + "\n\n"
        
        # Ajouter les connaissances apprises si disponibles
        if knowledge_context:
            context += knowledge_context + "\n\n"
        
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
        knowledge_result = extract_knowledge(user_message, ai_response)
        
        # Sauvegarder SEULEMENT si c'est un vrai enseignement
        knowledge_id = None
        category = None
        language = None
        
        if knowledge_result:
            question, answer, category, language = knowledge_result
            
            # Sauvegarder dans la base de connaissances
            knowledge_id = kb.add_knowledge(
                question=question,
                answer=answer,
                category=category,
                language=language,
                context=user_message,
                source='teaching_mode'
            )
            print(f"✅ Connaissance enregistrée: ID={knowledge_id}, Q='{question}', A='{answer}', Cat={category}, Lang={language}")
        else:
            print(f"⚠️ Pas d'enseignement détecté dans: '{user_message}'")
            print(f"   Message contient {len(user_message)} caractères")
            print(f"   Message lower: '{user_message.lower()}'")
        
        # Obtenir les statistiques
        stats = kb.get_statistics()
        
        return jsonify({
            'response': ai_response,
            'knowledge_id': knowledge_id,
            'knowledge_count': stats['total'],
            'category': category,
            'language': language,
            'knowledge_saved': knowledge_result is not None
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
