"""
Service de conversion de devises pour l'assistant médical
Utilise l'API ExchangeRate-API (gratuite - 1500 requêtes/mois)
"""

import requests
import os
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class CurrencyService:
    def __init__(self):
        # API gratuite ExchangeRate-API (pas de clé requise pour le plan gratuit)
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"
        
        # Cache pour éviter trop de requêtes
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache de 1h
        
        # Codes de devises courants
        self.currencies = {
            "euro": "EUR", "euros": "EUR", "eur": "EUR", "€": "EUR",
            "dollar": "USD", "dollars": "USD", "usd": "USD", "$": "USD",
            "livre": "GBP", "livres": "GBP", "gbp": "GBP", "£": "GBP",
            "yen": "JPY", "yens": "JPY", "jpy": "JPY", "¥": "JPY",
            "franc": "CHF", "francs": "CHF", "chf": "CHF",
            "yuan": "CNY", "cny": "CNY",
            "dirham": "MAD", "dirhams": "MAD", "mad": "MAD",
            "fcfa": "XOF", "xof": "XOF",
            "cfa": "XAF", "xaf": "XAF"
        }
        
        # Noms complets des devises
        self.currency_names = {
            "EUR": "Euro",
            "USD": "Dollar américain",
            "GBP": "Livre sterling",
            "JPY": "Yen japonais",
            "CHF": "Franc suisse",
            "CNY": "Yuan chinois",
            "MAD": "Dirham marocain",
            "XOF": "Franc CFA (BCEAO)",
            "XAF": "Franc CFA (BEAC)"
        }
    
    def is_available(self) -> bool:
        """Vérifie si le service est disponible"""
        return True  # Pas de clé API requise
    
    def is_currency_request(self, text: str) -> bool:
        """Détecte si le message est une demande de conversion"""
        text_lower = text.lower()
        
        keywords = [
            "convertis", "convertir", "conversion", "change", "changer",
            "combien font", "combien vaut", "équivalent", "en devise",
            "taux de change", "cours", "devise"
        ]
        
        # Vérifier les mots-clés
        if any(keyword in text_lower for keyword in keywords):
            return True
        
        # Pattern: "100 USD en EUR"
        pattern = r'\d+\s*[a-zA-Z€$£¥]+\s+(?:en|to|vers)\s+[a-zA-Z€$£¥]+'
        if re.search(pattern, text_lower):
            return True
        
        return False
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Convertit un montant d'une devise à une autre"""
        try:
            # Normaliser les codes de devises
            from_code = self._normalize_currency(from_currency)
            to_code = self._normalize_currency(to_currency)
            
            if not from_code or not to_code:
                return {
                    "success": False,
                    "error": "Devise invalide",
                    "message": f"Je ne reconnais pas la devise '{from_currency}' ou '{to_currency}'."
                }
            
            # Obtenir le taux de change
            rate = self._get_exchange_rate(from_code, to_code)
            
            if rate is None:
                return {
                    "success": False,
                    "error": "Taux non disponible",
                    "message": "Je n'ai pas pu obtenir le taux de change."
                }
            
            # Calculer la conversion
            result = amount * rate
            
            return {
                "success": True,
                "amount": amount,
                "from_currency": from_code,
                "to_currency": to_code,
                "rate": rate,
                "result": result,
                "from_name": self.currency_names.get(from_code, from_code),
                "to_name": self.currency_names.get(to_code, to_code)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Erreur lors de la conversion : {str(e)}"
            }
    
    def parse_and_convert(self, text: str) -> Dict[str, Any]:
        """Parse le texte et effectue la conversion"""
        # Extraire le montant et les devises
        # Patterns: "100 USD en EUR", "convertis 50 euros en dollars"
        patterns = [
            r'(\d+(?:\.\d+)?)\s*([a-zA-Z€$£¥]+)\s+(?:en|to|vers)\s+([a-zA-Z€$£¥]+)',
            r'convertis?\s+(\d+(?:\.\d+)?)\s*([a-zA-Z€$£¥]+)\s+(?:en|to|vers)\s+([a-zA-Z€$£¥]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                amount = float(match.group(1))
                from_curr = match.group(2)
                to_curr = match.group(3)
                
                return self.convert(amount, from_curr, to_curr)
        
        return {
            "success": False,
            "error": "Format invalide",
            "message": "Je n'ai pas compris la demande de conversion."
        }
    
    def _normalize_currency(self, currency: str) -> Optional[str]:
        """Normalise le code de devise"""
        currency_lower = currency.lower().strip()
        
        # Vérifier dans le dictionnaire
        if currency_lower in self.currencies:
            return self.currencies[currency_lower]
        
        # Vérifier si c'est déjà un code valide
        currency_upper = currency.upper()
        if len(currency_upper) == 3 and currency_upper.isalpha():
            return currency_upper
        
        return None
    
    def _get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Obtient le taux de change"""
        # Vérifier le cache
        cache_key = f"{from_currency}_{to_currency}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['rate']
        
        try:
            # Appeler l'API
            url = f"{self.api_url}{from_currency}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                
                if to_currency in rates:
                    rate = rates[to_currency]
                    
                    # Mettre en cache
                    self.cache[cache_key] = {
                        'rate': rate,
                        'timestamp': datetime.now()
                    }
                    
                    return rate
            
            return None
            
        except Exception as e:
            print(f"Currency API Error: {e}")
            return None
    
    def format_response(self, conversion_result: Dict[str, Any], original_query: str) -> str:
        """Formate la réponse pour l'utilisateur"""
        if not conversion_result["success"]:
            return f"""💱 **Conversion de Devises**

❌ Je n'ai pas pu effectuer cette conversion.

**Raison :** {conversion_result.get('message', 'Erreur inconnue')}

**Exemples de conversions :**
• "Convertis 100 USD en EUR"
• "Combien font 50 euros en dollars ?"
• "1000 MAD en EUR"

**Devises supportées :**
EUR (€), USD ($), GBP (£), JPY (¥), CHF, CNY, MAD, XOF, XAF

Essaie de reformuler ta demande !"""
        
        amount = conversion_result["amount"]
        from_curr = conversion_result["from_currency"]
        to_curr = conversion_result["to_currency"]
        rate = conversion_result["rate"]
        result = conversion_result["result"]
        from_name = conversion_result["from_name"]
        to_name = conversion_result["to_name"]
        
        # Formater les montants
        amount_str = f"{amount:,.2f}".replace(",", " ")
        result_str = f"{result:,.2f}".replace(",", " ")
        rate_str = f"{rate:.4f}"
        
        return f"""💱 **Conversion de Devises**

**{amount_str} {from_curr}** = **{result_str} {to_curr}**

---

📊 **Détails :**
• Devise source : {from_name} ({from_curr})
• Devise cible : {to_name} ({to_curr})
• Taux de change : 1 {from_curr} = {rate_str} {to_curr}

📅 **Taux à jour** (mis à jour il y a moins d'1 heure)

---

💡 **Autres conversions :**
• "100 EUR en USD"
• "50 GBP en EUR"
• "1000 MAD en EUR"

Besoin d'une autre conversion ?"""

# Instance globale
currency_service = CurrencyService()

# Test
if __name__ == "__main__":
    service = CurrencyService()
    
    # Test
    test = "Convertis 100 USD en EUR"
    print(f"=== Test: {test} ===")
    if service.is_currency_request(test):
        result = service.parse_and_convert(test)
        print(service.format_response(result, test))
