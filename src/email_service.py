"""
Service d'envoi d'emails pour l'Assistant Médical IA
Permet d'envoyer des résumés de conversation par email
"""

import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self):
        # Configuration SMTP (Gmail par défaut)
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_user = os.environ.get('SMTP_USER', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.sender_name = "Assistant Médical IA"
        
    def is_available(self):
        """Vérifie si le service email est configuré"""
        return bool(self.smtp_user and self.smtp_password)
    
    def validate_email(self, email):
        """Valide le format d'une adresse email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def extract_email_from_text(self, text):
        """Extrait une adresse email d'un texte"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def format_conversation_summary(self, conversation_history, collected_symptoms=None):
        """Formate l'historique de conversation en résumé lisible"""
        summary = f"""
═══════════════════════════════════════════════════════
        RÉSUMÉ DE CONSULTATION - ASSISTANT MÉDICAL IA
═══════════════════════════════════════════════════════

📅 Date: {datetime.now().strftime('%d/%m/%Y à %H:%M')}

"""
        if collected_symptoms:
            summary += f"""
🩺 SYMPTÔMES MENTIONNÉS:
{chr(10).join('  • ' + s for s in collected_symptoms)}

"""
        
        summary += """
💬 HISTORIQUE DE LA CONVERSATION:
───────────────────────────────────────────────────────
"""
        for msg in conversation_history:
            role = "👤 Vous" if msg.get('role') == 'user' else "🤖 Assistant"
            content = msg.get('content', '')[:500]  # Limiter la longueur
            if len(msg.get('content', '')) > 500:
                content += "..."
            summary += f"\n{role}:\n{content}\n"
        
        summary += """
───────────────────────────────────────────────────────

⚠️ AVERTISSEMENT IMPORTANT:
Ce résumé est fourni à titre informatif uniquement.
Il ne constitue pas un diagnostic médical.
Consultez toujours un professionnel de santé pour
un avis médical personnalisé.

🏥 En cas d'urgence, appelez le 15 (SAMU) ou le 112.

───────────────────────────────────────────────────────
Généré par Assistant Médical IA
https://medical-ai-assistant-2k1a.onrender.com
"""
        return summary

    def send_email(self, to_email, subject, body, is_html=False):
        """Envoie un email"""
        if not self.is_available():
            return {
                "success": False,
                "error": "Service email non configuré. Contactez l'administrateur."
            }
        
        if not self.validate_email(to_email):
            return {
                "success": False,
                "error": f"Adresse email invalide: {to_email}"
            }
        
        try:
            # Créer le message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.smtp_user}>"
            msg['To'] = to_email
            
            # Ajouter le contenu
            if is_html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Connexion et envoi
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return {
                "success": True,
                "message": f"Email envoyé avec succès à {to_email}"
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "error": "Erreur d'authentification SMTP. Vérifiez les identifiants."
            }
        except smtplib.SMTPException as e:
            return {
                "success": False,
                "error": f"Erreur SMTP: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur inattendue: {str(e)}"
            }
    
    def send_conversation_summary(self, to_email, conversation_history, collected_symptoms=None):
        """Envoie un résumé de conversation par email"""
        subject = f"📋 Résumé de votre consultation - Assistant Médical IA - {datetime.now().strftime('%d/%m/%Y')}"
        body = self.format_conversation_summary(conversation_history, collected_symptoms)
        return self.send_email(to_email, subject, body)


# Instance globale
email_service = EmailService()

# Test
if __name__ == "__main__":
    print(f"Service email disponible: {email_service.is_available()}")
    print(f"SMTP configuré: {email_service.smtp_server}:{email_service.smtp_port}")
