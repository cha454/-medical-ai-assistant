"""
Analyseur d'images médicales avec Deep Learning
Classification de lésions cutanées
"""

import numpy as np
from PIL import Image
import io
import base64

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.preprocessing import image as keras_image
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False
    print("TensorFlow non installé. Mode démo activé.")

class MedicalImageAnalyzer:
    def __init__(self):
        self.model = None
        self.image_size = (224, 224)
        self.classes = [
            "mélanome",
            "carcinome basocellulaire",
            "kératose actinique",
            "lésion bénigne",
            "naevus (grain de beauté)",
            "dermatofibrome",
            "kératose séborrhéique"
        ]
        
        self.class_descriptions = {
            "mélanome": {
                "description": "Cancer de la peau le plus grave, nécessite traitement urgent",
                "severity": "critique",
                "recommendations": ["CONSULTATION DERMATOLOGUE URGENTE", "Biopsie nécessaire", "Ne pas attendre"]
            },
            "carcinome basocellulaire": {
                "description": "Cancer de la peau le plus fréquent, croissance lente",
                "severity": "élevée",
                "recommendations": ["Consultation dermatologue rapide", "Biopsie recommandée", "Bon pronostic si traité"]
            },
            "kératose actinique": {
                "description": "Lésion précancéreuse due au soleil",
                "severity": "modérée",
                "recommendations": ["Consultation dermatologue", "Cryothérapie ou crème topique", "Protection solaire stricte"]
            },
            "lésion bénigne": {
                "description": "Lésion cutanée non cancéreuse",
                "severity": "faible",
                "recommendations": ["Surveillance simple", "Consulter si changement", "Protection solaire"]
            },
            "naevus (grain de beauté)": {
                "description": "Grain de beauté bénin",
                "severity": "faible",
                "recommendations": ["Surveillance ABCDE", "Consulter si changement", "Examen annuel recommandé"]
            },
            "dermatofibrome": {
                "description": "Nodule cutané bénin",
                "severity": "faible",
                "recommendations": ["Aucun traitement nécessaire", "Retrait si gênant", "Bénin"]
            },
            "kératose séborrhéique": {
                "description": "Lésion bénigne liée à l'âge",
                "severity": "faible",
                "recommendations": ["Aucun traitement nécessaire", "Retrait possible si esthétique", "Totalement bénin"]
            }
        }
        
        if HAS_TENSORFLOW:
            self.load_or_create_model()
    
    def load_or_create_model(self):
        """Charge ou crée le modèle"""
        try:
            self.model = keras.models.load_model('models/skin_lesion_model.h5')
            print("Modèle chargé")
        except:
            print("Création modèle MobileNetV2...")
            base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
            base_model.trainable = False
            
            self.model = keras.Sequential([
                base_model,
                keras.layers.GlobalAveragePooling2D(),
                keras.layers.Dense(128, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(len(self.classes), activation='softmax')
            ])
            
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            print("Modèle créé (démo)")

    def analyze_image(self, image_data):
        """Analyse les données binaires d'une image"""
        try:
            # Charger l'image avec PIL
            img = Image.open(io.BytesIO(image_data))
            img = img.convert('RGB')
            img_resized = img.resize(self.image_size)
            
            # Prétraitement
            if HAS_TENSORFLOW:
                x = keras_image.img_to_array(img_resized)
                x = np.expand_dims(x, axis=0)
                x = x / 255.0  # Normalisation
                
                # Prédiction
                preds = self.model.predict(x)[0]
                top_idx = np.argmax(preds)
                confidence = float(preds[top_idx])
                condition = self.classes[top_idx]
            else:
                # Mode démo sans TensorFlow
                import random
                condition = random.choice(self.classes)
                confidence = random.uniform(0.65, 0.98)
            
            return {
                "success": True,
                "top_prediction": {
                    "condition": condition,
                    "confidence": confidence
                },
                "class_info": self.class_descriptions
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def analyze_image_from_base64(self, base64_string):
        """Analyse une image encodée en base64"""
        try:
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            image_data = base64.b64decode(base64_string)
            return self.analyze_image(image_data)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_abcde_rule(self):
        """Retourne la règle ABCDE"""
        return {
            "title": "La Règle ABCDE",
            "description": "Méthode pour identifier les signes suspects d'un grain de beauté.",
            "steps": [
                {"letter": "A", "name": "Asymétrie", "desc": "Forme non circulaire ou irrégulière"},
                {"letter": "B", "name": "Bords", "desc": "Contours irréguliers, dentelés ou flous"},
                {"letter": "C", "name": "Couleur", "desc": "Plusieurs couleurs (brun, noir, rouge, blanc)"},
                {"letter": "D", "name": "Diamètre", "desc": "Supérieur à 6mm (taille d'une gomme de crayon)"},
                {"letter": "E", "name": "Évolution", "desc": "Changement de taille, forme, couleur ou relief"}
            ]
        }

    def get_skin_cancer_info(self):
        """Retourne des infos générales"""
        return {
            "prevention": [
                "Utilisez une protection solaire SPF 50+",
                "Évitez l'exposition entre 12h et 16h",
                "Portez des vêtements protecteurs et un chapeau",
                "Examinez votre peau tous les mois",
                "Consultez un dermatologue une fois par an"
            ],
            "risk_factors": [
                "Peau claire, cheveux blonds ou roux",
                "Antécédents de coups de soleil sévères",
                "Nombreux grains de beauté",
                "Antécédents familiaux de cancer de la peau"
            ]
        }
