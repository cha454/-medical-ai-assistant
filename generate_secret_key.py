"""
Génère une SECRET_KEY sécurisée pour Flask
"""

import secrets

# Générer une clé secrète aléatoire
secret_key = secrets.token_hex(32)

print("\n" + "="*60)
print("  SECRET_KEY GÉNÉRÉE")
print("="*60)
print(f"\n{secret_key}\n")
print("="*60)
print("\nCopiez cette clé et ajoutez-la sur Render :")
print("\nKey:   SECRET_KEY")
print(f"Value: {secret_key}")
print("\n" + "="*60)
