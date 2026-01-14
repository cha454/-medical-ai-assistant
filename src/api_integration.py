"""
Module d'intégration centralisé pour toutes les APIs externes
Gère: LLM, Email, Recherche Web, et autres services
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class APIIntegration:
    """Gestionnaire centralisé pour toutes les intégrations API"""
    
    def __init__(self):
        self.services = {}
        self.initialize_services()
    
    def initialize_services(self):
        """Initialise tous les services disponibles"""
        
        # 1. Service LLM
        try:
            from llm_provider import llm
            if llm and llm.is_available():
                self.services['llm'] = {
                    'instance': llm,
                    'status': 'active',
                    'provider': llm.get_provider_info().get('name', 'Unknown')
                }
                print(f"✓ LLM: {self.services['llm']['provider']} activé")
            else:
                self.services['llm'] = {'status': 'unavailable'}
                print("⚠️ LLM: Non configuré")
        except Exception as e:
            self.services['llm'] = {'status': 'error', 'error': str(e)}
            print(f"⚠️ LLM: Erreur - {e}")
        
        # 2. Service Email
        try:
            from email_service import email_service
            if email_service.is_available():
                self.services['email'] = {
                    'instance': email_service,
                    'status': 'active',
                    'provider': email_service.provider
                }
                print(f"✓ Email: {email_service.provider} activé")
            else:
                self.services['email'] = {'status': 'unavailable'}
                print("⚠️ Email: Non configuré")
        except Exception as e:
            self.services['email'] = {'status': 'error', 'error': str(e)}
            print(f"⚠️ Email: Erreur - {e}")
        
        # 3. Service Recherche Web
        try:
            from web_search import web_search
            self.services['web_search'] = {
                'instance': web_search,
                'status': 'active'
            }
            print("✓ Recherche Web: Activé")
        except Exception as e:
            self.services['web_search'] = {'status': 'error', 'error': str(e)}
            print(f"⚠️ Recherche Web: Erreur - {e}")
        
        # 4. Service Analyse d'Images
        try:
            from image_analyzer import analyzer
            self.services['image_analyzer'] = {
                'instance': analyzer,
                'status': 'active'
            }
            print("✓ Analyse d'Images: Activé")
        except Exception as e:
            self.services['image_analyzer'] = {'status': 'unavailable'}
            print("⚠️ Analyse d'Images: Non disponible")
    
    def get_service_status(self) -> Dict[str, Any]:
        """Retourne le statut de tous les services"""
        status = {}
        for service_name, service_info in self.services.items():
            status[service_name] = {
                'status': service_info.get('status', 'unknown'),
                'provider': service_info.get('provider', 'N/A')
            }
            if 'error' in service_info:
                status[service_name]['error'] = service_info['error']
        return status
    
    # === LLM METHODS ===
    
    def generate_llm_response(self, prompt: str, context: Optional[str] = None, 
                             language: str = "fr") -> Dict[str, Any]:
        """Génère une réponse avec le LLM"""
        if 'llm' not in self.services or self.services['llm']['status'] != 'active':
            return {
                'success': False,
                'error': 'LLM non disponible',
                'fallback': True
            }
        
        try:
            llm = self.services['llm']['instance']
            response = llm.generate_response(prompt, context, language)
            return {
                'success': True,
                'response': response,
                'provider': self.services['llm']['provider']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback': True
            }
    
    def chat_with_llm(self, message: str, conversation_history: List[Dict] = None,
                     language: str = "fr") -> Dict[str, Any]:
        """Chat conversationnel avec le LLM"""
        if 'llm' not in self.services or self.services['llm']['status'] != 'active':
            return {
                'success': False,
                'error': 'LLM non disponible'
            }
        
        try:
            llm = self.services['llm']['instance']
            response = llm.chat(message, conversation_history or [], language)
            return {
                'success': True,
                'response': response,
                'provider': self.services['llm']['provider']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # === EMAIL METHODS ===
    
    def send_email(self, to_email: str, subject: str, body: str) -> Dict[str, Any]:
        """Envoie un email"""
        if 'email' not in self.services or self.services['email']['status'] != 'active':
            return {
                'success': False,
                'error': 'Service email non disponible'
            }
        
        try:
            email_service = self.services['email']['instance']
            result = email_service.send_email(to_email, subject, body)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_consultation_summary(self, to_email: str, conversation_history: List[Dict],
                                 symptoms: Optional[List[str]] = None) -> Dict[str, Any]:
        """Envoie un résumé de consultation par email"""
        if 'email' not in self.services or self.services['email']['status'] != 'active':
            return {
                'success': False,
                'error': 'Service email non disponible'
            }
        
        try:
            email_service = self.services['email']['instance']
            result = email_service.send_conversation_summary(
                to_email, 
                conversation_history, 
                symptoms
            )
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # === WEB SEARCH METHODS ===
    
    def search_medical_info(self, query: str, language: str = "fr") -> Dict[str, Any]:
        """Recherche des informations médicales sur le web"""
        if 'web_search' not in self.services or self.services['web_search']['status'] != 'active':
            return {
                'success': False,
                'error': 'Service de recherche non disponible'
            }
        
        try:
            web_search = self.services['web_search']['instance']
            results = web_search.search_medical_info(query, language)
            return {
                'success': True,
                'results': results
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_and_format(self, query: str, language: str = "fr") -> Optional[str]:
        """Recherche et formate les résultats"""
        if 'web_search' not in self.services or self.services['web_search']['status'] != 'active':
            return None
        
        try:
            web_search = self.services['web_search']['instance']
            formatted = web_search.search_and_format(query, language)
            return formatted
        except Exception as e:
            print(f"Erreur recherche web: {e}")
            return None
    
    # === IMAGE ANALYSIS METHODS ===
    
    def analyze_medical_image(self, image_data: bytes) -> Dict[str, Any]:
        """Analyse une image médicale"""
        if 'image_analyzer' not in self.services or self.services['image_analyzer']['status'] != 'active':
            return {
                'success': False,
                'error': 'Service d\'analyse d\'images non disponible'
            }
        
        try:
            analyzer = self.services['image_analyzer']['instance']
            result = analyzer.analyze_image(image_data)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_image_from_base64(self, base64_string: str) -> Dict[str, Any]:
        """Analyse une image depuis une chaîne base64"""
        if 'image_analyzer' not in self.services or self.services['image_analyzer']['status'] != 'active':
            return {
                'success': False,
                'error': 'Service d\'analyse d\'images non disponible'
            }
        
        try:
            analyzer = self.services['image_analyzer']['instance']
            result = analyzer.analyze_image_from_base64(base64_string)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # === UTILITY METHODS ===
    
    def is_service_available(self, service_name: str) -> bool:
        """Vérifie si un service est disponible"""
        return (service_name in self.services and 
                self.services[service_name].get('status') == 'active')
    
    def get_available_services(self) -> List[str]:
        """Retourne la liste des services disponibles"""
        return [name for name, info in self.services.items() 
                if info.get('status') == 'active']
    
    def reload_services(self):
        """Recharge tous les services"""
        self.services = {}
        self.initialize_services()
    
    def get_integration_info(self) -> Dict[str, Any]:
        """Retourne les informations complètes sur les intégrations"""
        return {
            'timestamp': datetime.now().isoformat(),
            'services': self.get_service_status(),
            'available_services': self.get_available_services(),
            'total_services': len(self.services),
            'active_services': len(self.get_available_services())
        }


# Instance globale
api_integration = APIIntegration()


# === FONCTIONS HELPER ===

def get_api_status() -> Dict[str, Any]:
    """Retourne le statut de toutes les APIs"""
    return api_integration.get_service_status()


def is_llm_available() -> bool:
    """Vérifie si le LLM est disponible"""
    return api_integration.is_service_available('llm')


def is_email_available() -> bool:
    """Vérifie si le service email est disponible"""
    return api_integration.is_service_available('email')


def is_web_search_available() -> bool:
    """Vérifie si la recherche web est disponible"""
    return api_integration.is_service_available('web_search')


# Test du module
if __name__ == "__main__":
    print("=== Test API Integration ===\n")
    
    # Afficher le statut
    status = api_integration.get_service_status()
    print("Statut des services:")
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    print(f"\nServices disponibles: {api_integration.get_available_services()}")
    
    # Test recherche web
    if is_web_search_available():
        print("\n=== Test Recherche Web ===")
        result = api_integration.search_and_format("diabète", "fr")
        if result:
            print(result[:500])
    
    # Test LLM
    if is_llm_available():
        print("\n=== Test LLM ===")
        result = api_integration.generate_llm_response(
            "Explique les symptômes du diabète en 2 phrases",
            language="fr"
        )
        if result['success']:
            print(f"Réponse: {result['response']}")
