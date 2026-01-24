#!/usr/bin/env python3
"""
Script de nettoyage de la base de connaissances
Supprime les connaissances non pertinentes (questions, conversations, salutations)
"""

import sqlite3
import sys

def clean_knowledge_database(db_path='knowledge.db', dry_run=False):
    """
    Nettoie la base de connaissances
    
    Args:
        db_path: Chemin vers la base de données
        dry_run: Si True, affiche ce qui serait supprimé sans supprimer
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("="*60)
    print("🧹 NETTOYAGE DE LA BASE DE CONNAISSANCES")
    print("="*60)
    
    # Afficher l'état actuel
    cursor.execute('SELECT COUNT(*) FROM knowledge')
    total_before = cursor.fetchone()[0]
    print(f"\n📊 État actuel: {total_before} connaissances\n")
    
    # Afficher toutes les connaissances
    print("📚 Connaissances actuelles:\n")
    cursor.execute('SELECT id, question, answer, category FROM knowledge ORDER BY id')
    all_knowledge = cursor.fetchall()
    for row in all_knowledge:
        print(f"  ID {row[0]}: {row[1][:50]}... → {row[2][:50]}... ({row[3]})")
    
    print("\n" + "="*60)
    print("🔍 ANALYSE DES CONNAISSANCES À SUPPRIMER")
    print("="*60 + "\n")
    
    # Liste des suppressions à effectuer
    deletions = []
    
    # 1. Salutations simples
    cursor.execute("""
        SELECT id, question FROM knowledge 
        WHERE LOWER(TRIM(question)) IN ('bonjour', 'salut', 'hello', 'bonsoir', 'hey', 'coucou', 'hi', 'bsr')
    """)
    greetings = cursor.fetchall()
    if greetings:
        print(f"❌ Salutations simples ({len(greetings)}):")
        for g in greetings:
            print(f"   - ID {g[0]}: {g[1]}")
        deletions.append(("salutations", len(greetings), 
                         "DELETE FROM know