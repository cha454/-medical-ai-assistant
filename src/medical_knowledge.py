"""
Base de connaissances médicales
"""

# Base de données des maladies et symptômes
DISEASES_DATABASE = {
    "grippe": {
        "symptoms": ["fièvre", "toux", "fatigue", "courbatures", "maux de tête"],
        "description": "Infection virale respiratoire courante",
        "recommendations": [
            "Repos au lit",
            "Hydratation abondante",
            "Paracétamol pour la fièvre",
            "Consulter si symptômes persistent > 7 jours"
        ],
        "severity": "modérée"
    },
    "covid-19": {
        "symptoms": ["fièvre", "toux sèche", "fatigue", "perte goût", "perte odorat", "difficultés respiratoires"],
        "description": "Infection virale COVID-19",
        "recommendations": [
            "Isolement immédiat",
            "Test PCR recommandé",
            "Surveillance de la saturation en oxygène",
            "Consulter urgence si difficultés respiratoires"
        ],
        "severity": "élevée"
    },
    "migraine": {
        "symptoms": ["maux de tête", "nausées", "sensibilité lumière", "vomissements"],
        "description": "Céphalée intense et récurrente",
        "recommendations": [
            "Repos dans une pièce sombre",
            "Anti-inflammatoires",
            "Éviter les déclencheurs",
            "Consulter un neurologue si fréquent"
        ],
        "severity": "modérée"
    },
    "hypertension": {
        "symptoms": ["maux de tête", "vertiges", "vision trouble", "fatigue"],
        "description": "Pression artérielle élevée",
        "recommendations": [
            "Mesurer régulièrement la tension",
            "Réduire le sel",
            "Activité physique régulière",
            "Consultation médicale obligatoire"
        ],
        "severity": "élevée"
    },
    "diabète": {
        "symptoms": ["soif excessive", "fatigue", "vision trouble", "urines fréquentes", "perte de poids"],
        "description": "Trouble de la régulation du glucose",
        "recommendations": [
            "Test glycémie à jeun",
            "Consultation endocrinologue",
            "Régime alimentaire adapté",
            "Surveillance régulière"
        ],
        "severity": "élevée"
    },
    "gastro-entérite": {
        "symptoms": ["diarrhée", "nausées", "vomissements", "douleurs abdominales", "fièvre"],
        "description": "Infection digestive",
        "recommendations": [
            "Hydratation importante (SRO)",
            "Repos digestif",
            "Réintroduction progressive des aliments",
            "Consulter si déshydratation"
        ],
        "severity": "modérée"
    }
}

# Base de données des médicaments
DRUGS_DATABASE = {
    "paracétamol": {
        "category": "antalgique/antipyrétique",
        "interactions": ["alcool"],
        "contraindications": ["insuffisance hépatique"],
        "dosage": "1g toutes les 6h, max 4g/jour"
    },
    "ibuprofène": {
        "category": "anti-inflammatoire",
        "interactions": ["aspirine", "anticoagulants"],
        "contraindications": ["ulcère gastrique", "insuffisance rénale", "grossesse"],
        "dosage": "400mg toutes les 6-8h, max 1200mg/jour"
    },
    "aspirine": {
        "category": "antalgique/antiagrégant",
        "interactions": ["ibuprofène", "anticoagulants"],
        "contraindications": ["ulcère gastrique", "hémophilie", "enfants < 16 ans"],
        "dosage": "500mg-1g toutes les 4-6h"
    },
    "amoxicilline": {
        "category": "antibiotique",
        "interactions": ["pilule contraceptive"],
        "contraindications": ["allergie pénicilline"],
        "dosage": "Sur prescription médicale uniquement"
    }
}

# Symptômes d'urgence
EMERGENCY_SYMPTOMS = [
    "douleur thoracique",
    "difficultés respiratoires",
    "perte de conscience",
    "hémorragie importante",
    "paralysie",
    "confusion mentale",
    "convulsions",
    "douleur abdominale intense"
]

def get_disease_info(disease_name):
    """Récupère les informations sur une maladie"""
    return DISEASES_DATABASE.get(disease_name.lower())

def get_drug_info(drug_name):
    """Récupère les informations sur un médicament"""
    return DRUGS_DATABASE.get(drug_name.lower())

def check_emergency(symptoms):
    """Vérifie si les symptômes nécessitent une urgence"""
    for symptom in symptoms:
        if any(emergency in symptom.lower() for emergency in EMERGENCY_SYMPTOMS):
            return True
    return False

def get_all_diseases():
    """Retourne la liste de toutes les maladies"""
    return list(DISEASES_DATABASE.keys())

def get_all_drugs():
    """Retourne la liste de tous les médicaments"""
    return list(DRUGS_DATABASE.keys())
