"""
Test des variables d'environnement sur Render
À exécuter pour vérifier la configuration
"""

import os
import sys

print("\n" + "="*60)
print("  TEST VARIABLES D'ENVIRONNEMENT")
print("="*60 + "\n")

# Vérifier les variables
variables = {
    'SECRET_KEY': os.environ.get('SECRET_KEY', ''),
    'SENDGRID_API_KEY': os.environ.get('SENDGRID_API_KEY', ''),
    'SENDGRID_FROM_EMAIL': os.environ.get('SENDGRID_FROM_EMAIL', ''),
}

for key, value in variables.items():
    if value:
        # Masquer les valeurs sensibles
        if len(value) > 10:
            display_value = value[:10] + "..." + value[-5:]
        else:
            display_value = value
        print(f"✅ {key}: {display_value}")
    else:
        print(f"❌ {key}: NON DÉFINI")

print("\n" + "="*60)

# Test du service email
print("\n  TEST SERVICE EMAIL")
print("="*60 + "\n")

sys.path.insert(0, 'src')

try:
    from email_service import email_service
    
    print(f"Provider: {email_service.provider}")
    print(f"Email expéditeur: {email_service.sender_email}")
    print(f"Disponible: {email_service.is_available()}")
    
    if email_service.is_available():
        print("\n✅ Service email configuré correctement!")
    else:
        print("\n❌ Service email NON configuré")
        print("\nVérifiez que vous avez:")
        print("1. SENDGRID_API_KEY défini")
        print("2. SENDGRID_FROM_EMAIL défini")
        print("3. Email vérifié dans SendGrid")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*60 + "\n")
