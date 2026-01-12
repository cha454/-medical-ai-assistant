"""
Gestion de la base de données SQLite
"""

import sqlite3
import json
from datetime import datetime
import os

class MedicalDatabase:
    def __init__(self, db_path="medical_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Crée une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialise les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table des maladies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                symptoms TEXT,
                recommendations TEXT,
                severity TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des médicaments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                dosage TEXT,
                interactions TEXT,
                contraindications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des consultations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                symptoms TEXT,
                predicted_diseases TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table de l'historique des conversations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des vérifications de médicaments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drug_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                drugs TEXT,
                has_interactions BOOLEAN,
                interactions TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("✓ Base de données initialisée")
    
    def populate_initial_data(self):
        """Remplit la base avec les données initiales"""
        from medical_knowledge import DISEASES_DATABASE, DRUGS_DATABASE
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insérer les maladies
        for name, info in DISEASES_DATABASE.items():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO diseases (name, description, symptoms, recommendations, severity)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    name,
                    info['description'],
                    json.dumps(info['symptoms']),
                    json.dumps(info['recommendations']),
                    info['severity']
                ))
            except Exception as e:
                print(f"Erreur insertion maladie {name}: {e}")
        
        # Insérer les médicaments
        for name, info in DRUGS_DATABASE.items():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO drugs (name, category, dosage, interactions, contraindications)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    name,
                    info['category'],
                    info['dosage'],
                    json.dumps(info['interactions']),
                    json.dumps(info['contraindications'])
                ))
            except Exception as e:
                print(f"Erreur insertion médicament {name}: {e}")
        
        conn.commit()
        conn.close()
        print("✓ Données initiales insérées")
    
    # === MALADIES ===
    
    def add_disease(self, name, description, symptoms, recommendations, severity):
        """Ajoute une nouvelle maladie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO diseases (name, description, symptoms, recommendations, severity)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, json.dumps(symptoms), json.dumps(recommendations), severity))
        
        conn.commit()
        disease_id = cursor.lastrowid
        conn.close()
        return disease_id
    
    def get_disease(self, name):
        """Récupère une maladie par son nom"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM diseases WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'symptoms': json.loads(row['symptoms']),
                'recommendations': json.loads(row['recommendations']),
                'severity': row['severity']
            }
        return None
    
    def get_all_diseases(self):
        """Récupère toutes les maladies"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM diseases ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        diseases = []
        for row in rows:
            diseases.append({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'symptoms': json.loads(row['symptoms']),
                'recommendations': json.loads(row['recommendations']),
                'severity': row['severity']
            })
        return diseases
    
    def update_disease(self, name, **kwargs):
        """Met à jour une maladie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['symptoms', 'recommendations'] and isinstance(value, list):
                value = json.dumps(value)
            fields.append(f"{key} = ?")
            values.append(value)
        
        values.append(name)
        query = f"UPDATE diseases SET {', '.join(fields)} WHERE name = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def delete_disease(self, name):
        """Supprime une maladie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM diseases WHERE name = ?", (name,))
        conn.commit()
        conn.close()
    
    # === MÉDICAMENTS ===
    
    def add_drug(self, name, category, dosage, interactions, contraindications):
        """Ajoute un nouveau médicament"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO drugs (name, category, dosage, interactions, contraindications)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, dosage, json.dumps(interactions), json.dumps(contraindications)))
        
        conn.commit()
        drug_id = cursor.lastrowid
        conn.close()
        return drug_id
    
    def get_drug(self, name):
        """Récupère un médicament par son nom"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM drugs WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'dosage': row['dosage'],
                'interactions': json.loads(row['interactions']),
                'contraindications': json.loads(row['contraindications'])
            }
        return None
    
    def get_all_drugs(self):
        """Récupère tous les médicaments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM drugs ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        drugs = []
        for row in rows:
            drugs.append({
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'dosage': row['dosage'],
                'interactions': json.loads(row['interactions']),
                'contraindications': json.loads(row['contraindications'])
            })
        return drugs
    
    # === CONSULTATIONS ===
    
    def save_consultation(self, session_id, symptoms, predicted_diseases):
        """Enregistre une consultation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO consultations (session_id, symptoms, predicted_diseases)
            VALUES (?, ?, ?)
        """, (session_id, json.dumps(symptoms), json.dumps(predicted_diseases)))
        
        conn.commit()
        consultation_id = cursor.lastrowid
        conn.close()
        return consultation_id
    
    def get_consultations(self, session_id=None, limit=50):
        """Récupère l'historique des consultations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute("""
                SELECT * FROM consultations 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (session_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM consultations 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        consultations = []
        for row in rows:
            consultations.append({
                'id': row['id'],
                'session_id': row['session_id'],
                'symptoms': json.loads(row['symptoms']),
                'predicted_diseases': json.loads(row['predicted_diseases']),
                'timestamp': row['timestamp']
            })
        return consultations
    
    # === HISTORIQUE CHAT ===
    
    def save_chat_message(self, session_id, user_message, bot_response):
        """Enregistre un message de chat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO chat_history (session_id, user_message, bot_response)
            VALUES (?, ?, ?)
        """, (session_id, user_message, bot_response))
        
        conn.commit()
        conn.close()
    
    def get_chat_history(self, session_id, limit=20):
        """Récupère l'historique de chat"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM chat_history 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'user_message': row['user_message'],
                'bot_response': row['bot_response'],
                'timestamp': row['timestamp']
            })
        return list(reversed(history))
    
    # === VÉRIFICATIONS MÉDICAMENTS ===
    
    def save_drug_check(self, session_id, drugs, has_interactions, interactions):
        """Enregistre une vérification de médicaments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO drug_checks (session_id, drugs, has_interactions, interactions)
            VALUES (?, ?, ?, ?)
        """, (session_id, json.dumps(drugs), has_interactions, json.dumps(interactions)))
        
        conn.commit()
        conn.close()
    
    # === STATISTIQUES ===
    
    def get_statistics(self):
        """Récupère des statistiques générales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM diseases")
        stats['total_diseases'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM drugs")
        stats['total_drugs'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM consultations")
        stats['total_consultations'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM chat_history")
        stats['total_messages'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM drug_checks")
        stats['total_drug_checks'] = cursor.fetchone()['count']
        
        conn.close()
        return stats

# Initialisation globale
db = MedicalDatabase()

if __name__ == "__main__":
    # Test de la base de données
    print("=== Test de la base de données ===\n")
    
    db.populate_initial_data()
    
    print("\nMaladies dans la base:")
    diseases = db.get_all_diseases()
    for disease in diseases:
        print(f"- {disease['name']}: {disease['description']}")
    
    print("\nMédicaments dans la base:")
    drugs = db.get_all_drugs()
    for drug in drugs:
        print(f"- {drug['name']}: {drug['category']}")
    
    print("\nStatistiques:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"- {key}: {value}")
