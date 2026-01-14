"""
Script de test SendGrid - Basé sur la documentation officielle
Teste l'envoi d'email avec SendGrid API
"""

import os
import sys

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Importer SendGrid
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    print("✅ Module SendGrid importé avec succès")
except ImportError:
    print("❌ Module SendGrid non trouvé")
    print("💡 Installez-le avec: pip install sendgrid")
    sys.exit(1)

def test_sendgrid_configuration():
    """Teste la configuration SendGrid"""
    print("\n" + "="*60)
    print("  TEST DE CONFIGURATION SENDGRID")
    print("="*60 + "\n")
    
    # 1. Vérifier la clé API
    api_key = os.environ.get('SENDGRID_API_KEY', '')
    if not api_key:
        print("❌ SENDGRID_API_KEY non trouvée")
        print("💡 Ajoutez-la dans votre fichier .env ou sur Render")
        return False
    
    print(f"✅ SENDGRID_API_KEY trouvée (commence par: {api_key[:10]}...)")
    
    # 2. Vérifier l'email expéditeur
    from_email = os.environ.get('SENDGRID_FROM_EMAIL', '')
    if not from_email:
        print("❌ SENDGRID_FROM_EMAIL non trouvée")
        print("💡 Ajoutez-la dans votre fichier .env ou sur Render")
        print("💡 Utilisez un email vérifié dans SendGrid")
        return False
    
    print(f"✅ SENDGRID_FROM_EMAIL trouvée: {from_email}")
    
    return True

def send_test_email(to_email):
    """Envoie un email de test"""
    print("\n" + "="*60)
    print("  ENVOI D'EMAIL DE TEST")
    print("="*60 + "\n")
    
    api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = os.environ.get('SENDGRID_FROM_EMAIL')
    
    # Créer le message (code officiel SendGrid)
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='Test SendGrid - Assistant Medical IA',
        plain_text_content=f'''Bonjour,

Ceci est un email de test depuis l'Assistant Medical IA.

Si vous recevez cet email, cela signifie que SendGrid est correctement configuré ! 🎉

Configuration:
- Email expéditeur: {from_email}
- Email destinataire: {to_email}
- Provider: SendGrid API

---
Assistant Medical IA
https://medical-ai-assistant-2k1a.onrender.com/
'''
    )
    
    try:
        # Envoyer l'email
        sg = SendGridAPIClient(api_key)
        print(f"📧 Envoi de l'email à {to_email}...")
        response = sg.send(message)
        
        # Vérifier la réponse
        if response.status_code in [200, 201, 202]:
            print(f"✅ Email envoyé avec succès !")
            print(f"📊 Code de statut: {response.status_code}")
            print(f"📬 Vérifiez votre boîte email: {to_email}")
            return True
        else:
            print(f"⚠️ Réponse inattendue: {response.status_code}")
            print(f"📄 Body: {response.body}")
            return False
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur lors de l'envoi: {error_msg}")
        
        # Messages d'aide selon l'erreur
        if "does not contain a valid address" in error_msg or "Sender" in error_msg:
            print("\n💡 SOLUTION:")
            print("   1. Allez sur: https://app.sendgrid.com/settings/sender_auth/senders")
            print("   2. Vérifiez que votre email a le statut 'Verified' ✅")
            print(f"   3. L'email dans SENDGRID_FROM_EMAIL ({from_email}) doit être vérifié")
            
        elif "API key" in error_msg or "Unauthorized" in error_msg:
            print("\n💡 SOLUTION:")
            print("   1. Allez sur: https://app.sendgrid.com/settings/api_keys")
            print("   2. Créez une nouvelle clé API")
            print("   3. Mettez-la dans SENDGRID_API_KEY")
            
        return False

def main():
    """Fonction principale"""
    print("\n" + "🏥 "*20)
    print("   TEST SENDGRID - ASSISTANT MEDICAL IA")
    print("🏥 "*20)
    
    # Test 1: Configuration
    if not test_sendgrid_configuration():
        print("\n❌ Configuration incomplète")
        print("\n📖 Consultez: CONFIGURER_SENDGRID.md")
        return
    
    # Test 2: Demander l'email de test
    print("\n" + "="*60)
    print("  EMAIL DE TEST")
    print("="*60 + "\n")
    
    to_email = input("📧 Entrez l'email de test (ex: noir1777@gmail.com): ").strip()
    
    if not to_email or '@' not in to_email:
        print("❌ Email invalide")
        return
    
    # Test 3: Envoyer l'email
    success = send_test_email(to_email)
    
    # Résumé
    print("\n" + "="*60)
    print("  RÉSUMÉ")
    print("="*60 + "\n")
    
    if success:
        print("🎉 TEST RÉUSSI !")
        print(f"✅ Email envoyé à {to_email}")
        print("📬 Vérifiez votre boîte de réception")
        print("\n💡 Vous pouvez maintenant utiliser l'envoi d'email dans votre app !")
    else:
        print("❌ TEST ÉCHOUÉ")
        print("\n📖 Guides disponibles:")
        print("   • RENDER_SENDGRID_QUICK_FIX.md - Fix rapide")
        print("   • CONFIGURER_SENDGRID.md - Guide complet")
        print("   • SOLUTION_EMAIL.txt - Résumé visuel")
    
    print("\n")

if __name__ == "__main__":
    main()
