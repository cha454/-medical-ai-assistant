"""
Module d'intégration LLM pour réponses ultra-intelligentes
Supporte: OpenAI GPT, Anthropic Claude, Groq (gratuit), HuggingFace (gratuit)
"""

import os
import json
import requests
from datetime import datetime

class LLMProvider:
    def __init__(self):
        # Clés API (à configurer dans les variables d'environnement)
        self.google_key = os.environ.get('GOOGLE_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        self.groq_key = os.environ.get('GROQ_API_KEY')
        self.huggingface_key = os.environ.get('HUGGINGFACE_API_KEY')
        
        # Provider actif (par ordre de préférence)
        self.active_provider = self._detect_provider()
        
        # Prompt système médical
        self.system_prompt = """Tu es un assistant IA intelligent, empathique et conversationnel.

TES CAPACITÉS:
1. Tu peux répondre à TOUTES les questions (médicales, générales, techniques, etc.)
2. Tu as accès à des informations web à jour et vérifiées
3. Tu dialogues naturellement avec l'utilisateur
4. Tu es précis, factuel et tu cites tes sources

POUR LES QUESTIONS MÉDICALES:
1. Tu fournis des informations médicales générales à but éducatif UNIQUEMENT
2. Tu ne poses JAMAIS de diagnostic - seul un médecin peut le faire
3. Tu recommandes TOUJOURS de consulter un professionnel de santé
4. En cas d'urgence, tu diriges vers le 15 (SAMU) ou 112
5. Tu es empathique et rassurant, mais honnête sur tes limites
6. Tu cites tes sources (OMS, études médicales, sites fiables)

POUR LES QUESTIONS GÉNÉRALES:
1. Tu réponds de manière conversationnelle et naturelle
2. Tu utilises les informations web fournies pour être à jour
3. Tu es précis et factuel
4. Tu cites tes sources quand pertinent

FORMAT DE RÉPONSE:
- Utilise des emojis pour rendre la lecture agréable
- Structure tes réponses avec des titres et listes si nécessaire
- Sois concis mais complet
- Adapte ton langage au niveau de l'utilisateur
- Termine par une question de suivi ou une ouverture au dialogue

CONTEXTE: Tu es l'assistant IA du site "Assistant Médical IA" mais tu peux discuter de tout.
DATE ACTUELLE: {date}
"""
        
        print(f"✓ LLM Provider initialisé: {self.active_provider or 'Aucun (mode basique)'}")
    
    def _detect_provider(self):
        """Détecte le provider disponible"""
        if self.google_key:
            return "google"
        elif self.openai_key:
            return "openai"
        elif self.anthropic_key:
            return "anthropic"
        elif self.groq_key:
            return "groq"
        elif self.huggingface_key:
            return "huggingface"
        return None
    
    def is_available(self):
        """Vérifie si un LLM est disponible"""
        return self.active_provider is not None
    
    def generate_response(self, user_message, conversation_history=None, language="fr"):
        """Génère une réponse avec le LLM actif"""
        
        if not self.is_available():
            return None
        
        # Préparer le contexte
        system = self.system_prompt.format(date=datetime.now().strftime("%d/%m/%Y"))
        
        # Ajouter la langue
        if language == "en":
            system += "\nRéponds en ANGLAIS."
        elif language == "es":
            system += "\nRéponds en ESPAGNOL."
        else:
            system += "\nRéponds en FRANÇAIS."
        
        # Construire les messages
        messages = [{"role": "system", "content": system}]
        
        # Ajouter l'historique de conversation (derniers 10 messages)
        if conversation_history:
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        # Ajouter le message actuel
        messages.append({"role": "user", "content": user_message})
        
        # Appeler le provider approprié
        try:
            if self.active_provider == "google":
                return self._call_google(messages)
            elif self.active_provider == "openai":
                return self._call_openai(messages)
            elif self.active_provider == "anthropic":
                return self._call_anthropic(messages, system)
            elif self.active_provider == "groq":
                return self._call_groq(messages)
            elif self.active_provider == "huggingface":
                return self._call_huggingface(user_message, system)
        except Exception as e:
            print(f"Erreur LLM ({self.active_provider}): {e}")
            return None
        
        return None
    
    def _call_google(self, messages):
        """Appel à l'API Google Gemini"""
        # Liste des modèles à essayer dans l'ordre
        models_to_try = [
            ("v1beta/models/gemini-pro", "gemini-pro"),
            ("v1beta/models/gemini-1.5-pro-latest", "gemini-1.5-pro-latest"),
            ("v1/models/gemini-pro", "gemini-pro v1"),
        ]
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Convertir les messages au format Gemini
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                # Gemini n'a pas de rôle system, on l'ajoute comme premier message user
                contents.append({
                    "role": "user",
                    "parts": [{"text": msg["content"]}]
                })
            elif msg["role"] == "user":
                contents.append({
                    "role": "user",
                    "parts": [{"text": msg["content"]}]
                })
            elif msg["role"] == "assistant":
                contents.append({
                    "role": "model",
                    "parts": [{"text": msg["content"]}]
                })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1500
            }
        }
        
        # Essayer chaque modèle jusqu'à ce qu'un fonctionne
        for endpoint, model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/{endpoint}:generateContent?key={self.google_key}"
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        # Vérifier si le contenu a été bloqué
                        if "content" in candidate and "parts" in candidate["content"]:
                            print(f"✓ Google Gemini ({model_name}): Réponse reçue")
                            return candidate["content"]["parts"][0]["text"]
                        else:
                            print(f"⚠️ Google Gemini ({model_name}): Contenu bloqué - {result}")
                    else:
                        print(f"⚠️ Google Gemini ({model_name}): Pas de candidats - {result}")
                elif response.status_code == 404:
                    print(f"⚠️ Google Gemini ({model_name}): Modèle non trouvé, essai suivant...")
                    continue  # Essayer le modèle suivant
                else:
                    print(f"❌ Google Gemini ({model_name}) Error: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"❌ Google Gemini ({model_name}) Exception: {e}")
                continue
        
        print("❌ Tous les modèles Google Gemini ont échoué")
        return None
    
    def _call_openai(self, messages):
        """Appel à l'API OpenAI"""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",  # Modèle économique et performant
            "messages": messages,
            "max_tokens": 1500,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"OpenAI Error: {response.status_code} - {response.text}")
            return None
    
    def _call_anthropic(self, messages, system):
        """Appel à l'API Anthropic Claude"""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        # Convertir le format des messages pour Claude
        claude_messages = []
        for msg in messages:
            if msg["role"] != "system":
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        data = {
            "model": "claude-3-haiku-20240307",  # Modèle rapide et économique
            "max_tokens": 1500,
            "system": system,
            "messages": claude_messages
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["content"][0]["text"]
        else:
            print(f"Anthropic Error: {response.status_code} - {response.text}")
            return None
    
    def _call_groq(self, messages):
        """Appel à l'API Groq (gratuit et rapide)"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",  # Nouveau modèle recommandé
            "messages": messages,
            "max_tokens": 1500,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Groq Error: {response.status_code} - {response.text}")
            return None
    
    def _call_huggingface(self, user_message, system):
        """Appel à l'API HuggingFace (gratuit)"""
        url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {
            "Authorization": f"Bearer {self.huggingface_key}",
            "Content-Type": "application/json"
        }
        
        # Format pour Mistral
        prompt = f"<s>[INST] {system}\n\nQuestion de l'utilisateur: {user_message} [/INST]"
        
        data = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
        else:
            print(f"HuggingFace Error: {response.status_code} - {response.text}")
        return None
    
    def get_provider_info(self):
        """Retourne les informations sur le provider actif"""
        providers_info = {
            "google": {
                "name": "Google Gemini",
                "model": "gemini-1.5-flash",
                "quality": "Excellent",
                "speed": "Très rapide",
                "cost": "Gratuit"
            },
            "openai": {
                "name": "OpenAI GPT-4",
                "model": "gpt-4o-mini",
                "quality": "Excellent",
                "speed": "Rapide",
                "cost": "Payant"
            },
            "anthropic": {
                "name": "Anthropic Claude",
                "model": "claude-3-haiku",
                "quality": "Excellent",
                "speed": "Rapide",
                "cost": "Payant"
            },
            "groq": {
                "name": "Groq (Llama 3.1)",
                "model": "llama-3.1-70b-versatile",
                "quality": "Très bon",
                "speed": "Très rapide",
                "cost": "Gratuit"
            },
            "huggingface": {
                "name": "HuggingFace (Mistral)",
                "model": "Mistral-7B-Instruct",
                "quality": "Bon",
                "speed": "Moyen",
                "cost": "Gratuit"
            }
        }
        
        if self.active_provider:
            return providers_info.get(self.active_provider, {})
        return {"name": "Mode basique (sans LLM)", "quality": "Limité"}

# Instance globale
llm = LLMProvider()

# Test
if __name__ == "__main__":
    print(f"Provider actif: {llm.active_provider}")
    print(f"LLM disponible: {llm.is_available()}")
    print(f"Info: {llm.get_provider_info()}")
    
    if llm.is_available():
        response = llm.generate_response("Quels sont les symptômes de la grippe?")
        print(f"\nRéponse:\n{response}")
