"""
Service de génération d'images avec DALL-E (OpenAI)
"""

import os
import requests

# Import OpenAI avec gestion d'erreur
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Module openai non disponible: {e}")
    OPENAI_AVAILABLE = False
    OpenAI = None

class ImageGenerator:
    def __init__(self):
        self.api_key = os.environ.get('CLE_API_OPENAI')
        self.enabled = bool(self.api_key) and OPENAI_AVAILABLE
        
        if not OPENAI_AVAILABLE:
            print("⚠️ Générateur d'images: Module openai non installé")
            return
        
        if self.enabled:
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("✓ Générateur d'images DALL-E activé")
            except Exception as e:
                print(f"⚠️ Erreur initialisation OpenAI: {e}")
                self.enabled = False
        else:
            print("⚠️ Générateur d'images: Clé API OpenAI manquante")
    
    def generate_image(self, prompt, size="1024x1024", quality="standard", n=1):
        """
        Génère une image avec DALL-E
        
        Args:
            prompt (str): Description de l'image à générer
            size (str): Taille de l'image ("1024x1024", "1792x1024", "1024x1792")
            quality (str): Qualité ("standard" ou "hd")
            n (int): Nombre d'images à générer (1-10)
        
        Returns:
            dict: {
                'success': bool,
                'images': [{'url': str, 'revised_prompt': str}],
                'error': str (si échec)
            }
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'Service de génération d\'images non disponible (clé API manquante)'
            }
        
        try:
            # Valider la taille
            valid_sizes = ["1024x1024", "1792x1024", "1024x1792"]
            if size not in valid_sizes:
                size = "1024x1024"
            
            # Valider la qualité
            if quality not in ["standard", "hd"]:
                quality = "standard"
            
            # Limiter le nombre d'images
            n = max(1, min(n, 10))
            
            print(f"🎨 Génération d'image: '{prompt[:50]}...' (taille: {size}, qualité: {quality})")
            
            # Appel à l'API DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1  # DALL-E 3 ne supporte qu'une image à la fois
            )
            
            # Extraire les résultats
            images = []
            for image_data in response.data:
                images.append({
                    'url': image_data.url,
                    'revised_prompt': getattr(image_data, 'revised_prompt', prompt)
                })
            
            print(f"✓ Image générée avec succès")
            
            return {
                'success': True,
                'images': images,
                'model': 'dall-e-3',
                'size': size,
                'quality': quality
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Erreur génération d'image: {error_msg}")
            
            return {
                'success': False,
                'error': error_msg
            }
    
    def detect_image_request(self, message):
        """
        Détecte si le message demande la génération d'une image
        
        Args:
            message (str): Message de l'utilisateur
        
        Returns:
            dict: {
                'is_request': bool,
                'prompt': str (si détecté),
                'size': str,
                'quality': str
            }
        """
        message_lower = message.lower()
        
        # Logs de debug
        print(f"🔍 Détection génération d'image pour: '{message[:50]}...'")
        
        # Mots-clés de génération d'images
        keywords = [
            'génère', 'génerer', 'genere', 'generer', 'générer',
            'créer', 'creer', 'créé', 'cree',
            'dessine', 'dessiner', 'dessiné',
            'illustre', 'illustrer', 'illustré',
            'image de', 'photo de', 'dessin de', 'illustration de',
            'montre moi', 'montre-moi', 'fais moi', 'fais-moi',
            'peux-tu créer', 'peux-tu générer', 'peux tu créer', 'peux tu générer',
            'je veux une image', 'je veux un dessin', 'je veux une photo',
            'crée moi', 'cree moi', 'génère moi', 'genere moi'
        ]
        
        # Vérifier si le message contient un mot-clé
        is_request = any(keyword in message_lower for keyword in keywords)
        
        print(f"   → Détection: {is_request}")
        if is_request:
            matched_keywords = [kw for kw in keywords if kw in message_lower]
            print(f"   → Mots-clés trouvés: {matched_keywords}")
        
        if not is_request:
            return {'is_request': False}
        
        # Extraire le prompt (enlever les mots-clés)
        prompt = message
        for keyword in keywords:
            if keyword in message_lower:
                # Enlever le mot-clé et ce qui vient avant
                parts = message_lower.split(keyword, 1)
                if len(parts) > 1:
                    prompt_part = parts[1].strip()
                    # Enlever les mots de liaison courants
                    linking_words = ['une', 'un', 'le', 'la', 'les', 'du', 'de', 'd\'', 'moi', 'me']
                    words = prompt_part.split()
                    # Enlever les mots de liaison au début
                    while words and words[0] in linking_words:
                        words.pop(0)
                    prompt = ' '.join(words) if words else message
                break
        
        # Si le prompt est vide ou trop court, utiliser le message original
        if len(prompt.strip()) < 3:
            prompt = message
        
        # Détecter la taille demandée
        size = "1024x1024"  # Par défaut
        if "grand" in message_lower or "large" in message_lower:
            size = "1792x1024"
        elif "portrait" in message_lower or "vertical" in message_lower:
            size = "1024x1792"
        
        # Détecter la qualité demandée
        quality = "standard"
        if "hd" in message_lower or "haute qualité" in message_lower or "haute définition" in message_lower:
            quality = "hd"
        
        return {
            'is_request': True,
            'prompt': prompt,
            'size': size,
            'quality': quality
        }

# Instance globale
image_generator = ImageGenerator()
