"""
Service d'envoi d'emails pour l'Assistant Medical IA
"""

import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class EmailService:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_user = os.environ.get('SMTP_USER', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.sender_name = "Assistant Medical IA"

    def is_available(self):
        return bool(self.smtp_user and self.smtp_password)

    def validate_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None

    def extract_email_from_text(self, text):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def format_conversation_summary(self, conversation_history, collected_symptoms=None):
        date_str = datetime.now().strftime('%d/%m/%Y a %H:%M')
        lines = []
        lines.append("RESUME DE CONSULTATION - ASSISTANT MEDICAL IA")
        lines.append("")
        lines.append(f"Date: {date_str}")
        lines.append("")
        
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
        
        lines.append("-" * 40)
        lines.append("")
        lines.append("AVERTISSEMENT: Ce resume est informatif uniquement.")
        lines.append("Consultez un professionnel de sante.")
        lines.append("Urgence: appelez le 15 (SAMU)")
        
        return "\n".join(lines)

    def send_email(self, to_email, subject, body, is_html=False):
        if not self.is_available():
            return {"success": False, "error": "Service email non configure"}

        if not self.validate_email(to_email):
            return {"success": False, "error": f"Email invalide: {to_email}"}

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.smtp_user}>"
            msg['To'] = to_email
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return {"success": True, "message": f"Email envoye a {to_email}"}

        except smtplib.SMTPAuthenticationError:
            return {"success": False, "error": "Erreur authentification SMTP"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_conversation_summary(self, to_email, conversation_history, collected_symptoms=None):
        date_str = datetime.now().strftime('%d/%m/%Y')
        subject = f"Resume consultation - {date_str}"
        body = self.format_conversation_summary(conversation_history, collected_symptoms)
        return self.send_email(to_email, subject, body)


email_service = EmailService()
