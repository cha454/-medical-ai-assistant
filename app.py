"""
API Flask pour l'Assistant Médical IA
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import MedicalChatbot
from disease_classifier import DiseaseClassifier
from drug_interactions import DrugInteractionChecker
from medical_knowledge import get_disease_info, get_drug_info, check_emergency, get_all_diseases, get_all_drugs

app = Flask(__name__)
CORS(app)

# Initialisation des composants
chatbot = MedicalChatbot()
classifier = DiseaseClassifier()
drug_checker = DrugInteractionChecker()

# Entraîner le modèle au démarrage
print("Entraînement du modèle...")
classifier.train()
print("Modèle prêt!")

@app.route('/')
def home():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de santé de l'API"""
    return jsonify({
        "status": "healthy",
        "message": "Assistant Médical IA opérationnel"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint pour le chatbot"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "Message vide"}), 400
        
        response = chatbot.process_message(message)
        symptoms = chatbot.get_collected_symptoms()
        
        return jsonify({
            "response": response,
            "collected_symptoms": symptoms
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
        for result in results[:3]:
            formatted_results.append({
                "disease": result['disease'],
                "confidence": round(result['confidence'] * 100, 1),
                "description": result['info']['description'],
                "severity": result['info']['severity'],
                "symptoms": result['info']['symptoms'],
                "recommendations": result['info']['recommendations']
            })
        
        return jsonify({
            "emergency": False,
            "results": formatted_results,
            "input_symptoms": symptoms
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
        
        return jsonify({
            "safe": result['safe'],
            "interactions": result['interactions'],
            "warnings": result['warnings'],
            "drugs_info": drugs_info
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
