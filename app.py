"""
API Flask pour l'Assistant Médical IA
"""

from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os
import uuid

# Charger les variables d'environnement depuis .env
load_dotenv()

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import MedicalChatbot
from enhanced_chatbot import EnhancedMedicalChatbot
from disease_classifier import DiseaseClassifier
from drug_interactions import DrugInteractionChecker
from medical_knowledge import get_disease_info, get_drug_info, check_emergency, get_all_diseases, get_all_drugs
from database import MedicalDatabase
from api_routes import api_bp
from api_integration import api_integration
from teach_routes import teach_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Enregistrer les nouvelles routes API
app.register_blueprint(api_bp)
app.register_blueprint(teach_bp)

# Initialisation de la base de données
db = MedicalDatabase()
db.populate_initial_data()

# Initialisation des composants - Utiliser le chatbot enrichi
chatbot = EnhancedMedicalChatbot()  # Chatbot amélioré
classifier = DiseaseClassifier()
drug_checker = DrugInteractionChecker()

# Entraîner le modèle au démarrage
print("Entraînement du modèle...")
classifier.train()
print("Modèle prêt!")

def get_session_id():
    """Récupère ou crée un ID de session"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

@app.route('/')
def home():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/chat')
def chat_interface():
    """Interface de chat style ChatGPT"""
    return render_template('chat.html')

@app.route('/admin')
def admin():
    """Page d'administration"""
    return render_template('admin.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de santé de l'API"""
    from medical_knowledge import get_knowledge_base_info, check_data_freshness
    
    kb_info = get_knowledge_base_info()
    freshness = check_data_freshness()
    
    return jsonify({
        "status": "healthy",
        "message": "Assistant Médical IA opérationnel",
        "version": kb_info["version"],
        "last_updated": kb_info["last_updated"],
        "data_freshness": freshness,
        "total_diseases": kb_info["total_diseases"],
        "total_drugs": kb_info["total_drugs"],
        "disclaimer": "Informations à but éducatif uniquement"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint pour le chatbot avec support LLM"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        language = data.get('language', 'fr')
        
        if not message:
            return jsonify({"error": "Message vide"}), 400
        
        session_id = get_session_id()
        
        # Ajouter le disclaimer au début de chaque session
        from medical_knowledge import get_medical_disclaimer
        disclaimer = get_medical_disclaimer()
        
        # Appeler le chatbot avec la langue
        response = chatbot.process_message(message, language)
        symptoms = chatbot.get_collected_symptoms()
        
        # Sauvegarder dans la base de données
        db.save_chat_message(session_id, message, response)
        
        # Vérifier si LLM est actif
        llm_active = False
        llm_provider = "Mode basique"
        try:
            from llm_provider import llm
            if llm and llm.is_available():
                llm_active = True
                llm_provider = llm.get_provider_info().get('name', 'LLM')
        except:
            pass
        
        return jsonify({
            "response": response,
            "collected_symptoms": symptoms,
            "session_id": session_id,
            "disclaimer": disclaimer.get(language, disclaimer['fr']),
            "llm_active": llm_active,
            "llm_provider": llm_provider
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    """Analyse des symptômes"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({"error": "Aucun symptôme fourni"}), 400
        
        session_id = get_session_id()
        
        # Vérification d'urgence
        if check_emergency(symptoms):
            return jsonify({
                "emergency": True,
                "message": "URGENCE DÉTECTÉE! Appelez le 15 (SAMU) immédiatement."
            })
        
        # Classification
        results = classifier.predict(symptoms)
        
        if not results:
            return jsonify({
                "emergency": False,
                "results": [],
                "message": "Aucune maladie correspondante. Consultez un médecin."
            })
        
        # Formater les résultats
        formatted_results = []
        predicted_diseases = []
        for result in results[:3]:
            formatted_results.append({
                "disease": result['disease'],
                "confidence": round(result['confidence'] * 100, 1),
                "description": result['info']['description'],
                "severity": result['info']['severity'],
                "symptoms": result['info']['symptoms'],
                "recommendations": result['info']['recommendations']
            })
            predicted_diseases.append({
                "disease": result['disease'],
                "confidence": round(result['confidence'] * 100, 1)
            })
        
        # Sauvegarder la consultation
        db.save_consultation(session_id, symptoms, predicted_diseases)
        
        return jsonify({
            "emergency": False,
            "results": formatted_results,
            "input_symptoms": symptoms,
            "session_id": session_id
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/drugs/check', methods=['POST'])
def check_drugs():
    """Vérification des interactions médicamenteuses"""
    try:
        data = request.get_json()
        drugs = data.get('drugs', [])
        
        if not drugs or len(drugs) < 1:
            return jsonify({"error": "Aucun médicament fourni"}), 400
        
        session_id = get_session_id()
        result = drug_checker.check_interactions(drugs)
        
        # Récupérer les infos détaillées
        drugs_info = []
        for drug in drugs:
            info = drug_checker.get_drug_info(drug)
            if info:
                drugs_info.append({
                    "name": drug,
                    "category": info['category'],
                    "dosage": info['dosage'],
                    "interactions": info['interactions'],
                    "contraindications": info['contraindications']
                })
        
        # Sauvegarder la vérification
        db.save_drug_check(session_id, drugs, not result['safe'], result['interactions'])
        
        return jsonify({
            "safe": result['safe'],
            "interactions": result['interactions'],
            "warnings": result['warnings'],
            "drugs_info": drugs_info,
            "session_id": session_id
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/disease/<disease_name>', methods=['GET'])
def get_disease(disease_name):
    """Récupère les informations sur une maladie"""
    try:
        info = get_disease_info(disease_name)
        
        if not info:
            return jsonify({"error": "Maladie non trouvée"}), 404
        
        return jsonify({
            "name": disease_name,
            "description": info['description'],
            "symptoms": info['symptoms'],
            "recommendations": info['recommendations'],
            "severity": info['severity']
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/drug/<drug_name>', methods=['GET'])
def get_drug(drug_name):
    """Récupère les informations sur un médicament"""
    try:
        info = get_drug_info(drug_name)
        
        if not info:
            return jsonify({"error": "Médicament non trouvé"}), 404
        
        return jsonify({
            "name": drug_name,
            "category": info['category'],
            "dosage": info['dosage'],
            "interactions": info['interactions'],
            "contraindications": info['contraindications']
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/diseases', methods=['GET'])
def list_diseases():
    """Liste toutes les maladies disponibles"""
    return jsonify({
        "diseases": get_all_diseases()
    })

@app.route('/api/drugs', methods=['GET'])
def list_drugs():
    """Liste tous les médicaments disponibles"""
    return jsonify({
        "drugs": get_all_drugs()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


# === NOUVEAUX ENDPOINTS POUR LA BASE DE DONNÉES ===

@app.route('/api/history/consultations', methods=['GET'])
def get_consultation_history():
    """Récupère l'historique des consultations"""
    try:
        session_id = get_session_id()
        limit = request.args.get('limit', 50, type=int)
        
        consultations = db.get_consultations(session_id, limit)
        
        return jsonify({
            "consultations": consultations,
            "count": len(consultations)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/chat', methods=['GET'])
def get_chat_history_endpoint():
    """Récupère l'historique du chat"""
    try:
        session_id = get_session_id()
        limit = request.args.get('limit', 20, type=int)
        
        history = db.get_chat_history(session_id, limit)
        
        return jsonify({
            "history": history,
            "count": len(history)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Récupère les statistiques de l'application"""
    try:
        stats = db.get_statistics()
        
        return jsonify({
            "statistics": stats
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/diseases', methods=['GET', 'POST'])
def manage_diseases():
    """Gestion des maladies (admin)"""
    try:
        if request.method == 'GET':
            diseases = db.get_all_diseases()
            return jsonify({"diseases": diseases})
        
        elif request.method == 'POST':
            data = request.get_json()
            disease_id = db.add_disease(
                name=data['name'],
                description=data['description'],
                symptoms=data['symptoms'],
                recommendations=data['recommendations'],
                severity=data['severity']
            )
            return jsonify({"success": True, "id": disease_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/drugs', methods=['GET', 'POST'])
def manage_drugs():
    """Gestion des médicaments (admin)"""
    try:
        if request.method == 'GET':
            drugs = db.get_all_drugs()
            return jsonify({"drugs": drugs})
        
        elif request.method == 'POST':
            data = request.get_json()
            drug_id = db.add_drug(
                name=data['name'],
                category=data['category'],
                dosage=data['dosage'],
                interactions=data['interactions'],
                contraindications=data['contraindications']
            )
            return jsonify({"success": True, "id": drug_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === ENDPOINTS ANALYSE D'IMAGES ===
# Commenté temporairement - à implémenter plus tard
# from image_analyzer import analyzer

# @app.route('/api/image/analyze', methods=['POST'])
# def analyze_medical_image():
#     """Analyse une image médicale"""
#     try:
#         # Vérifier si une image est présente
#         if 'image' not in request.files and 'image_base64' not in request.json:
#             return jsonify({"error": "Aucune image fournie"}), 400
#         
#         session_id = get_session_id()
#         
#         # Image uploadée
#         if 'image' in request.files:
#             image_file = request.files['image']
#             if image_file.filename == '':
#                 return jsonify({"error": "Nom de fichier vide"}), 400
#             
#             # Lire l'image
#             image_data = image_file.read()
#             result = analyzer.analyze_image(image_data)
#         
#         # Image en base64
#         else:
#             data = request.get_json()
#             base64_string = data.get('image_base64', '')
#             result = analyzer.analyze_image_from_base64(base64_string)
#         
#         # Sauvegarder l'analyse dans la base de données
#         if result.get('success'):
#             top_prediction = result.get('top_prediction', {})
#             db.save_consultation(
#                 session_id,
#                 ["analyse_image"],
#                 [{
#                     "type": "image_analysis",
#                     "condition": top_prediction.get('condition', 'inconnue'),
#                     "confidence": top_prediction.get('confidence', 0)
#                 }]
#             )
#         
#         return jsonify(result)
#     
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/image/abcde', methods=['GET'])
# def get_abcde_rule():
#     """Retourne la règle ABCDE pour l'auto-examen"""
#     try:
#         from image_analyzer import MedicalImageAnalyzer
#         temp_analyzer = MedicalImageAnalyzer()
#         abcde = temp_analyzer.get_abcde_rule()
#         return jsonify(abcde)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/image/skin-cancer-info', methods=['GET'])
# def get_skin_cancer_info():
#     """Retourne des informations sur le cancer de la peau"""
#     try:
#         from image_analyzer import MedicalImageAnalyzer
#         temp_analyzer = MedicalImageAnalyzer()
#         info = temp_analyzer.get_skin_cancer_info()
#         return jsonify(info)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
