"""
Service de recherche avancée utilisant OpenAI
Permet des analyses approfondies sur n'importe quel sujet
"""

import os
import requests
from datetime import datetime

class AdvancedSearchService:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"  # Modèle économique et performant
        
        if not self.api_key:
            print("⚠️ OPENAI_API_KEY non configurée - Recherche avancée désactivée")
        else:
            print("✓ Service de recherche avancée OpenAI i