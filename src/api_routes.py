"""
Routes API supplémentaires pour l'intégration des services externes
À importer dans app.py
"""

from flask import Blueprint, request, jsonify, session
from api_integration import api_integration
import uuid

# Créer un Blueprint pour les routes API
api_bp = Blueprint('api_extended', __name__, url_prefix='/api')


def get_session_id():
    """Récupère ou crée un ID de session"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']


# === STATUS & HEALTH ===

@api_bp.route('/services/status', methods=['GET'])
def get_services_status():
    """Retourne le statut de tous les services intégrés"""
    try:
        status = api_integration.get_service_status()
        available = api_integration.get_available_services()
        
        return jsonify({
            'success': True,
            'services': status,
            'available_services': available,
            'total_active': len(available)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/services/info', methods=['GET'])
def get_integration_info():
    """Informations complètes sur les intégrations"""
    try:
        info = api_integration.get_integration_info()
        return jsonify({
            'success': True,
            'info': info
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# === LLM ENDPOINTS ===

@api_bp.route('/llm/generate', methods=['POST'])
def llm_generate():
    """Génère une réponse avec le LLM"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        context = data.get('context')
        language = data.get('language', 'fr')
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt requis'}), 400
        
        result = api_integration.generate_llm_response(prompt, context, language)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 503
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/llm/chat', methods=['POST'])
def llm_chat():
    """Chat conversationnel avec le LLM"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        history = data.get('history', [])
        language = data.get('language', 'fr')
        
        if not message:
            return jsonify({'success': False, 'error': 'Message requis'}), 400
        
        result = api_integration.chat_with_llm(message, history, language)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 503
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# === EMAIL ENDPOINTS ===

@api_bp.route('/email/send', methods=['POST'])
def send_email():
    """Envoie un email"""
    try:
        data = request.get_json()
        to_email = data.get('to_email', '')
        subject = data.get('subject', '')
        body = data.get('body', '')
        
        if not to_email or not subject or not body:
            return jsonify({
                'success': False,
                'error': 'to_email, subject et body requis'
            }), 400
        
        result = api_integration.send_email(to_email, subject, body)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 503
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/email/consultation', methods=['POST'])
def send_consultation_email():
    """Envoie un résumé de consultation par email"""
    try:
        data = request.get_json()
        to_email = data.get('to_email', '')
        conversation = data.get('conversation', [])
        symptoms = data.get('symptoms', [])
        
        if not to_email:
            return jsonify({
                'success': False,
                'error': 'to_email requis'
            }), 400
        
        if not conversation:
            return jsonify({
                'success': False,
                'error': 'conversation requise'
            }), 400
        
        result = api_integration.send_consultation_summary(
            to_email, 
            conversation, 
            symptoms if symptoms else None
        )
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 503
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# === WEB SEARCH ENDPOINTS ===

@api_bp.route('/search/medical', methods=['POST'])
def search_medical():
    """Recherche des informations médicales sur le web"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        language = data.get('language', 'fr')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query requis'
            }), 400
        
        result = api_integration.search_medical_info(query, language)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 503
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/search/formatted', methods=['POST'])
def search_formatted():
    """Recherche et retourne un résultat formaté"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        language = data.get('language', 'fr')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query requis'
            }), 400
        
        formatted = api_integration.search_and_format(query, language)
        
        if formatted:
            return jsonify({
                'success': True,
                'formatted_result': formatted
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Aucun résultat trouvé'
            }), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# === IMAGE ANALYSIS ENDPOINTS ===

@api_bp.route('/image/analyze', methods=['POST'])
def analyze_image():
    """Analyse une image médicale"""
    try:
        # Image uploadée
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'Nom de fichier vide'
                }), 400
            
            image_data = image_file.read()
            result = api_integration.analyze_medical_image(image_data)
        
        # Image en base64
        elif request.is_json:
            data = request.get_json()
            base64_string = data.get('image_base64', '')
            
            if not base64_string:
                return jsonify({
                    'success': False,
                    'error': 'image ou image_base64 requis'
                }), 400
            
            result = api_integration.analyze_image_from_base64(base64_string)
        
        else:
            return jsonify({
                'success': False,
                'error': 'Format non supporté'
            }), 400
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 503
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# === COMBINED ENDPOINTS (Intelligence augmentée) ===

@api_bp.route('/enhanced/chat', methods=['POST'])
def enhanced_chat():
    """
    Chat enrichi qui combine:
    - Chatbot de base
    - LLM si disponible
    - Recherche web si nécessaire
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        language = data.get('language', 'fr')
        use_web_search = data.get('use_web_search', False)
        
        if not message:
            return jsonify({'success': False, 'error': 'Message requis'}), 400
        
        session_id = get_session_id()
        response_data = {
            'success': True,
            'session_id': session_id,
            'sources': []
        }
        
        # 1. Essayer avec le LLM d'abord
        if api_integration.is_service_available('llm'):
            llm_result = api_integration.generate_llm_response(message, language=language)
            if llm_result.get('success'):
                response_data['response'] = llm_result['response']
                response_data['source'] = 'llm'
                response_data['provider'] = llm_result.get('provider')
        
        # 2. Fallback sur le chatbot de base
        if 'response' not in response_data:
            from enhanced_chatbot import EnhancedMedicalChatbot
            chatbot = EnhancedMedicalChatbot()
            response = chatbot.process_message(message, language)
            response_data['response'] = response
            response_data['source'] = 'chatbot'
        
        # 3. Ajouter recherche web si demandé
        if use_web_search and api_integration.is_service_available('web_search'):
            search_result = api_integration.search_and_format(message, language)
            if search_result:
                response_data['web_search'] = search_result
                response_data['sources'].append('web')
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/enhanced/diagnose', methods=['POST'])
def enhanced_diagnose():
    """
    Diagnostic enrichi qui combine:
    - Classification ML
    - LLM pour explication
    - Recherche web pour informations supplémentaires
    """
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        language = data.get('language', 'fr')
        
        if not symptoms:
            return jsonify({'success': False, 'error': 'Symptômes requis'}), 400
        
        from disease_classifier import DiseaseClassifier
        from medical_knowledge import check_emergency
        
        # 1. Vérification d'urgence
        if check_emergency(symptoms):
            return jsonify({
                'success': True,
                'emergency': True,
                'message': 'URGENCE DÉTECTÉE! Appelez le 15 (SAMU) immédiatement.'
            })
        
        # 2. Classification ML
        classifier = DiseaseClassifier()
        results = classifier.predict(symptoms)
        
        response_data = {
            'success': True,
            'emergency': False,
            'results': results[:3] if results else [],
            'sources': ['ml_classifier']
        }
        
        # 3. Enrichir avec LLM si disponible
        if results and api_integration.is_service_available('llm'):
            top_disease = results[0]['disease']
            prompt = f"Explique brièvement la maladie '{top_disease}' et ses symptômes en 3 phrases."
            llm_result = api_integration.generate_llm_response(prompt, language=language)
            
            if llm_result.get('success'):
                response_data['llm_explanation'] = llm_result['response']
                response_data['sources'].append('llm')
        
        # 4. Ajouter recherche web
        if results and api_integration.is_service_available('web_search'):
            top_disease = results[0]['disease']
            search_result = api_integration.search_and_format(top_disease, language)
            
            if search_result:
                response_data['web_info'] = search_result
                response_data['sources'].append('web')
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# === UTILITY ENDPOINTS ===

@api_bp.route('/services/reload', methods=['POST'])
def reload_services():
    """Recharge tous les services (admin)"""
    try:
        api_integration.reload_services()
        return jsonify({
            'success': True,
            'message': 'Services rechargés',
            'available': api_integration.get_available_services()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Export du Blueprint
__all__ = ['api_bp']
