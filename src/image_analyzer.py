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
