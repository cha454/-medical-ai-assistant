"""
Service de calculatrice pour l'assistant médical
Permet de faire des calculs mathématiques simples et complexes
"""

import re
import math
from typing import Optional, Dict, Any

class CalculatorService:
    def __init__(self):
        self.last_result = None
        
        # Fonctions mathématiques autorisées
        self.safe_functions = {
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'abs': abs,
            'round': round,
            'pow': pow,
            'pi': math.pi,
            'e': math.e
        }
    
    def is_calculation_request(self, text: str) -> bool:
        """Détecte si le message est une demande de calcul"""
        text_lower = text.lower()
        
        # Mots-clés de calcul
        calc_keywords = [
            "calcul", "calculer", "calcule", "combien font", "combien fait",
            "résous", "résoudre", "équation", "addition", "soustraction",
            "multiplication", "division", "pourcentage", "racine", "carré",
            "puissance", "×", "÷", "=", "+", "table de multiplication"
        ]
        
        # Vérifier les mots-clés
        if any(keyword in text_lower for keyword in calc_keywords):
            return True
        
        # Vérifier si c'est une expression mathématique directe
        # Ex: "45 + 12", "15% de 250", "2^3"
        math_pattern = r'\d+\s*[\+\-\*\/\^%]\s*\d+'
        if re.search(math_pattern, text):
            return True
        
        return False
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """Effectue un calcul mathématique"""
        try:
            # Vérifier si c'est une table de multiplication
            table_match = re.search(r'table\s+(?:de\s+)?multiplication\s+(?:de\s+)?(\d+)', expression.lower())
            if table_match:
                number = int(table_match.group(1))
                return self._generate_multiplication_table(number)
            
            # Nettoyer l'expression
            cleaned_expr = self._clean_expression(expression)
            
            if not cleaned_expr:
                return {
                    "success": False,
                    "error": "Expression invalide",
                    "message": "Je n'ai pas pu comprendre l'expression mathématique."
                }
            
            # Calculer
            result = self._safe_eval(cleaned_expr)
            
            if result is None:
                return {
                    "success": False,
                    "error": "Calcul impossible",
                    "message": "Je n'ai pas pu effectuer ce calcul."
                }
            
            self.last_result = result
            
            return {
                "success": True,
                "expression": cleaned_expr,
                "result": result,
                "formatted_result": self._format_result(result)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Erreur lors du calcul : {str(e)}"
            }
    
    def _generate_multiplication_table(self, number: int) -> Dict[str, Any]:
        """Génère une table de multiplication"""
        table = []
        for i in range(1, 11):
            table.append(f"{number} × {i} = {number * i}")
        
        return {
            "success": True,
            "is_table": True,
            "number": number,
            "table": table
        }
    
    def _clean_expression(self, text: str) -> Optional[str]:
        """Nettoie et prépare l'expression pour le calcul"""
        text = text.lower()
        
        # Extraire l'expression mathématique
        # Patterns courants
        patterns = [
            r"calcule?\s+(.+)",
            r"combien\s+(?:font|fait)\s+(.+)",
            r"résous?\s+(.+)",
            r"(.+)\s*=\s*\?",
            r"^(.+)$"  # Toute l'expression si rien d'autre ne matche
        ]
        
        expression = None
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                expression = match.group(1).strip()
                break
        
        if not expression:
            return None
        
        # Remplacer les mots par des symboles
        replacements = {
            "plus": "+",
            "moins": "-",
            "fois": "*",
            "multiplié par": "*",
            "divisé par": "/",
            "puissance": "**",
            "au carré": "**2",
            "au cube": "**3",
            "×": "*",
            "÷": "/",
            "^": "**",
            " de ": "*",  # Pour "15% de 250"
            "pourcent": "/100*",
            "%": "/100*"
        }
        
        for word, symbol in replacements.items():
            expression = expression.replace(word, symbol)
        
        # Nettoyer les espaces
        expression = re.sub(r'\s+', '', expression)
        
        # Vérifier que c'est sécurisé (seulement chiffres et opérateurs)
        if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
            return None
        
        return expression
    
    def _safe_eval(self, expression: str) -> Optional[float]:
        """Évalue l'expression de manière sécurisée"""
        try:
            # Utiliser eval avec un environnement restreint
            safe_dict = {"__builtins__": {}}
            safe_dict.update(self.safe_functions)
            
            result = eval(expression, safe_dict)
            return float(result)
        except:
            return None
    
    def _format_result(self, result: float) -> str:
        """Formate le résultat pour l'affichage"""
        # Si c'est un entier, afficher sans décimales
        if result == int(result):
            return f"{int(result):,}".replace(",", " ")
        
        # Sinon, afficher avec 2 décimales
        return f"{result:,.2f}".replace(",", " ")
    
    def format_response(self, calc_result: Dict[str, Any], original_query: str) -> str:
        """Formate la réponse pour l'utilisateur"""
        # Table de multiplication
        if calc_result.get("is_table"):
            number = calc_result["number"]
            table = calc_result["table"]
            table_text = "\n".join(table)
            
            return f"""🧮 **Table de Multiplication de {number}**

{table_text}

---

💡 **Autres tables disponibles :**
Demande "table de multiplication de X" pour n'importe quel nombre !"""
        
        # Erreur
        if not calc_result["success"]:
            return f"""🧮 **Calculatrice**

❌ Je n'ai pas pu effectuer ce calcul.

**Raison :** {calc_result.get('message', 'Expression invalide')}

**Exemples de calculs que je peux faire :**
• Calculs simples : "Combien font 45 + 12 ?"
• Pourcentages : "Calcule 15% de 250"
• Puissances : "2 puissance 8"
• Racines : "Racine carrée de 144"
• Tables : "Table de multiplication de 5"

Essaie de reformuler ta question !"""
        
        # Résultat normal
        result = calc_result["result"]
        formatted = calc_result["formatted_result"]
        expression = calc_result["expression"]
        
        return f"""🧮 **Calculatrice**

**Question :** {original_query}

**Calcul :** `{expression}`

**Résultat :** **{formatted}**

---

💡 **Autres calculs que je peux faire :**
• Pourcentages : "15% de 250"
• Puissances : "2^8" ou "2 puissance 8"
• Racines : "sqrt(144)"
• Opérations : +, -, ×, ÷
• Tables : "Table de multiplication de 5"

Besoin d'un autre calcul ?"""

# Instance globale
calculator = CalculatorService()

# Test
if __name__ == "__main__":
    calc = CalculatorService()
    
    # Tests
    tests = [
        "Calcule 45 + 12",
        "Combien font 15% de 250",
        "2 puissance 8",
        "45 × 12",
        "Table de multiplication de 5"
    ]
    
    for test in tests:
        print(f"\n=== Test: {test} ===")
        if calc.is_calculation_request(test):
            result = calc.calculate(test)
            print(calc.format_response(result, test))
