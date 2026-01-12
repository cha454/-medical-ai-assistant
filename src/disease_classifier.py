"""
Classificateur de maladies basé sur les symptômes
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
from medical_knowledge import DISEASES_DATABASE

class DiseaseClassifier:
    def __init__(self):
        self.model = None
        self.trained = False
        
    def prepare_training_data(self):
        """Prépare les données d'entraînement depuis la base de connaissances"""
        X = []  # Symptômes
        y = []  # Maladies
        
        for disease, info in DISEASES_DATABASE.items():
            symptoms_text = " ".join(info["symptoms"])
            X.append(symptoms_text)
            y.append(disease)
            
        return X, y
    
    def train(self):
        """Entraîne le modèle de classification"""
        X, y = self.prepare_training_data()
        
        # Pipeline: vectorisation + classification
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
        
        self.model.fit(X, y)
        self.trained = True
        print("✓ Modèle de classification entraîné")
        
    def predict(self, symptoms):
        """Prédit les maladies possibles basées sur les symptômes"""
        if not self.trained:
            self.train()
        
        # Convertir la liste de symptômes en texte
        if isinstance(symptoms, list):
            symptoms_text = " ".join(symptoms)
        else:
            symptoms_text = symptoms
            
        # Prédiction
        prediction = self.model.predict([symptoms_text])[0]
        
        # Probabilités pour toutes les classes
        probabilities = self.model.predict_proba([symptoms_text])[0]
        classes = self.model.classes_
        
        # Trier par probabilité décroissante
        results = []
        for disease, prob in zip(classes, probabilities):
            if prob > 0.1:  # Seuil de confiance minimum
                results.append({
                    "disease": disease,
                    "confidence": prob,
                    "info": DISEASES_DATABASE.get(disease)
                })
        
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
    
    def save_model(self, filepath):
        """Sauvegarde le modèle entraîné"""
        if self.trained:
            with open(filepath, 'wb') as f:
                pickle.dump(self.model, f)
            print(f"✓ Modèle sauvegardé: {filepath}")
    
    def load_model(self, filepath):
        """Charge un modèle pré-entraîné"""
        try:
            with open(filepath, 'rb') as f:
                self.model = pickle.load(f)
            self.trained = True
            print(f"✓ Modèle chargé: {filepath}")
        except FileNotFoundError:
            print(f"⚠ Modèle non trouvé: {filepath}")
            self.train()

# Test du classificateur
if __name__ == "__main__":
    classifier = DiseaseClassifier()
    classifier.train()
    
    # Test
    test_symptoms = ["fièvre", "toux", "fatigue"]
    results = classifier.predict(test_symptoms)
    
    print(f"\nSymptômes: {test_symptoms}")
    print("\nMaladies possibles:")
    for result in results[:3]:
        print(f"- {result['disease']}: {result['confidence']*100:.1f}%")
