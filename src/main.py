"""
Assistant Médical IA - Interface principale
"""

import sys
from chatbot import MedicalChatbot
from disease_classifier import DiseaseClassifier
from drug_interactions import DrugInteractionChecker
from medical_knowledge import get_disease_info, get_drug_info, check_emergency

try:
    from colorama import init, Fore, Style
    init()
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

class MedicalAssistant:
    def __init__(self):
        print("Initialisation de l'Assistant Medical IA...")
        self.chatbot = MedicalChatbot()
        self.classifier = DiseaseClassifier()
        self.drug_checker = DrugInteractionChecker()
        print("Assistant pret!\n")
        
    def print_colored(self, text, color="white"):
        """Affiche du texte coloré si disponible"""
        if HAS_COLOR:
            colors = {
                "red": Fore.RED,
                "green": Fore.GREEN,
                "yellow": Fore.YELLOW,
                "blue": Fore.BLUE,
                "cyan": Fore.CYAN,
                "white": Fore.WHITE
            }
            print(colors.get(color, Fore.WHITE) + text + Style.RESET_ALL)
        else:
            print(text)
    
    def display_menu(self):
        """Affiche le menu principal"""
        self.print_colored("\n" + "="*60, "cyan")
        self.print_colored("ASSISTANT MEDICAL IA", "cyan")
        self.print_colored("="*60, "cyan")
        print("\nChoisissez une option:")
        print("1. Chatbot conversationnel")
        print("2. Analyser des symptomes")
        print("3. Verifier interactions medicamenteuses")
        print("4. Consulter base de connaissances")
        print("5. Quitter")
        self.print_colored("\nCet outil ne remplace pas un medecin!", "yellow")
        print("="*60)
    
    def chatbot_mode(self):
        """Mode chatbot conversationnel"""
        self.print_colored("\nMode Chatbot - Tapez 'menu' pour revenir", "green")
        print("-"*60)
        
        print(self.chatbot.process_message("bonjour"))
        
        while True:
            user_input = input("\nVous: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["menu", "retour", "exit"]:
                break
            
            if user_input.lower() == "analyser":
                symptoms = self.chatbot.get_collected_symptoms()
                if symptoms:
                    self.analyze_symptoms(symptoms)
                else:
                    print("Assistant: Aucun symptome collecte.")
                continue
            
            response = self.chatbot.process_message(user_input)
            print(f"\nAssistant: {response}")
    
    def analyze_symptoms(self, symptoms=None):
        """Analyse les symptômes et prédit les maladies"""
        self.print_colored("\nAnalyse de symptomes", "green")
        print("-"*60)
        
        if not symptoms:
            print("Entrez vos symptomes separes par des virgules")
            print("Exemple: fievre, toux, fatigue")
            symptoms_input = input("\nSymptomes: ").strip()
            
            if not symptoms_input:
                return
            
            symptoms = [s.strip() for s in symptoms_input.split(",")]
        
        if check_emergency(symptoms):
            self.print_colored("\nURGENCE DETECTEE!", "red")
            self.print_colored("Appelez immediatement le 15 (SAMU)", "red")
            return
        
        print(f"\nAnalyse en cours pour: {', '.join(symptoms)}")
        
        results = self.classifier.predict(symptoms)
        
        if not results:
            print("\nAucune maladie correspondante trouvee.")
            print("Consultez un medecin pour un diagnostic precis.")
            return
        
        print("\nMaladies possibles (par ordre de probabilite):\n")
        
        for i, result in enumerate(results[:3], 1):
            disease = result['disease']
            confidence = result['confidence'] * 100
            info = result['info']
            
            self.print_colored(f"{i}. {disease.upper()} - Confiance: {confidence:.1f}%", "cyan")
            print(f"   Description: {info['description']}")
            print(f"   Gravite: {info['severity']}")
            print(f"   Symptomes typiques: {', '.join(info['symptoms'])}")
            print(f"\n   Recommandations:")
            for rec in info['recommendations']:
                print(f"   - {rec}")
            print()
        
        self.print_colored("Consultez un medecin pour un diagnostic definitif", "yellow")

    def check_drug_interactions(self):
        """Vérifie les interactions médicamenteuses"""
        self.print_colored("\nVerification d'interactions medicamenteuses", "green")
        print("-"*60)
        
        print("Entrez les medicaments separes par des virgules")
        print("Exemple: ibuprofene, aspirine")
        print("Disponibles: paracetamol, ibuprofene, aspirine, amoxicilline")
        
        drugs_input = input("\nMedicaments: ").strip()
        
        if not drugs_input:
            return
        
        drugs = [d.strip() for d in drugs_input.split(",")]
        
        print(f"\nVerification pour: {', '.join(drugs)}\n")
        
        result = self.drug_checker.check_interactions(drugs)
        
        if result['warnings']:
            for warning in result['warnings']:
                self.print_colored(warning, "yellow")
        
        if result['safe']:
            self.print_colored("Aucune interaction majeure detectee", "green")
        else:
            self.print_colored("INTERACTIONS DETECTEES:", "red")
            for interaction in result['interactions']:
                print(f"\n{interaction['warning']}")
                print(f"   Gravite: {interaction['severity']}")
        
        print("\nInformations detaillees:\n")
        for drug in drugs:
            info = self.drug_checker.get_drug_info(drug)
            if info:
                print(f"- {drug.upper()}")
                print(f"  Categorie: {info['category']}")
                print(f"  Dosage: {info['dosage']}")
                if info['contraindications']:
                    print(f"  Contre-indications: {', '.join(info['contraindications'])}")
                print()
    
    def knowledge_base(self):
        """Consulte la base de connaissances"""
        self.print_colored("\nBase de connaissances medicales", "green")
        print("-"*60)
        
        print("\nQue souhaitez-vous consulter?")
        print("1. Information sur une maladie")
        print("2. Information sur un medicament")
        
        choice = input("\nChoix: ").strip()
        
        if choice == "1":
            print("\nMaladies disponibles:")
            print("grippe, covid-19, migraine, hypertension, diabete, gastro-enterite")
            disease = input("\nMaladie: ").strip().lower()
            
            info = get_disease_info(disease)
            if info:
                self.print_colored(f"\n{disease.upper()}", "cyan")
                print(f"Description: {info['description']}")
                print(f"Gravite: {info['severity']}")
                print(f"Symptomes: {', '.join(info['symptoms'])}")
                print(f"\nRecommandations:")
                for rec in info['recommendations']:
                    print(f"- {rec}")
            else:
                print("Maladie non trouvee dans la base de donnees")
        
        elif choice == "2":
            print("\nMedicaments disponibles:")
            print("paracetamol, ibuprofene, aspirine, amoxicilline")
            drug = input("\nMedicament: ").strip().lower()
            
            info = get_drug_info(drug)
            if info:
                self.print_colored(f"\n{drug.upper()}", "cyan")
                print(f"Categorie: {info['category']}")
                print(f"Dosage: {info['dosage']}")
                print(f"Interactions: {', '.join(info['interactions']) if info['interactions'] else 'Aucune majeure'}")
                print(f"Contre-indications: {', '.join(info['contraindications'])}")
            else:
                print("Medicament non trouve dans la base de donnees")
    
    def run(self):
        """Lance l'assistant"""
        self.print_colored("\nBienvenue dans l'Assistant Medical IA!", "green")
        
        while True:
            self.display_menu()
            choice = input("\nVotre choix: ").strip()
            
            if choice == "1":
                self.chatbot_mode()
            elif choice == "2":
                self.analyze_symptoms()
            elif choice == "3":
                self.check_drug_interactions()
            elif choice == "4":
                self.knowledge_base()
            elif choice == "5":
                self.print_colored("\nAu revoir! Prenez soin de vous!", "green")
                break
            else:
                self.print_colored("\nChoix invalide", "red")
            
            input("\n[Appuyez sur Entree pour continuer]")

def main():
    """Point d'entrée principal"""
    try:
        assistant = MedicalAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu. Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
