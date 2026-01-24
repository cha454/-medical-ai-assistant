#!/usr/bin/env python3
"""
Script de gestion de la base de connaissances
Permet de nettoyer, exporter, importer et gérer les connaissances
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from knowledge_base import KnowledgeBase
import sqlite3
from datetime import datetime

def print_header(title):
    """Affiche un en-tête formaté"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def print_info(message):
    """Affiche un message d'information"""
    print(f"ℹ️  {message}")

def print_warning(message):
    """Affiche un avertissement"""
    print(f"⚠️  {message}")

def show_statistics(kb):
    """Affiche les statistiques de la base de connaissances"""
    print_header("📊 Statistiques de la Base de Connaissances")
    
    stats = kb.get_statistics()
    
    print(f"📚 Total de connaissances: {stats['total']}")
    print(f"📅 Dernière mise à jour: {stats['last_update'] or 'Jamais'}")
    
    if stats['by_category']:
        print("\n📁 Par catégorie:")
        for category, count in stats['by_category'].items():
            print(f"   • {category}: {count}")
    
    if stats['by_language']:
        print("\n🌍 Par langue:")
        for language, count in stats['by_language'].items():
            print(f"   • {language}: {count}")
    
    print()

def list_all_knowledge(kb):
    """Liste toutes les connaissances"""
    print_header("📚 Liste de Toutes les Connaissances")
    
    knowledge = kb.get_all_knowledge(limit=1000)
    
    if not knowledge:
        print_warning("Aucune connaissance trouvée")
        return
    
    for k in knowledge:
        print(f"\n🆔 ID: {k['id']}")
        print(f"📁 Catégorie: {k['category']}")
        print(f"❓ Question: {k['question']}")
        print(f"💡 Réponse: {k['answer'][:100]}{'...' if len(k['answer']) > 100 else ''}")
        print(f"🌍 Langue: {k['language']}")
        print(f"📊 Utilisations: {k['usage_count']}")
        print(f"📅 Créé le: {k['date_created']}")
        print("-" * 60)

def search_knowledge(kb, query):
    """Recherche des connaissances"""
    print_header(f"🔍 Recherche: '{query}'")
    
    results = kb.search_knowledge(query, limit=50)
    
    if not results:
        print_warning(f"Aucune connaissance trouvée pour '{query}'")
        return
    
    print_success(f"{len(results)} résultat(s) trouvé(s)")
    
    for r in results:
        print(f"\n🆔 ID: {r['id']}")
        print(f"📁 Catégorie: {r['category']}")
        print(f"❓ Question: {r['question']}")
        print(f"💡 Réponse: {r['answer']}")
        print(f"🌍 Langue: {r['language']}")
        print("-" * 60)

def delete_knowledge(kb, knowledge_id):
    """Supprime une connaissance"""
    print_header(f"🗑️  Suppression de la Connaissance #{knowledge_id}")
    
    try:
        kb.delete_knowledge(knowledge_id)
        print_success(f"Connaissance #{knowledge_id} supprimée avec succès")
    except Exception as e:
        print_error(f"Erreur lors de la suppression: {e}")

def clear_all_knowledge(kb):
    """Supprime TOUTES les connaissances"""
    print_header("⚠️  SUPPRESSION TOTALE DE LA BASE DE CONNAISSANCES")
    
    stats = kb.get_statistics()
    total = stats['total']
    
    if total == 0:
        print_info("La base de connaissances est déjà vide")
        return
    
    print_warning(f"Vous êtes sur le point de supprimer {total} connaissance(s)")
    print_warning("Cette action est IRRÉVERSIBLE !")
    
    confirmation = input("\n❓ Tapez 'OUI' en majuscules pour confirmer: ")
    
    if confirmation != "OUI":
        print_info("Suppression annulée")
        return
    
    try:
        conn = sqlite3.connect(kb.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM knowledge')
        conn.commit()
        conn.close()
        
        print_success(f"✅ {total} connaissance(s) supprimée(s) avec succès")
        print_info("La base de connaissances est maintenant vide")
    except Exception as e:
        print_error(f"Erreur lors de la suppression: {e}")

def export_knowledge(kb, filepath=None):
    """Exporte les connaissances en JSON"""
    if not filepath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"knowledge_export_{timestamp}.json"
    
    print_header(f"📤 Export des Connaissances")
    
    try:
        exported_file = kb.export_knowledge(filepath)
        stats = kb.get_statistics()
        print_success(f"{stats['total']} connaissance(s) exportée(s) vers: {exported_file}")
    except Exception as e:
        print_error(f"Erreur lors de l'export: {e}")

def import_knowledge(kb, filepath):
    """Importe des connaissances depuis un fichier JSON"""
    print_header(f"📥 Import des Connaissances depuis {filepath}")
    
    if not os.path.exists(filepath):
        print_error(f"Le fichier {filepath} n'existe pas")
        return
    
    try:
        imported = kb.import_knowledge(filepath)
        print_success(f"{imported} connaissance(s) importée(s) avec succès")
    except Exception as e:
        print_error(f"Erreur lors de l'import: {e}")

def delete_by_category(kb, category):
    """Supprime toutes les connaissances d'une catégorie"""
    print_header(f"🗑️  Suppression par Catégorie: {category}")
    
    try:
        conn = sqlite3.connect(kb.db_path)
        cursor = conn.cursor()
        
        # Compter d'abord
        cursor.execute('SELECT COUNT(*) FROM knowledge WHERE category = ?', (category,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            print_warning(f"Aucune connaissance trouvée dans la catégorie '{category}'")
            conn.close()
            return
        
        print_warning(f"Vous allez supprimer {count} connaissance(s) de la catégorie '{category}'")
        confirmation = input("\n❓ Tapez 'OUI' pour confirmer: ")
        
        if confirmation != "OUI":
            print_info("Suppression annulée")
            conn.close()
            return
        
        cursor.execute('DELETE FROM knowledge WHERE category = ?', (category,))
        conn.commit()
        conn.close()
        
        print_success(f"{count} connaissance(s) supprimée(s) de la catégorie '{category}'")
    except Exception as e:
        print_error(f"Erreur: {e}")

def show_menu():
    """Affiche le menu principal"""
    print_header("🎓 Gestionnaire de Base de Connaissances")
    print("1. 📊 Afficher les statistiques")
    print("2. 📚 Lister toutes les connaissances")
    print("3. 🔍 Rechercher des connaissances")
    print("4. 🗑️  Supprimer une connaissance (par ID)")
    print("5. 🗑️  Supprimer par catégorie")
    print("6. ⚠️  Supprimer TOUTES les connaissances")
    print("7. 📤 Exporter les connaissances (JSON)")
    print("8. 📥 Importer des connaissances (JSON)")
    print("9. ❌ Quitter")
    print()

def main():
    """Fonction principale"""
    # Initialiser la base de connaissances
    kb = KnowledgeBase()
    
    # Mode interactif si aucun argument
    if len(sys.argv) == 1:
        while True:
            show_menu()
            choice = input("👉 Votre choix: ").strip()
            
            if choice == "1":
                show_statistics(kb)
            elif choice == "2":
                list_all_knowledge(kb)
            elif choice == "3":
                query = input("\n🔍 Entrez votre recherche: ").strip()
                if query:
                    search_knowledge(kb, query)
            elif choice == "4":
                try:
                    kid = int(input("\n🆔 Entrez l'ID de la connaissance à supprimer: ").strip())
                    delete_knowledge(kb, kid)
                except ValueError:
                    print_error("ID invalide")
            elif choice == "5":
                category = input("\n📁 Entrez la catégorie à supprimer: ").strip()
                if category:
                    delete_by_category(kb, category)
            elif choice == "6":
                clear_all_knowledge(kb)
            elif choice == "7":
                filepath = input("\n📤 Nom du fichier (laisser vide pour auto): ").strip()
                export_knowledge(kb, filepath if filepath else None)
            elif choice == "8":
                filepath = input("\n📥 Chemin du fichier JSON: ").strip()
                if filepath:
                    import_knowledge(kb, filepath)
            elif choice == "9":
                print_info("Au revoir ! 👋")
                break
            else:
                print_error("Choix invalide")
            
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
    
    # Mode ligne de commande
    else:
        command = sys.argv[1]
        
        if command == "stats":
            show_statistics(kb)
        
        elif command == "list":
            list_all_knowledge(kb)
        
        elif command == "search":
            if len(sys.argv) < 3:
                print_error("Usage: python manage_knowledge.py search <query>")
                sys.exit(1)
            query = " ".join(sys.argv[2:])
            search_knowledge(kb, query)
        
        elif command == "delete":
            if len(sys.argv) < 3:
                print_error("Usage: python manage_knowledge.py delete <id>")
                sys.exit(1)
            try:
                kid = int(sys.argv[2])
                delete_knowledge(kb, kid)
            except ValueError:
                print_error("ID invalide")
                sys.exit(1)
        
        elif command == "clear":
            clear_all_knowledge(kb)
        
        elif command == "export":
            filepath = sys.argv[2] if len(sys.argv) > 2 else None
            export_knowledge(kb, filepath)
        
        elif command == "import":
            if len(sys.argv) < 3:
                print_error("Usage: python manage_knowledge.py import <filepath>")
                sys.exit(1)
            import_knowledge(kb, sys.argv[2])
        
        elif command == "delete-category":
            if len(sys.argv) < 3:
                print_error("Usage: python manage_knowledge.py delete-category <category>")
                sys.exit(1)
            delete_by_category(kb, sys.argv[2])
        
        else:
            print_error(f"Commande inconnue: {command}")
            print_info("\nCommandes disponibles:")
            print("  stats              - Afficher les statistiques")
            print("  list               - Lister toutes les connaissances")
            print("  search <query>     - Rechercher des connaissances")
            print("  delete <id>        - Supprimer une connaissance")
            print("  delete-category <cat> - Supprimer par catégorie")
            print("  clear              - Supprimer TOUTES les connaissances")
            print("  export [file]      - Exporter en JSON")
            print("  import <file>      - Importer depuis JSON")
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
