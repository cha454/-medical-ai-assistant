"""
Chatbot médical conversationnel
"""

import re
from medical_knowledge import DISEASES_DATABASE, EMERGENCY_SYMPTOMS, check_emergency

class MedicalChatbot:
    def __init__(self):
        self.conversation_state = "greeting"
        self.collected_symptoms = []
        self.patient_name = None
        
    def process_message(self, user_input):
        """Traite le message de l'utilisateur"""
        user_input_lower = user_input.lower()
        
        # Détection d'urgence
        if check_emergency([user_input]):
            return self._emergency_response()
        
        # Salutations
        if any(word in user_input_lower for word in ["bonjour", "salut", "hello", "bonsoir"]):
            return self._greeting_response()
        
        # Demande d'aide
        if any(word in user_input_lower for word in ["aide", "help", "comment"]):
            return self._help_response()
        
        # Au revoir
        if any(word in user_input_lower for word in ["au revoir", "bye", "merci", "stop"]):
            return self._goodbye_response()
        
        # Extraction de symptômes
        symptoms = self._extract_symptoms(user_input)
        if symptoms:
            self.collected_symptoms.extend(symptoms)
            return self._symptom_acknowledgment(symptoms)
        
        # Réponse par défaut
        return self._default_response()
    
    def _greeting_response(self):
        """Réponse de salutation"""
        return """Bonjour! Je suis votre assistant médical IA.

⚠️ IMPORTANT: Je ne remplace pas un médecin. En cas d'urgence, appelez le 15 (SAMU).

Comment puis-je vous aider aujourd'hui?
- Décrivez vos symptômes
- Posez des questions sur une maladie
- Vérifiez des interactions médicamenteuses

Tapez 'aide' pour plus d'informations."""
    
    def _help_response(self):
        """Réponse d'aide"""
        return """Je peux vous aider avec:

1. 📋 Analyse de symptômes
   Exemple: "J'ai de la fièvre et de la toux"

2. 🔍 Informations sur les maladies
   Exemple: "Qu'est-ce que la grippe?"

3. 💊 Vérification de médicaments
   Exemple: "Puis-je prendre ibuprofène et aspirine?"

4. ⚠️ Détection d'urgences médicales

Que souhaitez-vous faire?"""
    
    def _emergency_response(self):
        """Réponse en cas d'urgence"""
        return """🚨 URGENCE MÉDICALE DÉTECTÉE 🚨

Vos symptômes nécessitent une attention médicale IMMÉDIATE.

APPELEZ IMMÉDIATEMENT:
📞 15 - SAMU (France)
📞 112 - Numéro d'urgence européen

N'attendez pas. Consultez un médecin ou rendez-vous aux urgences."""
    
    def _goodbye_response(self):
        """Réponse d'au revoir"""
        self.collected_symptoms = []
        return """Au revoir! Prenez soin de vous.

⚠️ Rappel: Consultez toujours un professionnel de santé pour un diagnostic précis.

À bientôt! 👋"""
    
    def _extract_symptoms(self, text):
        """Extrait les symptômes du texte"""
        # Liste de symptômes communs
        common_symptoms = [
            "fièvre", "toux", "fatigue", "douleur", "maux de tête", 
            "nausées", "vomissements", "diarrhée", "vertiges",
            "courbatures", "frissons", "mal de gorge", "congestion",
            "essoufflement", "perte goût", "perte odorat"
        ]
        
        found_symptoms = []
        text_lower = text.lower()
        
        for symptom in common_symptoms:
            if symptom in text_lower:
                found_symptoms.append(symptom)
        
        return found_symptoms
    
    def _symptom_acknowledgment(self, symptoms):
        """Accuse réception des symptômes"""
        response = f"J'ai noté les symptômes suivants: {', '.join(symptoms)}\n\n"
        
        if len(self.collected_symptoms) >= 2:
            response += "J'ai suffisamment d'informations. Tapez 'analyser' pour obtenir une analyse, ou continuez à décrire vos symptômes."
        else:
            response += "Avez-vous d'autres symptômes à signaler?"
        
        return response
    
    def _default_response(self):
        """Réponse par défaut"""
        return """Je n'ai pas bien compris. Pouvez-vous:
- Décrire vos symptômes plus clairement
- Taper 'aide' pour voir ce que je peux faire
- Poser une question spécifique sur une maladie ou un médicament"""
    
    def get_collected_symptoms(self):
        """Retourne les symptômes collectés"""
        return self.collected_symptoms
    
    def reset_conversation(self):
        """Réinitialise la conversation"""
        self.collected_symptoms = []
        self.conversation_state = "greeting"

# Test du chatbot
if __name__ == "__main__":
    chatbot = MedicalChatbot()
    
    print("=== Test du Chatbot Médical ===\n")
    
    test_messages = [
        "Bonjour",
        "J'ai de la fièvre et de la toux",
        "Je suis aussi très fatigué",
        "aide",
        "au revoir"
    ]
    
    for message in test_messages:
        print(f"Utilisateur: {message}")
        response = chatbot.process_message(message)
        print(f"Assistant: {response}\n")
        print("-" * 50 + "\n")
