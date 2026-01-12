"""
Vérification des interactions médicamenteuses
"""

from medical_knowledge import DRUGS_DATABASE

class DrugInteractionChecker:
    def __init__(self):
        self.drugs_db = DRUGS_DATABASE
    
    def check_interactions(self, drug_list):
        """Vérifie les interactions entre plusieurs médicaments"""
        if len(drug_list) < 2:
            return {"safe": True, "interactions": [], "warnings": []}
        
        interactions = []
        warnings = []
        
        for i, drug1 in enumerate(drug_list):
            drug1_lower = drug1.lower()
            if drug1_lower not in self.drugs_db:
                warnings.append(f"⚠ Médicament inconnu: {drug1}")
                continue
            
            drug1_info = self.drugs_db[drug1_lower]
            
            for drug2 in drug_list[i+1:]:
                drug2_lower = drug2.lower()
                if drug2_lower not in self.drugs_db:
                    continue
                
                # Vérifier si drug2 est dans les interactions de drug1
                if drug2_lower in [x.lower() for x in drug1_info.get("interactions", [])]:
                    interactions.append({
                        "drug1": drug1,
                        "drug2": drug2,
                        "severity": "modérée à élevée",
                        "warning": f"Interaction détectée entre {drug1} et {drug2}"
                    })
        
        return {
            "safe": len(interactions) == 0,
            "interactions": interactions,
            "warnings": warnings
        }
    
    def get_drug_info(self, drug_name):
        """Récupère les informations détaillées sur un médicament"""
        drug_lower = drug_name.lower()
        if drug_lower in self.drugs_db:
            return self.drugs_db[drug_lower]
        return None
    
    def check_contraindications(self, drug_name, patient_conditions):
        """Vérifie les contre-indications pour un patient"""
        drug_info = self.get_drug_info(drug_name)
        if not drug_info:
            return {"found": False, "message": "Médicament non trouvé"}
        
        contraindications = drug_info.get("contraindications", [])
        found_contraindications = []
        
        for condition in patient_conditions:
            for contraindication in contraindications:
                if contraindication.lower() in condition.lower():
                    found_contraindications.append({
                        "condition": condition,
                        "contraindication": contraindication
                    })
        
        return {
            "found": len(found_contraindications) > 0,
            "contraindications": found_contraindications,
            "all_contraindications": contraindications
        }

# Test du vérificateur
if __name__ == "__main__":
    checker = DrugInteractionChecker()
    
    # Test 1: Interactions
    drugs = ["ibuprofène", "aspirine"]
    result = checker.check_interactions(drugs)
    print(f"Test interactions: {drugs}")
    print(f"Sûr: {result['safe']}")
    if result['interactions']:
        for interaction in result['interactions']:
            print(f"⚠ {interaction['warning']}")
    
    # Test 2: Contre-indications
    print("\n" + "="*50)
    patient_conditions = ["ulcère gastrique", "hypertension"]
    result = checker.check_contraindications("ibuprofène", patient_conditions)
    print(f"\nTest contre-indications: ibuprofène")
    print(f"Conditions patient: {patient_conditions}")
    if result['found']:
        print("⚠ CONTRE-INDICATIONS TROUVÉES:")
        for ci in result['contraindications']:
            print(f"  - {ci['condition']} → {ci['contraindication']}")
