"""
Service d'envoi d'emails pour l'Assistant Medical IA
Supporte: SendGrid API (recommandé pour Render) et SMTP
"""

import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Import SendGrid
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


class EmailService:
    def __init__(self):
        # Configuration SendGrid (prioritaire)
        self.sendgrid_key = os.environ.get('SENDGRID_API_KEY', '')
        
        # Configuration SMTP (fallback)
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_user = os.environ.get('SMTP_USER', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        self.sender_name = "Assistant Medical IA"
        
        # Email expéditeur pour SendGrid (IMPORTANT: doit être vérifié dans SendGrid)
        # Utiliser SENDGRID_FROM_EMAIL ou SMTP_USER ou email par défaut
        self.sender_email = os.environ.get('SENDGRID_FROM_EMAIL', 
                                          os.environ.get('SMTP_USER', 
                                          'noreply@medical-ai.com'))
        
        # Déterminer le provider
        if self.sendgrid_key and SENDGRID_AVAILABLE:
            self.provider = "sendgrid"
            print(f"✓ Email: SendGrid activé (expéditeur: {self.sender_email})")
        elif self.smtp_user and self.smtp_password:
            self.provider = "smtp"
            print("⚠️ Email: SMTP (peut être bloqué sur Render)")
        else:
            self.provider = None
            print("⚠️ Email: Non configuré")

    def is_available(self):
        return self.provider is not None

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def extract_email_from_text(self, text):
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def format_conversation_summary(self, conversation_history, collected_symptoms=None):
        date_str = datetime.now().strftime('%d/%m/%Y a %H:%M')
        lines = ["RESUME DE CONSULTATION - ASSISTANT MEDICAL IA", "", f"Date: {date_str}", ""]
        
        if collected_symptoms:
            lines.append("SYMPTOMES MENTIONNES:")
            for s in collected_symptoms:
                lines.append(f"  - {s}")
            lines.append("")
        
        lines.append("HISTORIQUE DE LA CONVERSATION:")
        lines.append("-" * 40)

        for msg in conversation_history:
            role = "Vous" if msg.get('role') == 'user' else "Assistant"
            content = msg.get('content', '')[:500]
            lines.append(f"{role}: {content}")
            lines.append("")
        
        lines.extend(["-" * 40, "", "AVERTISSEMENT: Ce resume est informatif uniquement.",
                     "Consultez un professionnel de sante.", "Urgence: appelez le 15 (SAMU)"])
        
        return "\n".join(lines)

    def send_email(self, to_email, subject, body, is_html=False):
        if not self.is_available():
            return {"success": False, "error": "Service email non configure"}

        if not self.validate_email(to_email):
            return {"success": False, "error": f"Email invalide: {to_email}"}

        # Utiliser SendGrid si disponible
        if self.provider == "sendgrid":
            return self._send_with_sendgrid(to_email, subject, body)
        else:
            return self._send_with_smtp(to_email, subject, body)

    def _send_with_sendgrid(self, to_email, subject, body):
        """Envoie via SendGrid API"""
        try:
            # Vérifier que la clé API est présente
            if not self.sendgrid_key:
                return {"success": False, "error": "SENDGRID_API_KEY non configurée"}
            
            # Vérifier que l'email expéditeur est configuré
            if not self.sender_email or self.sender_email == 'noreply@medical-ai.com':
                return {
                    "success": False, 
                    "error": "Email expéditeur non configuré. Ajoutez SENDGRID_FROM_EMAIL dans les variables d'environnement Render avec un email vérifié dans SendGrid."
                }
            
            message = Mail(
                from_email=self.sender_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )
            
            sg = SendGridAPIClient(self.sendgrid_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                return {"success": True, "message": f"Email envoyé à {to_email} via SendGrid"}
            else:
                return {
                    "success": False, 
                    "error": f"SendGrid erreur {response.status_code}: {response.body}"
                }
                
        except Exception as e:
            error_msg = str(e)
            
            # Messages d'erreur plus clairs
            if "does not contain a valid address" in error_msg or "Sender" in error_msg:
                return {
                    "success": False,
                    "error": f"Email expéditeur '{self.sender_email}' non vérifié dans SendGrid. Allez sur SendGrid > Settings > Sender Authentication pour vérifier votre email."
                }
            elif "API key" in error_msg or "Unauthorized" in error_msg:
                return {
                    "success": False,
                    "error": "Clé API SendGrid invalide. Vérifiez SENDGRID_API_KEY dans Render."
                }
            else:
                return {
                    "success": False, 
                    "error": f"Erreur SendGrid: {error_msg[:200]}"
                }

    def _send_with_smtp(self, to_email, subject, body):
        """Envoie via SMTP (peut être bloqué sur Render)"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.smtp_user}>"
            msg['To'] = to_email
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=5) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return {"success": True, "message": f"Email envoye a {to_email}"}

        except smtplib.SMTPAuthenticationError:
            return {"success": False, "error": "Erreur authentification SMTP"}
        except (TimeoutError, OSError):
            return {"success": False, "error": "Render bloque SMTP. Configurez SENDGRID_API_KEY"}
        except Exception as e:
            return {"success": False, "error": f"Erreur: {str(e)[:100]}"}

    def send_conversation_summary(self, to_email, conversation_history, collected_symptoms=None):
        date_str = datetime.now().strftime('%d/%m/%Y')
        subject = f"Resume consultation - {date_str}"
        body = self.format_conversation_summary(conversation_history, collected_symptoms)
        return self.send_email(to_email, subject, body)


email_service = EmailService()
