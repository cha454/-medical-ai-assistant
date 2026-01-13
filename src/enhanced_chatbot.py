"""
Chatbot médical enrichi avec capacités étendues
"""

import re
from medical_knowledge import DISEASES_DATABASE, DRUGS_DATABASE, EMERGENCY_SYMPTOMS, check_emergency

class EnhancedMedicalChatbot:
    def __init__(self):
        self.conversation_state = "greeting"
        self.collected_symptoms = []
        self.patient_name = None
        self.conversation_history = []
        
        # Base de connaissances étendue
        self.medical_topics = {
            # Anatomie
            "anatomie": {
                "cœur": "Le cœur est un muscle qui pompe le sang dans tout le corps. Il bat environ 100 000 fois par jour.",
                "poumons": "Les poumons permettent l'échange d'oxygène et de dioxyde de carbone. Nous avons deux poumons.",
                "foie": "Le foie est le plus grand organe interne. Il filtre le sang et produit la bile.",
                "reins": "Les reins filtrent le sang et produisent l'urine. Nous en avons deux.",
                "cerveau": "Le cerveau contrôle toutes les fonctions du corps. Il pèse environ 1,4 kg.",
                "estomac": "L'estomac digère les aliments grâce à l'acide gastrique.",
                "intestins": "Les intestins absorbent les nutriments. L'intestin grêle mesure environ 6 mètres."
            },
            
            # Prévention
            "prévention": {
                "hygiène": "Lavez-vous les mains régulièrement, surtout avant de manger et après les toilettes.",
                "alimentation": "Mangez équilibré: fruits, légumes, protéines, céréales complètes. Limitez le sucre et le sel.",
                "exercice": "Faites au moins 30 minutes d'activité physique par jour.",
                "sommeil": "Dormez 7-9 heures par nuit pour une bonne santé.",
                "hydratation": "Buvez 1,5 à 2 litres d'eau par jour.",
                "tabac": "Le tabac est la première cause de mortalité évitable. Arrêter améliore immédiatement la santé.",
                "alcool": "Limitez la consommation d'alcool. Maximum 2 verres par jour pour les hommes, 1 pour les femmes.",
                "stress": "Gérez le stress par la relaxation, la méditation, le sport ou les loisirs."
            },
            
            # Vaccinations
            "vaccins": {
                "importance": "Les vaccins protègent contre les maladies graves. Ils sont sûrs et efficaces.",
                "covid": "Le vaccin COVID-19 réduit les formes graves. Plusieurs doses sont recommandées.",
                "grippe": "Le vaccin contre la grippe est recommandé chaque année, surtout pour les personnes fragiles.",
                "tétanos": "Le rappel du tétanos est nécessaire tous les 10 ans.",
                "rougeole": "Le vaccin ROR protège contre la rougeole, les oreillons et la rubéole."
            },
            
            # Premiers secours
            "premiers_secours": {
                "brûlure": "Refroidissez immédiatement à l'eau froide pendant 10-15 minutes. Ne percez pas les cloques.",
                "coupure": "Nettoyez à l'eau, désinfectez, comprimez si saignement, pansement propre.",
                "étouffement": "Méthode de Heimlich: compressions abdominales vers le haut. Appelez le 15 si inefficace.",
                "malaise": "Allongez la personne, jambes surélevées. Appelez le 15 si perte de conscience.",
                "fracture": "Immobilisez le membre, ne bougez pas la personne. Appelez le 15.",
                "piqûre": "Retirez le dard, désinfectez. Surveillez les signes d'allergie. Appelez le 15 si gonflement important."
            },
            
            # Santé mentale
            "santé_mentale": {
                "dépression": "La dépression est une maladie qui se soigne. Parlez-en à un professionnel.",
                "anxiété": "L'anxiété peut être gérée avec thérapie, relaxation et parfois médicaments.",
                "stress": "Le stress chronique affecte la santé. Techniques: respiration, méditation, sport.",
                "sommeil": "Les troubles du sommeil peuvent être traités. Consultez si persistants.",
                "burn-out": "L'épuisement professionnel nécessite repos et accompagnement psychologique."
            },
            
            # Nutrition
            "nutrition": {
                "protéines": "Sources: viande, poisson, œufs, légumineuses, produits laitiers.",
                "glucides": "Préférez les glucides complexes: céréales complètes, légumineuses.",
                "lipides": "Privilégiez les bonnes graisses: huile d'olive, poissons gras, noix.",
                "vitamines": "Variez votre alimentation pour couvrir tous les besoins en vitamines.",
                "minéraux": "Calcium (produits laitiers), fer (viande, légumes verts), magnésium (fruits secs).",
                "fibres": "Les fibres aident au transit: fruits, légumes, céréales complètes.",
                "eau": "L'eau est essentielle. Buvez régulièrement, même sans soif."
            },
            
            # Grossesse
            "grossesse": {
                "suivi": "Consultations mensuelles recommandées. Échographies à 12, 22 et 32 semaines.",
                "alimentation": "Évitez alcool, tabac, fromages au lait cru, viande crue, poisson cru.",
                "médicaments": "Consultez toujours avant de prendre un médicament pendant la grossesse.",
                "sport": "L'activité physique modérée est bénéfique. Évitez les sports à risque.",
                "symptômes": "Nausées, fatigue, seins sensibles sont normaux. Consultez si saignements ou douleurs."
            },
            
            # Enfants
            "pédiatrie": {
                "fièvre": "Normale jusqu'à 38°C. Donnez du paracétamol si > 38,5°C. Consultez si < 3 mois.",
                "croissance": "Suivez le carnet de santé. Consultez si cassure de la courbe.",
                "alimentation": "Diversification à partir de 4-6 mois. Pas de sel ni sucre avant 1 an.",
                "sommeil": "Nouveau-né: 16-18h. 1 an: 12-14h. 3 ans: 11-13h.",
                "vaccins": "Suivez le calendrier vaccinal. Les vaccins protègent votre enfant."
            },
            
            # Personnes âgées
            "gériatrie": {
                "chutes": "Aménagez le domicile: barres d'appui, éclairage, pas de tapis. Activité physique régulière.",
                "mémoire": "Stimulez la mémoire: lecture, jeux, activités sociales. Consultez si troubles importants.",
                "médicaments": "Attention aux interactions. Revoyez régulièrement avec le médecin.",
                "nutrition": "Risque de dénutrition. Repas réguliers, riches en protéines.",
                "autonomie": "Maintenez l'activité physique et sociale pour préserver l'autonomie."
            }
        }
        
        # Questions fréquentes
        self.faq = {
            "comment ça va": "Je suis un assistant IA, je n'ai pas d'état de santé, mais merci de demander! Comment puis-je vous aider aujourd'hui?",
            "qui es-tu": "Je suis un assistant médical IA conçu pour fournir des informations de santé générales. Je ne remplace pas un médecin.",
            "que peux-tu faire": "Je peux vous informer sur les maladies, symptômes, médicaments, prévention, nutrition et premiers secours. Posez-moi vos questions!",
            "es-tu un vrai médecin": "Non, je suis une intelligence artificielle. Pour un diagnostic ou traitement, consultez toujours un médecin qualifié.",
            "puis-je te faire confiance": "Je fournis des informations basées sur des sources médicales fiables, mais vous devez toujours consulter un professionnel de santé pour votre situation personnelle."
        }
    
    def process_message(self, user_input):
        """Traite le message de l'utilisateur avec intelligence étendue"""
        user_input_lower = user_input.lower()
        
        # Sauvegarder dans l'historique
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Détection d'urgence
        if check_emergency([user_input]):
            response = self._emergency_response()
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # Salutations
        if any(word in user_input_lower for word in ["bonjour", "salut", "hello", "bonsoir", "hey", "coucou"]):
            response = self._greeting_response()
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # FAQ
        for question, answer in self.faq.items():
            if question in user_input_lower:
                self.conversation_history.append({"role": "assistant", "content": answer})
                return answer
        
        # Recherche dans les maladies
        disease_response = self._search_diseases(user_input_lower)
        if disease_response:
            self.conversation_history.append({"role": "assistant", "content": disease_response})
            return disease_response
        
        # Recherche dans les médicaments
        drug_response = self._search_drugs(user_input_lower)
        if drug_response:
            self.conversation_history.append({"role": "assistant", "content": drug_response})
            return drug_response
        
        # Recherche dans les topics médicaux
        topic_response = self._search_medical_topics(user_input_lower)
        if topic_response:
            self.conversation_history.append({"role": "assistant", "content": topic_response})
            return topic_response
        
        # Extraction de symptômes
        symptoms = self._extract_symptoms(user_input)
        if symptoms:
            self.collected_symptoms.extend(symptoms)
            response = self._symptom_acknowledgment(symptoms)
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # Demande d'aide
        if any(word in user_input_lower for word in ["aide", "help", "comment", "peux-tu"]):
            response = self._help_response()
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # Au revoir
        if any(word in user_input_lower for word in ["au revoir", "bye", "merci", "stop", "adieu"]):
            response = self._goodbye_response()
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # Réponse intelligente par défaut
        response = self._intelligent_default_response(user_input)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def _search_diseases(self, query):
        """Recherche intelligente dans les maladies"""
        for disease_name, info in DISEASES_DATABASE.items():
            if disease_name in query or any(symptom in query for symptom in info['symptoms']):
                return f"""**{disease_name.upper()}**

📝 **Description:** {info['description']}

🩺 **Symptômes typiques:** {', '.join(info['symptoms'])}

⚠️ **Gravité:** {info['severity']}

💡 **Recommandations:**
{chr(10).join('• ' + rec for rec in info['recommendations'])}

⚠️ Consultez un médecin pour un diagnostic précis."""
        return None
    
    def _search_drugs(self, query):
        """Recherche intelligente dans les médicaments"""
        for drug_name, info in DRUGS_DATABASE.items():
            if drug_name in query:
                return f"""**💊 {drug_name.upper()}**

📋 **Catégorie:** {info['category']}

💉 **Dosage:** {info['dosage']}

⚠️ **Interactions:** {', '.join(info['interactions']) if info['interactions'] else 'Aucune majeure connue'}

🚫 **Contre-indications:** {', '.join(info['contraindications'])}

⚠️ Ne prenez jamais un médicament sans avis médical."""
        return None
    
    def _search_medical_topics(self, query):
        """Recherche dans les topics médicaux étendus"""
        for category, topics in self.medical_topics.items():
            for topic, info in topics.items():
                if topic in query or category in query:
                    return f"""**{topic.upper()}**

{info}

💡 Pour plus d'informations personnalisées, consultez un professionnel de santé."""
        return None
    
    def _intelligent_default_response(self, query):
        """Réponse intelligente par défaut"""
        # Détection de questions sur la santé générale
        if any(word in query.lower() for word in ["santé", "bien-être", "forme", "conseil"]):
            return """Pour une bonne santé générale, je recommande:

✅ **Alimentation équilibrée:** Fruits, légumes, protéines, céréales complètes
✅ **Activité physique:** 30 minutes par jour minimum
✅ **Sommeil:** 7-9 heures par nuit
✅ **Hydratation:** 1,5-2 litres d'eau par jour
✅ **Gestion du stress:** Relaxation, méditation, loisirs
✅ **Suivi médical:** Consultations régulières

Avez-vous une question plus spécifique?"""
        
        # Détection de questions sur les symptômes
        if any(word in query.lower() for word in ["symptôme", "signe", "douleur", "mal", "souffre"]):
            return """Je comprends que vous avez des symptômes. Pour vous aider au mieux:

1. **Décrivez précisément** vos symptômes
2. **Depuis quand** les ressentez-vous?
3. **Intensité:** Légers, modérés ou intenses?
4. **Autres signes:** Fièvre, fatigue, etc.?

⚠️ Si les symptômes sont intenses ou inquiétants, consultez rapidement un médecin.
🚨 En cas d'urgence, appelez le 15 (SAMU)."""
        
        # Réponse générale
        return """Je n'ai pas trouvé d'information spécifique sur votre question dans ma base de connaissances.

💡 **Je peux vous aider avec:**
• Informations sur les maladies courantes
• Conseils de prévention et hygiène
• Informations sur les médicaments
• Premiers secours
• Nutrition et bien-être
• Santé mentale

Pouvez-vous reformuler votre question ou être plus précis?

⚠️ Pour un avis médical personnalisé, consultez toujours un professionnel de santé."""
    
    def _greeting_response(self):
        """Réponse de salutation enrichie"""
        return """Bonjour! 👋 Je suis votre assistant médical IA.

⚠️ **IMPORTANT:** Je ne remplace pas un médecin. En cas d'urgence, appelez le 15 (SAMU).

💡 **Je peux vous aider avec:**
• Informations sur les maladies et symptômes
• Conseils de prévention et hygiène
• Informations sur les médicaments
• Premiers secours
• Nutrition et bien-être
• Santé mentale

**Comment puis-je vous aider aujourd'hui?**"""
    
    def _help_response(self):
        """Réponse d'aide enrichie"""
        return """**🏥 GUIDE D'UTILISATION**

**Je peux répondre à vos questions sur:**

1. **🦠 Maladies:** "Qu'est-ce que la grippe?", "Symptômes du diabète"
2. **💊 Médicaments:** "À quoi sert le paracétamol?", "Interactions médicamenteuses"
3. **🩺 Symptômes:** "J'ai mal à la tête", "Que faire en cas de fièvre?"
4. **🛡️ Prévention:** "Comment éviter la grippe?", "Conseils d'hygiène"
5. **🥗 Nutrition:** "Alimentation équilibrée", "Vitamines importantes"
6. **🧠 Santé mentale:** "Gérer le stress", "Signes de dépression"
7. **🚑 Premiers secours:** "Que faire en cas de brûlure?", "Gestes d'urgence"

**Posez-moi vos questions en langage naturel!**

⚠️ Pour un diagnostic ou traitement, consultez toujours un médecin."""
    
    def _emergency_response(self):
        """Réponse d'urgence"""
        return """🚨 **URGENCE MÉDICALE DÉTECTÉE** 🚨

**APPELEZ IMMÉDIATEMENT:**
📞 **15** - SAMU (France)
📞 **112** - Numéro d'urgence européen
📞 **18** - Pompiers

**EN ATTENDANT LES SECOURS:**
• Restez calme
• Ne bougez pas la personne (sauf danger immédiat)
• Surveillez la respiration et le pouls
• Suivez les instructions du SAMU

⚠️ **N'ATTENDEZ PAS** - Chaque minute compte!"""
    
    def _goodbye_response(self):
        """Réponse d'au revoir"""
        self.collected_symptoms = []
        return """Au revoir! 👋 Prenez soin de vous.

⚠️ **Rappel:** Consultez toujours un professionnel de santé pour un diagnostic précis.

💡 **Numéros utiles:**
• Urgences: 15 (SAMU)
• Médecin de garde: 116 117
• Antipoison: 01 40 05 48 48

À bientôt!"""
    
    def _extract_symptoms(self, text):
        """Extrait les symptômes du texte"""
        common_symptoms = [
            "fièvre", "toux", "fatigue", "douleur", "maux de tête", 
            "nausées", "vomissements", "diarrhée", "vertiges",
            "courbatures", "frissons", "mal de gorge", "congestion",
            "essoufflement", "perte goût", "perte odorat", "mal de ventre",
            "mal au dos", "mal aux dents", "démangeaisons", "éruption"
        ]
        
        found_symptoms = []
        text_lower = text.lower()
        
        for symptom in common_symptoms:
            if symptom in text_lower:
                found_symptoms.append(symptom)
        
        return found_symptoms
    
    def _symptom_acknowledgment(self, symptoms):
        """Accuse réception des symptômes"""
        response = f"J'ai noté les symptômes suivants: **{', '.join(symptoms)}**\n\n"
        
        if len(self.collected_symptoms) >= 2:
            response += """Pour une analyse plus précise, je vous recommande de:

1. **Noter** depuis quand vous avez ces symptômes
2. **Mesurer** votre température si vous avez de la fièvre
3. **Consulter** un médecin si les symptômes persistent ou s'aggravent

Avez-vous d'autres symptômes à signaler?

⚠️ Si les symptômes sont intenses, consultez rapidement."""
        else:
            response += "Avez-vous d'autres symptômes à signaler?"
        
        return response
    
    def get_collected_symptoms(self):
        """Retourne les symptômes collectés"""
        return self.collected_symptoms
    
    def reset_conversation(self):
        """Réinitialise la conversation"""
        self.collected_symptoms = []
        self.conversation_state = "greeting"
        self.conversation_history = []
