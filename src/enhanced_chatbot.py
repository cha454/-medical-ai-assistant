"""
Chatbot médical enrichi avec capacités étendues et intelligence contextuelle
+ Recherche web en temps réel
+ Intégration LLM pour réponses ultra-intelligentes
"""

import re
from datetime import datetime
from medical_knowledge import DISEASES_DATABASE, DRUGS_DATABASE, EMERGENCY_SYMPTOMS, check_emergency

# Import du module de recherche web
try:
    from web_search import web_search
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False
    print("⚠️ Module de recherche web non disponible")

# Import du module LLM
try:
    from llm_provider import llm
    LLM_AVAILABLE = llm.is_available()
    if LLM_AVAILABLE:
        print(f"✓ LLM activé: {llm.get_provider_info().get('name', 'Inconnu')}")
except ImportError:
    LLM_AVAILABLE = False
    llm = None
    print("⚠️ Module LLM non disponible")

# Import du module Email
try:
    from email_service import email_service
    EMAIL_AVAILABLE = email_service.is_available()
    if EMAIL_AVAILABLE:
        print("✓ Service email activé")
except ImportError:
    EMAIL_AVAILABLE = False
    email_service = None
    print("⚠️ Module email non disponible")

class EnhancedMedicalChatbot:
    def __init__(self):
        self.conversation_state = "greeting"
        self.collected_symptoms = []
        self.patient_name = None
        self.conversation_history = []
        self.last_topic = None
        self.last_disease = None  # Nouvelle variable pour mémoriser la dernière maladie
        self.user_concerns = []
        
        # Détection d'émotions
        self.emotion_keywords = {
            "inquiet": ["inquiet", "peur", "angoisse", "stress", "anxieux", "nerveux", "préoccupé"],
            "douleur": ["mal", "douleur", "souffre", "fait mal", "insupportable", "intense"],
            "fatigue": ["fatigué", "épuisé", "crevé", "pas d'énergie", "faible"],
            "urgent": ["urgent", "vite", "rapidement", "immédiat", "maintenant", "grave"]
        }
        
        # Synonymes pour meilleure compréhension
        self.synonyms = {
            "tête": ["tête", "crâne", "cerveau"],
            "ventre": ["ventre", "abdomen", "estomac", "intestin"],
            "gorge": ["gorge", "pharynx", "amygdales"],
            "poitrine": ["poitrine", "thorax", "poumons", "cœur"],
            "dos": ["dos", "colonne", "vertèbres", "lombaires"],
            "jambes": ["jambes", "cuisses", "mollets", "pieds"],
            "bras": ["bras", "épaules", "coudes", "mains"]
        }
        
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
    
    def process_message(self, user_input, language="fr"):
        """Traite le message de l'utilisateur avec intelligence étendue et contextuelle"""
        user_input_lower = user_input.lower()
        
        # Sauvegarder dans l'historique
        self.conversation_history.append({
            "role": "user", 
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Détection d'émotions
        emotion = self._detect_emotion(user_input_lower)
        
        # Détection d'urgence - TOUJOURS prioritaire
        if check_emergency([user_input]):
            response = self._emergency_response()
            self._save_response(response)
            return response
        
        # ============================================
        # DÉTECTION DEMANDE D'EMAIL
        # ============================================
        # Détecter uniquement si une adresse email est présente ET un mot-clé d'envoi
        has_email_address = '@' in user_input and '.' in user_input
        email_send_keywords = ["envoie", "envoyer", "envoi"]
        if has_email_address and any(kw in user_input_lower for kw in email_send_keywords):
            try:
                email_response = self._handle_email_request(user_input, user_input_lower)
                if email_response:
                    self._save_response(email_response)
                    return email_response
            except Exception as e:
                print(f"Erreur email: {e}")
                # Continuer avec le mode normal si erreur
        
        # ============================================
        # RECHERCHE WEB + LLM (MODE PRINCIPAL)
        # ============================================
        # Pour toutes les questions (sauf salutations basiques), utiliser recherche web + LLM
        
        # Salutations simples (pas besoin de recherche)
        simple_greetings = ["bonjour", "salut", "hello", "bonsoir", "hey", "coucou", "hi"]
        is_simple_greeting = any(word == user_input_lower.strip() for word in simple_greetings)
        
        if is_simple_greeting:
            response = self._greeting_response()
            self._save_response(response)
            return response
        
        # Au revoir simple
        simple_goodbyes = ["au revoir", "bye", "merci", "adieu", "à bientôt"]
        is_simple_goodbye = any(word == user_input_lower.strip() for word in simple_goodbyes)
        
        if is_simple_goodbye:
            response = self._goodbye_response()
            self._save_response(response)
            return response
        
        # ============================================
        # POUR TOUTES LES AUTRES QUESTIONS: WEB + LLM
        # ============================================
        if LLM_AVAILABLE and llm:
            try:
                # 1. RECHERCHE WEB pour des infos à jour
                web_results = None
                web_context = ""
                
                # Faire une recherche web si la question a plus de 3 mots
                if WEB_SEARCH_AVAILABLE and len(user_input.split()) >= 3:
                    print(f"🔍 Recherche web pour: {user_input}")
                    web_results = web_search.search_medical_info(user_input, language)
                    
                    if web_results and web_results.get("sources"):
                        web_context = "\n\n**Informations trouvées sur le web (à jour):**\n"
                        
                        # Ajouter le résumé Wikipedia si disponible
                        if web_results.get("summary"):
                            web_context += f"Résumé: {web_results['summary'][:800]}\n\n"
                        
                        # Ajouter les sources
                        web_context += "Sources consultées:\n"
                        for source in web_results["sources"][:3]:
                            web_context += f"- {source.get('source', 'Source')}: {source.get('extract', '')[:300]}\n"
                            if source.get('url'):
                                web_context += f"  URL: {source['url']}\n"
                
                # 2. CONTEXTE de la base de données locale
                local_context = self._build_context_for_llm(user_input_lower)
                
                # 3. CONTEXTE de la conversation précédente
                conversation_context = ""
                if self.last_disease and any(word in user_input_lower for word in ["prévention", "prevention", "mesures", "éviter", "protéger", "comment", "pourquoi"]):
                    if self.last_disease in DISEASES_DATABASE:
                        disease_info = DISEASES_DATABASE[self.last_disease]
                        conversation_context = f"""

Contexte de la conversation précédente:
L'utilisateur a demandé des informations sur: {self.last_disease}
Description: {disease_info['description']}
Recommandations: {', '.join(disease_info['recommendations'])}
"""
                
                # 4. CONSTRUIRE LE MESSAGE ENRICHI pour le LLM
                enriched_message = f"""Question de l'utilisateur: {user_input}

{web_context}

Contexte de notre base de données locale:
{local_context}

{conversation_context}

INSTRUCTIONS IMPORTANTES:
- Réponds de manière conversationnelle, naturelle et empathique
- Utilise les informations du web en priorité car elles sont à jour
- Structure ta réponse avec des emojis et des sections claires
- Si c'est une question médicale, ajoute toujours un disclaimer
- Si c'est une question générale (non médicale), réponds normalement sans disclaimer médical
- Cite tes sources quand tu utilises les infos du web
- Sois précis, factuel et vérifié"""
                
                # 5. APPELER LE LLM
                llm_response = llm.generate_response(
                    enriched_message,
                    self.conversation_history[-10:],  # Derniers 10 messages pour contexte
                    language
                )
                
                if llm_response:
                    # Ajouter les sources web si disponibles
                    if web_results and web_results.get("sources"):
                        llm_response += "\n\n---\n**📚 Sources consultées:**\n"
                        for i, source in enumerate(web_results["sources"][:3], 1):
                            reliability = {"very_high": "⭐⭐⭐", "high": "⭐⭐", "medium": "⭐"}.get(source.get("reliability", "medium"), "⭐")
                            llm_response += f"{i}. {source.get('source', 'Source')} {reliability}\n"
                            if source.get('url'):
                                llm_response += f"   🔗 {source['url']}\n"
                    
                    # Ajouter disclaimer seulement pour questions médicales
                    medical_keywords = ["symptôme", "maladie", "douleur", "traitement", "médicament", "santé", "médecin", "diagnostic"]
                    is_medical = any(keyword in user_input_lower for keyword in medical_keywords)
                    
                    if is_medical:
                        llm_response += "\n\n⚠️ *Ces informations sont à but éducatif. Consultez un professionnel de santé pour un avis personnalisé.*"
                    
                    self._save_response(llm_response)
                    return llm_response
                    
            except Exception as e:
                print(f"Erreur LLM/Web: {e}")
                # Continuer avec le mode basique si erreur
        
        # ============================================
        # MODE BASIQUE (si LLM non disponible)
        # ============================================
        
        # Salutations
        if any(word in user_input_lower for word in ["bonjour", "salut", "hello", "bonsoir", "hey", "coucou"]):
            response = self._greeting_response()
            self._save_response(response)
            return response
        
        # Détection du nom
        name_match = re.search(r"je m'appelle (\w+)|mon nom est (\w+)", user_input_lower)
        if name_match:
            self.patient_name = name_match.group(1) or name_match.group(2)
            response = f"Enchanté {self.patient_name.capitalize()}! Comment puis-je vous aider aujourd'hui?"
            self._save_response(response)
            return response
        
        # Questions de suivi (contexte)
        if self.last_topic and any(word in user_input_lower for word in ["plus", "encore", "détails", "expliquer", "pourquoi", "comment"]):
            response = self._elaborate_on_topic()
            self._save_response(response)
            return response
        
        # FAQ
        for question, answer in self.faq.items():
            if question in user_input_lower:
                self._save_response(answer)
                return answer
        
        # Recherche dans les maladies
        disease_response = self._search_diseases(user_input_lower)
        if disease_response:
            self.last_topic = "disease"
            response = self._add_empathy(disease_response, emotion)
            
            # Enrichir avec recherche web si disponible
            if WEB_SEARCH_AVAILABLE and len(user_input.split()) > 2:
                web_info = self._enrich_with_web_search(user_input)
                if web_info:
                    response += f"\n\n{web_info}"
            
            self._save_response(response)
            return response
        
        # Recherche dans les médicaments
        drug_response = self._search_drugs(user_input_lower)
        if drug_response:
            self.last_topic = "drug"
            response = self._add_empathy(drug_response, emotion)
            self._save_response(response)
            return response
        
        # Recherche dans les topics médicaux
        topic_response = self._search_medical_topics(user_input_lower)
        if topic_response:
            self.last_topic = "topic"
            response = self._add_empathy(topic_response, emotion)
            
            # Enrichir avec recherche web
            if WEB_SEARCH_AVAILABLE:
                web_info = self._enrich_with_web_search(user_input)
                if web_info:
                    response += f"\n\n{web_info}"
            
            self._save_response(response)
            return response
        
        # Extraction de symptômes
        symptoms = self._extract_symptoms(user_input)
        if symptoms:
            self.collected_symptoms.extend(symptoms)
            self.user_concerns.append(user_input)
            response = self._symptom_acknowledgment(symptoms, emotion)
            self._save_response(response)
            return response
        
        # Demande d'aide
        if any(word in user_input_lower for word in ["aide", "help", "comment", "peux-tu", "capable"]):
            response = self._help_response()
            self._save_response(response)
            return response
        
        # Au revoir
        if any(word in user_input_lower for word in ["au revoir", "bye", "merci", "stop", "adieu", "à bientôt"]):
            response = self._goodbye_response()
            self._save_response(response)
            return response
        
        # Réponse intelligente par défaut avec contexte
        response = self._intelligent_default_response(user_input, emotion)
        self._save_response(response)
        return response
    
    def _detect_emotion(self, text):
        """Détecte l'émotion dans le message"""
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        return None
    
    def _handle_email_request(self, user_input, user_input_lower):
        """Gère les demandes d'envoi d'email"""
        # Vérifier si le service email est disponible
        if not EMAIL_AVAILABLE or not email_service:
            return """📧 **Service email non disponible**

Le service d'envoi d'email n'est pas configuré actuellement.

**Alternative:** Vous pouvez copier le résumé de notre conversation en cliquant sur le bouton 📋 à côté de chaque message.

Contactez l'administrateur pour activer cette fonctionnalité."""
        
        # Extraire l'adresse email du message
        email_address = email_service.extract_email_from_text(user_input)
        
        if not email_address:
            return """📧 **Envoi de résumé par email**

Je peux vous envoyer un résumé de notre conversation par email.

**Comment faire:**
Dites-moi simplement: "Envoie le résumé à mon.email@exemple.com"

⚠️ Assurez-vous d'inclure une adresse email valide dans votre message."""
        
        # Vérifier qu'il y a une conversation à envoyer
        if len(self.conversation_history) < 2:
            return f"""📧 **Pas assez de contenu**

Je n'ai pas encore assez d'informations à vous envoyer.

Posez-moi d'abord quelques questions sur votre santé, puis demandez-moi d'envoyer le résumé à {email_address}."""
        
        # Envoyer l'email
        result = email_service.send_conversation_summary(
            email_address,
            self.conversation_history,
            self.collected_symptoms if self.collected_symptoms else None
        )
        
        if result["success"]:
            symptoms_text = ', '.join(self.collected_symptoms) if self.collected_symptoms else 'Aucun'
            return f"""📧 **Email envoyé avec succès!** ✅

Le résumé de notre conversation a été envoyé à:
📬 **{email_address}**

**Contenu envoyé:**
• Historique de notre conversation
• Symptômes mentionnés: {symptoms_text}
• Date et heure de la consultation

⚠️ Vérifiez votre dossier spam si vous ne voyez pas l'email.

Puis-je vous aider avec autre chose?"""
        else:
            error_msg = result.get('error', 'Erreur inconnue')
            return f"""📧 **Erreur d'envoi** ❌

Je n'ai pas pu envoyer l'email à {email_address}.

**Raison:** {error_msg}

**Suggestions:**
• Vérifiez que l'adresse email est correcte
• Réessayez dans quelques instants
• Utilisez le bouton 📋 pour copier les messages manuellement

Voulez-vous réessayer?"""
    
    def _add_empathy(self, response, emotion):
        """Ajoute de l'empathie selon l'émotion détectée"""
        empathy_phrases = {
            "inquiet": "Je comprends votre inquiétude. ",
            "douleur": "Je suis désolé que vous souffriez. ",
            "fatigue": "Je comprends que vous vous sentiez fatigué. ",
            "urgent": "Je vois que c'est urgent pour vous. "
        }
        
        if emotion and emotion in empathy_phrases:
            return empathy_phrases[emotion] + response
        return response
    
    def _build_context_for_llm(self, query):
        """Construit le contexte médical pour enrichir la réponse du LLM"""
        context_parts = []
        
        # Chercher dans les maladies
        for disease_name, info in DISEASES_DATABASE.items():
            if disease_name in query or any(symptom in query for symptom in info['symptoms']):
                context_parts.append(f"""
Maladie trouvée: {disease_name}
Description: {info['description']}
Symptômes: {', '.join(info['symptoms'])}
Gravité: {info['severity']}
Recommandations: {', '.join(info['recommendations'])}
""")
                break
        
        # Chercher dans les médicaments
        for drug_name, info in DRUGS_DATABASE.items():
            if drug_name in query:
                context_parts.append(f"""
Médicament trouvé: {drug_name}
Catégorie: {info['category']}
Dosage: {info['dosage']}
Interactions: {', '.join(info['interactions'])}
Contre-indications: {', '.join(info['contraindications'])}
""")
                break
        
        # Chercher dans les topics médicaux (prévention, nutrition, etc.)
        for category, topics in self.medical_topics.items():
            for topic, info in topics.items():
                if topic in query or category in query:
                    context_parts.append(f"""
Topic trouvé: {topic} (catégorie: {category})
Information: {info}
""")
        
        # Synonymes courants
        synonyms_check = {
            "rhume": ["enrhumé", "enrhumée", "nez qui coule"],
            "grippe": ["grippé", "grippée", "syndrome grippal"],
            "migraine": ["migraineux", "mal de tête"],
            "covid": ["covid", "covid-19", "coronavirus"],
        }
        
        for disease, syns in synonyms_check.items():
            if any(s in query for s in syns) and disease in DISEASES_DATABASE:
                info = DISEASES_DATABASE[disease]
                context_parts.append(f"""
Maladie détectée (synonyme): {disease}
Description: {info['description']}
Symptômes: {', '.join(info['symptoms'])}
Recommandations: {', '.join(info['recommendations'])}
""")
                break
        
        # Si on parle de prévention mais pas de maladie spécifique, ajouter infos générales
        if "prévention" in query or "prevention" in query:
            if not context_parts:
                context_parts.append("""
Informations générales sur la prévention:
- Hygiène: Lavage des mains régulier
- Alimentation équilibrée: fruits, légumes, protéines
- Exercice: 30 minutes par jour minimum
- Sommeil: 7-9 heures par nuit
- Hydratation: 1,5-2 litres d'eau par jour
- Vaccinations à jour
- Éviter tabac et alcool excessif
""")
        
        return "\n".join(context_parts) if context_parts else "Aucune information spécifique trouvée dans la base de données locale."
    
    def _elaborate_on_topic(self):
        """Élabore sur le dernier sujet abordé"""
        if not self.last_topic:
            return "De quoi souhaitez-vous que je parle plus en détail?"
        
        elaborations = {
            "disease": """Pour approfondir sur cette maladie:

**Facteurs de risque:**
• Âge, antécédents familiaux, mode de vie
• Certaines conditions médicales préexistantes

**Prévention:**
• Hygiène de vie saine
• Dépistage régulier si nécessaire
• Vaccination si disponible

**Quand consulter:**
• Si les symptômes persistent ou s'aggravent
• Si vous avez des doutes
• Pour un suivi régulier

Avez-vous d'autres questions spécifiques?""",
            
            "drug": """Informations complémentaires sur ce médicament:

**Conservation:**
• À température ambiante sauf indication contraire
• Hors de portée des enfants
• Vérifier la date de péremption

**Effets secondaires possibles:**
• Consultez la notice
• Signalez tout effet inhabituel à votre médecin

**Oubli de dose:**
• Prenez-la dès que possible
• Ne doublez pas la dose suivante

**Questions à poser à votre médecin:**
• Durée du traitement
• Interactions avec vos autres médicaments
• Précautions particulières

Autre chose?""",
            
            "topic": """Pour aller plus loin sur ce sujet:

**Ressources fiables:**
• Santé Publique France
• OMS (Organisation Mondiale de la Santé)
• Votre médecin traitant

**Actions concrètes:**
• Notez vos questions pour votre prochain rendez-vous
• Tenez un journal de santé si nécessaire
• Impliquez vos proches si besoin

Souhaitez-vous des informations sur un aspect particulier?"""
        }
        
        return elaborations.get(self.last_topic, "Que voulez-vous savoir de plus?")
    
    def _save_response(self, response):
        """Sauvegarde la réponse dans l'historique"""
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
    
    def _symptom_acknowledgment(self, symptoms, emotion):
        """Accuse réception des symptômes avec empathie"""
        prefix = ""
        if emotion == "douleur":
            prefix = "Je suis désolé que vous souffriez. "
        elif emotion == "inquiet":
            prefix = "Je comprends votre inquiétude. "
        
        response = f"{prefix}J'ai noté les symptômes suivants: **{', '.join(symptoms)}**\n\n"
        
        # Suggestions personnalisées
        if "fièvre" in symptoms:
            response += "💡 **Conseil:** Prenez votre température et notez-la. Restez hydraté.\n\n"
        
        if "toux" in symptoms:
            response += "💡 **Conseil:** Buvez des boissons chaudes, reposez-vous.\n\n"
        
        if "douleur" in symptoms or any("mal" in s for s in symptoms):
            response += "💡 **Conseil:** Notez l'intensité de la douleur (1-10) et sa localisation précise.\n\n"
        
        if len(self.collected_symptoms) >= 3:
            response += """**📋 Résumé de vos symptômes:**
{symptoms_list}

**Recommandations:**
1. Si ces symptômes persistent > 48h, consultez un médecin
2. Si aggravation, consultez rapidement
3. Notez l'évolution de vos symptômes

Souhaitez-vous une analyse de ces symptômes?""".format(
                symptoms_list='\n'.join(f"• {s}" for s in set(self.collected_symptoms))
            )
        else:
            response += "Avez-vous d'autres symptômes? Plus vous me donnez d'informations, mieux je peux vous orienter."
        
        return response
    
    def _search_diseases(self, query):
        """Recherche intelligente dans les maladies avec synonymes"""
        # Synonymes et variations de mots
        disease_synonyms = {
            "rhume": ["rhume", "enrhumé", "enrhumée", "rhinopharyngite", "nez qui coule", "nez bouché"],
            "grippe": ["grippe", "grippé", "grippée", "syndrome grippal"],
            "gastro-entérite": ["gastro", "gastro-entérite", "gastroentérite"],
            "covid-19": ["covid", "covid-19", "coronavirus"],
            "migraine": ["migraine", "migraineux", "migraineuse"],
            "angine": ["angine", "mal de gorge", "gorge irritée"],
        }
        
        # Chercher d'abord par synonymes
        for disease_name, synonyms in disease_synonyms.items():
            if any(syn in query for syn in synonyms):
                if disease_name in DISEASES_DATABASE:
                    info = DISEASES_DATABASE[disease_name]
                    self.last_disease = disease_name  # Mémoriser la maladie
                    return f"""**{disease_name.upper()}**

📝 **Description:** {info['description']}

🩺 **Symptômes typiques:** {', '.join(info['symptoms'])}

⚠️ **Gravité:** {info['severity']}

💡 **Recommandations:**
{chr(10).join('• ' + rec for rec in info['recommendations'])}

⚠️ Consultez un médecin pour un diagnostic précis."""
        
        # Recherche standard
        for disease_name, info in DISEASES_DATABASE.items():
            if disease_name in query or any(symptom in query for symptom in info['symptoms']):
                self.last_disease = disease_name  # Mémoriser la maladie
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
    
    def _intelligent_default_response(self, query, emotion=None):
        """Réponse intelligente par défaut avec contexte et empathie"""
        
        # Ajouter empathie si émotion détectée
        empathy_prefix = ""
        if emotion == "inquiet":
            empathy_prefix = "Je comprends votre inquiétude. "
        elif emotion == "urgent":
            empathy_prefix = "Je vois que c'est important pour vous. "
        
        # Détection de questions sur la santé générale
        if any(word in query.lower() for word in ["santé", "bien-être", "forme", "conseil", "rester en bonne santé"]):
            return empathy_prefix + """**🌟 Pour une santé optimale, voici mes recommandations:**

**🥗 Alimentation:**
• 5 fruits et légumes par jour
• Protéines variées (viande, poisson, légumineuses)
• Céréales complètes
• Limitez sucre, sel et graisses saturées

**🏃 Activité physique:**
• 30 minutes d'exercice modéré par jour
• Marche, vélo, natation, jardinage...
• Montez les escaliers au lieu de l'ascenseur

**😴 Sommeil:**
• 7-9 heures par nuit
• Horaires réguliers
• Évitez les écrans 1h avant le coucher

**💧 Hydratation:**
• 1,5-2 litres d'eau par jour
• Plus si sport ou chaleur

**🧘 Bien-être mental:**
• Gérez le stress (méditation, yoga, loisirs)
• Maintenez des liens sociaux
• Prenez du temps pour vous

**🏥 Suivi médical:**
• Consultations régulières
• Dépistages recommandés selon l'âge
• Vaccinations à jour

💡 **Astuce:** Commencez par un petit changement à la fois!

Avez-vous une question plus spécifique sur l'un de ces aspects?"""
        
        # Détection de questions sur les symptômes
        if any(word in query.lower() for word in ["symptôme", "signe", "douleur", "mal", "souffre", "ressens"]):
            return empathy_prefix + """**🩺 Pour m'aider à mieux vous orienter, pouvez-vous me dire:**

1. **Quel(s) symptôme(s)** ressentez-vous exactement?
2. **Depuis quand?** (heures, jours, semaines)
3. **Intensité:** Sur une échelle de 1 à 10?
4. **Évolution:** Stable, s'améliore ou s'aggrave?
5. **Autres signes:** Fièvre, fatigue, perte d'appétit?
6. **Contexte:** Après un repas, un effort, au repos?

💡 **Plus vous êtes précis, mieux je peux vous aider!**

⚠️ **Signes d'alerte nécessitant une consultation rapide:**
• Douleur intense et soudaine
• Fièvre élevée persistante
• Difficultés respiratoires
• Saignements importants
• Symptômes qui s'aggravent rapidement

🚨 **En cas d'urgence, appelez le 15 (SAMU)**"""
        
        # Détection de questions sur les traitements
        if any(word in query.lower() for word in ["traitement", "soigner", "guérir", "médicament", "remède"]):
            return empathy_prefix + """**💊 Concernant les traitements:**

**⚠️ Important:** Je ne peux pas prescrire de médicaments. Seul un médecin peut le faire après examen.

**Ce que je peux faire:**
• Vous informer sur les médicaments courants
• Expliquer les interactions médicamenteuses
• Donner des conseils généraux de prévention
• Vous orienter vers une consultation si nécessaire

**Traitements non médicamenteux:**
• Repos et hydratation
• Alimentation adaptée
• Activité physique modérée
• Gestion du stress
• Sommeil de qualité

**Pour un traitement adapté à votre situation:**
1. Consultez votre médecin traitant
2. Décrivez précisément vos symptômes
3. Mentionnez vos antécédents et traitements en cours
4. Suivez les prescriptions à la lettre

Avez-vous une question sur un médicament spécifique ou une maladie?"""
        
        # Détection de questions sur "quand consulter"
        if any(word in query.lower() for word in ["consulter", "médecin", "docteur", "rendez-vous", "aller voir"]):
            return empathy_prefix + """**🏥 Quand consulter un médecin?**

**🚨 URGENCE - Appelez le 15 immédiatement:**
• Douleur thoracique intense
• Difficultés respiratoires sévères
• Perte de conscience
• Hémorragie importante
• Paralysie soudaine
• Convulsions

**⚠️ Consultation rapide (24-48h):**
• Fièvre > 39°C persistante
• Douleur intense non soulagée
• Vomissements/diarrhée avec déshydratation
• Symptômes qui s'aggravent
• Blessure nécessitant des points de suture

**📅 Consultation programmée:**
• Symptômes persistants > 1 semaine
• Fatigue inexpliquée prolongée
• Perte de poids involontaire
• Changement inhabituel dans votre corps
• Suivi de maladie chronique
• Bilan de santé annuel

**💡 En cas de doute, il vaut mieux consulter!**

**Numéros utiles:**
• Urgences: 15 (SAMU)
• Médecin de garde: 116 117
• Antipoison: 01 40 05 48 48

Avez-vous des symptômes spécifiques qui vous inquiètent?"""
        
        # Suggestions basées sur l'historique
        if len(self.conversation_history) > 4:
            return empathy_prefix + """Je n'ai pas trouvé d'information spécifique sur votre question.

**💡 Suggestions basées sur notre conversation:**

Vous pouvez me demander:
• Des détails sur un symptôme spécifique
• Des informations sur une maladie
• Des conseils de prévention
• Des informations sur un médicament
• Quand consulter un médecin

**Ou reformulez votre question différemment.**

Par exemple:
• Au lieu de "J'ai mal", dites "J'ai mal à la tête depuis 2 jours"
• Au lieu de "C'est grave?", décrivez vos symptômes précisément

Je suis là pour vous aider! 😊"""
        
        # Réponse générale
        return empathy_prefix + """Je n'ai pas trouvé d'information spécifique sur votre question dans ma base de connaissances.

**💡 Je peux vous aider avec:**

**🦠 Maladies:** Grippe, diabète, hypertension, migraine, etc.
**💊 Médicaments:** Paracétamol, ibuprofène, antibiotiques, etc.
**🩺 Symptômes:** Fièvre, toux, douleurs, fatigue, etc.
**🛡️ Prévention:** Hygiène, alimentation, exercice, vaccins
**🥗 Nutrition:** Alimentation équilibrée, vitamines, hydratation
**🧠 Santé mentale:** Stress, anxiété, sommeil, burn-out
**🚑 Premiers secours:** Brûlures, coupures, étouffement, etc.
**👶 Pédiatrie:** Santé des enfants, fièvre, croissance
**👴 Gériatrie:** Santé des seniors, prévention des chutes

**Pouvez-vous reformuler votre question ou être plus précis?**

Exemple: "Quels sont les symptômes du diabète?" ou "Comment traiter une brûlure?"

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
        """Extrait les symptômes du texte avec synonymes"""
        common_symptoms = [
            "fièvre", "toux", "fatigue", "douleur", "maux de tête", 
            "nausées", "vomissements", "diarrhée", "vertiges",
            "courbatures", "frissons", "mal de gorge", "congestion",
            "essoufflement", "perte goût", "perte odorat", "mal de ventre",
            "mal au dos", "mal aux dents", "démangeaisons", "éruption",
            "sueurs", "palpitations", "tremblements", "engourdissement",
            "gonflement", "rougeur", "saignement", "brûlure"
        ]
        
        found_symptoms = []
        text_lower = text.lower()
        
        # Recherche directe
        for symptom in common_symptoms:
            if symptom in text_lower:
                found_symptoms.append(symptom)
        
        # Recherche avec synonymes
        if "tête" in text_lower and "mal" in text_lower:
            found_symptoms.append("maux de tête")
        if "ventre" in text_lower and "mal" in text_lower:
            found_symptoms.append("mal de ventre")
        if "gorge" in text_lower and "mal" in text_lower:
            found_symptoms.append("mal de gorge")
        if "dos" in text_lower and "mal" in text_lower:
            found_symptoms.append("mal au dos")
        
        # Température
        if re.search(r"\d{2}[.,]\d", text_lower):
            found_symptoms.append("fièvre")
        
        return list(set(found_symptoms))  # Supprimer les doublons
    
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

    
    def _enrich_with_web_search(self, query):
        """Enrichit la réponse avec des informations du web"""
        if not WEB_SEARCH_AVAILABLE:
            return None
        
        try:
            # Nettoyer la requête
            clean_query = query.strip()
            
            # Rechercher sur le web
            web_results = web_search.search_and_format(clean_query, "fr")
            
            if web_results:
                return f"""---

**🌐 INFORMATIONS COMPLÉMENTAIRES DU WEB:**

{web_results}"""
            
        except Exception as e:
            print(f"Erreur recherche web: {e}")
        
        return None
    
    def search_web_only(self, query):
        """Recherche uniquement sur le web (pour questions non couvertes)"""
        if not WEB_SEARCH_AVAILABLE:
            return "La recherche web n'est pas disponible actuellement."
        
        try:
            results = web_search.search_and_format(query, "fr")
            if results:
                return f"""Je n'ai pas cette information dans ma base de données, mais voici ce que j'ai trouvé sur le web:

{results}

⚠️ **Important:** Ces informations proviennent de sources externes. Vérifiez toujours avec un professionnel de santé."""
            else:
                return "Je n'ai pas trouvé d'informations fiables sur le web pour cette question. Consultez un professionnel de santé."
        except Exception as e:
            return f"Erreur lors de la recherche web: {str(e)}"
