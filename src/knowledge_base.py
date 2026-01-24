"""
Système de gestion de la base de connaissances personnalisée
Permet à l'IA d'apprendre de nouvelles informations via conversation
Support SQLite (local) et PostgreSQL (Railway)
"""

import json
from datetime import datetime
from pathlib import Path
import os

class KnowledgeBase:
    def __init__(self, db_path=None):
        # Détecter si on utilise PostgreSQL (Railway) ou SQLite (local)
        self.use_postgres = False
        self.db_url = os.environ.get('DATABASE_URL')
        
        if self.db_url:
            # PostgreSQL sur Railway
            self.use_postgres = True
            print(f"✓ Utilisation de PostgreSQL (Railway)")
            try:
                import psycopg2
                self.psycopg2 = psycopg2
            except ImportError:
                print("⚠️ psycopg2 non installé, fallback sur SQLite")
                self.use_postgres = False
        
        if not self.use_postgres:
            # SQLite en local
            import sqlite3
            self.sqlite3 = sqlite3
            
            if db_path is None:
                # Essayer différents chemins dans l'ordre de préférence
                possible_paths = [
                    os.environ.get('DATA_DIR'),
                    '/data',
                    os.path.join(os.getcwd(), 'data'),
                    os.getcwd(),
                ]
                
                data_dir = None
                for path in possible_paths:
                    if path and os.path.exists(path):
                        data_dir = path
                        break
                    elif path and path != os.getcwd():
                        try:
                            os.makedirs(path, exist_ok=True)
                            data_dir = path
                            print(f"✓ Dossier data créé: {path}")
                            break
                        except Exception as e:
                            continue
                
                if data_dir is None:
                    data_dir = os.getcwd()
                
                db_path = os.path.join(data_dir, 'knowledge.db')
                print(f"✓ Base de données SQLite: {db_path}")
            
            self.db_path = db_path
        
        self.init_database()
    
    def get_connection(self):
        """Retourne une connexion à la base de données"""
        if self.use_postgres:
            return self.psycopg2.connect(self.db_url)
        else:
            return self.sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialise la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Adapter la syntaxe selon le type de base de données
        if self.use_postgres:
            # PostgreSQL
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id SERIAL PRIMARY KEY,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    language TEXT DEFAULT 'fr',
                    context TEXT,
                    tags TEXT,
                    confidence REAL DEFAULT 1.0,
                    source TEXT DEFAULT 'user',
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    icon TEXT,
                    color TEXT
                )
            ''')
        else:
            # SQLite
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    language TEXT DEFAULT 'fr',
                    context TEXT,
                    tags TEXT,
                    confidence REAL DEFAULT 1.0,
                    source TEXT DEFAULT 'user',
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    icon TEXT,
                    color TEXT
                )
            ''')
        
        # Insérer les catégories par défaut
        default_categories = [
            ('langue_locale', 'Langues locales et traductions', '🌍', '#3b82f6'),
            ('medical', 'Connaissances médicales', '💊', '#10b981'),
            ('personnel', 'Informations personnelles', '👤', '#8b5cf6'),
            ('correction', 'Corrections et feedback', '✏️', '#f59e0b'),
            ('preference', 'Préférences utilisateur', '⚙️', '#6b7280'),
            ('culture', 'Culture et traditions', '🎭', '#ec4899'),
            ('plante', 'Plantes médicinales', '🌿', '#22c55e'),
            ('autre', 'Autres connaissances', '📚', '#64748b')
        ]
        
        for cat in default_categories:
            if self.use_postgres:
                cursor.execute('''
                    INSERT INTO categories (name, description, icon, color)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                ''', cat)
            else:
                cursor.execute('''
                    INSERT OR IGNORE INTO categories (name, description, icon, color)
                    VALUES (?, ?, ?, ?)
                ''', cat)
        
        conn.commit()
        conn.close()
    
    def add_knowledge(self, question, answer, category='autre', language='fr', 
                     context=None, tags=None, source='user'):
        """Ajoute une nouvelle connaissance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tags_str = json.dumps(tags) if tags else None
        
        if self.use_postgres:
            cursor.execute('''
                INSERT INTO knowledge 
                (category, question, answer, language, context, tags, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (category, question, answer, language, context, tags_str, source))
            knowledge_id = cursor.fetchone()[0]
        else:
            cursor.execute('''
                INSERT INTO knowledge 
                (category, question, answer, language, context, tags, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (category, question, answer, language, context, tags_str, source))
            knowledge_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return knowledge_id
    
    def update_knowledge(self, knowledge_id, answer=None, category=None, 
                        language=None, context=None, tags=None):
        """Met à jour une connaissance existante"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if answer:
            updates.append('answer = ' + ('%s' if self.use_postgres else '?'))
            params.append(answer)
        if category:
            updates.append('category = ' + ('%s' if self.use_postgres else '?'))
            params.append(category)
        if language:
            updates.append('language = ' + ('%s' if self.use_postgres else '?'))
            params.append(language)
        if context:
            updates.append('context = ' + ('%s' if self.use_postgres else '?'))
            params.append(context)
        if tags:
            updates.append('tags = ' + ('%s' if self.use_postgres else '?'))
            params.append(json.dumps(tags))
        
        updates.append('date_updated = CURRENT_TIMESTAMP')
        params.append(knowledge_id)
        
        placeholder = '%s' if self.use_postgres else '?'
        query = f"UPDATE knowledge SET {', '.join(updates)} WHERE id = {placeholder}"
        cursor.execute(query, params)
        
        conn.commit()
        conn.close()
    
    def search_knowledge(self, query, category=None, language=None, limit=10):
        """Recherche dans les connaissances avec recherche intelligente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Nettoyer et préparer la requête
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Placeholder selon le type de base de données
        ph = '%s' if self.use_postgres else '?'
        
        # Construire une recherche flexible
        sql = f'''
            SELECT id, category, question, answer, language, context, tags, 
                   confidence, date_created, usage_count
            FROM knowledge
            WHERE (
                LOWER(question) LIKE {ph} OR 
                LOWER(answer) LIKE {ph} OR 
                LOWER(context) LIKE {ph}
        '''
        params = [f'%{query_lower}%', f'%{query_lower}%', f'%{query_lower}%']
        
        # Ajouter une recherche par mots-clés individuels
        for word in query_words:
            if len(word) > 3:  # Ignorer les mots trop courts
                sql += f' OR LOWER(question) LIKE {ph} OR LOWER(answer) LIKE {ph}'
                params.extend([f'%{word}%', f'%{word}%'])
        
        sql += ')'
        
        if category:
            sql += f' AND category = {ph}'
            params.append(category)
        
        if language:
            sql += f' AND language = {ph}'
            params.append(language)
        
        sql += f' ORDER BY confidence DESC, usage_count DESC, date_updated DESC LIMIT {ph}'
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'category': r[1],
                'question': r[2],
                'answer': r[3],
                'language': r[4],
                'context': r[5],
                'tags': json.loads(r[6]) if r[6] else [],
                'confidence': r[7],
                'date_created': r[8],
                'usage_count': r[9]
            }
            for r in results
        ]
    
    def get_all_knowledge(self, category=None, language=None, limit=100):
        """Récupère toutes les connaissances"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        ph = '%s' if self.use_postgres else '?'
        
        sql = f'''
            SELECT id, category, question, answer, language, context, 
                   date_created, usage_count
            FROM knowledge
            WHERE 1=1
        '''
        params = []
        
        if category:
            sql += f' AND category = {ph}'
            params.append(category)
        
        if language:
            sql += f' AND language = {ph}'
            params.append(language)
        
        sql += f' ORDER BY date_updated DESC LIMIT {ph}'
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': r[0],
                'category': r[1],
                'question': r[2],
                'answer': r[3],
                'language': r[4],
                'context': r[5],
                'date_created': r[6],
                'usage_count': r[7]
            }
            for r in results
        ]
    
    def increment_usage(self, knowledge_id):
        """Incrémente le compteur d'utilisation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        ph = '%s' if self.use_postgres else '?'
        
        cursor.execute(f'''
            UPDATE knowledge 
            SET usage_count = usage_count + 1,
                date_updated = CURRENT_TIMESTAMP
            WHERE id = {ph}
        ''', (knowledge_id,))
        
        conn.commit()
        conn.close()
    
    def delete_knowledge(self, knowledge_id):
        """Supprime une connaissance"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        ph = '%s' if self.use_postgres else '?'
        cursor.execute(f'DELETE FROM knowledge WHERE id = {ph}', (knowledge_id,))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Récupère les statistiques de la base de connaissances"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total des connaissances
        cursor.execute('SELECT COUNT(*) FROM knowledge')
        total = cursor.fetchone()[0]
        
        # Par catégorie
        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM knowledge
            GROUP BY category
            ORDER BY count DESC
        ''')
        by_category = dict(cursor.fetchall())
        
        # Par langue
        cursor.execute('''
            SELECT language, COUNT(*) as count
            FROM knowledge
            GROUP BY language
            ORDER BY count DESC
        ''')
        by_language = dict(cursor.fetchall())
        
        # Dernière mise à jour
        cursor.execute('''
            SELECT MAX(date_updated) FROM knowledge
        ''')
        last_update = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'by_category': by_category,
            'by_language': by_language,
            'last_update': last_update
        }
    
    def get_context_for_llm(self, query=None, limit=20):
        """
        Récupère les connaissances pertinentes pour injecter dans le contexte du LLM
        """
        if query:
            knowledge = self.search_knowledge(query, limit=limit)
        else:
            knowledge = self.get_all_knowledge(limit=limit)
        
        if not knowledge:
            return ""
        
        context = "📚 **CONNAISSANCES PERSONNALISÉES APPRISES PAR L'UTILISATEUR** :\n\n"
        context += "⚠️ IMPORTANT: Ces connaissances ont été enseignées par l'utilisateur. Utilise-les EN PRIORITÉ pour répondre.\n\n"
        
        for k in knowledge:
            context += f"**Question/Contexte:** {k['question']}\n"
            context += f"**Réponse apprise:** {k['answer']}\n"
            context += f"**Catégorie:** {k['category']}\n"
            if k['language'] != 'fr':
                context += f"**Langue:** {k['language']}\n"
            if k.get('context'):
                context += f"**Contexte additionnel:** {k['context']}\n"
            context += "\n"
        
        context += "---\n"
        context += "💡 **INSTRUCTION:** Si la question de l'utilisateur correspond à une de ces connaissances, "
        context += "réponds en utilisant EXACTEMENT les informations apprises ci-dessus. "
        context += "L'utilisateur a pris le temps de t'enseigner ces informations, respecte-les !\n"
        context += "---\n\n"
        
        return context
    
    def export_knowledge(self, filepath='knowledge_export.json'):
        """Exporte toutes les connaissances en JSON"""
        knowledge = self.get_all_knowledge(limit=10000)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(knowledge, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def import_knowledge(self, filepath):
        """Importe des connaissances depuis un fichier JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            knowledge_list = json.load(f)
        
        imported = 0
        for k in knowledge_list:
            try:
                self.add_knowledge(
                    question=k['question'],
                    answer=k['answer'],
                    category=k.get('category', 'autre'),
                    language=k.get('language', 'fr'),
                    context=k.get('context'),
                    source='import'
                )
                imported += 1
            except Exception as e:
                print(f"Erreur import: {e}")
        
        return imported
