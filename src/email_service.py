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
        self.sender_name = "Assistant Medical IA"

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
        date_str = datetime.now().strftime('%d/%m/%Y a %H:%M')
        summary = f"""
RESUME DE CONSULTATION - ASSISTANT MEDICAL IA

Date: {date_str}

"""
        if collected_symptoms:
            symptoms_list = '\n'.join('  - ' + s for s in collected_symptoms)
            summary += f"""SYMPTOMES MENTIONNES:
{symptoms_list}

"""
        summary += "HISTORIQUE DE LA CONVERSATION:\n"
        summary += "-" * 50 + "\n"

        for msg in conversation_history:
            role = "Vous" if msg.get('role') == 'user' else "Assistant"
            content = msg.get('content', '')[:500]
            if len(msg.get('content', '')) > 500:
                content += "..."
            summary += f"\n{role}:\n{content}\n"

        summary += """
-" * 50

AVERTISSEMENT IMPORTANT:
Ce resume est fourni a titre informatif uniquement.
Il ne constitue pas un diagnostic medical.
Consultez toujours un professionnel de sante.

En cas d'urgence, appelez le 15 (SAMU) ou le 112.

Genere par Assistant Medical IA
"""
        return summary

    def send_email(self, to_email, subject, body, is_html=False):
        """Envoie un email"""
        if not self.is_available():
            return {
                "success": False,
                "error": "Service email non configure. Contactez l'administrateur."
            }

        if not self.validate_email(to_email):
            return {
                "success": False,
                "error": f"Adresse email invalide: {to_email}"
            }

        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.smtp_user}>"
            msg['To'] = to_email

            if is_html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return {
                "success": True,
                "message": f"Email envoye avec succes a {to_email}"
            }

        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "error": "Erreur d'authentification SMTP. Verifiez les identifiants."
            }
        except smtplib.SMTPException as e:
            return {
                "success": False,
                "error": f"Erreur SMTP: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur: {str(e)}"
            }

    def send_conversation_summary(self, to_email, conversation_history, collected_symptoms=None):
        """Envoie un résumé de conversation par email"""
        date_str = datetime.now().strftime('%d/%m/%Y')
        subject = f"Resume consultation - Assistant Medical IA - {date_str}"
        body = self.format_conversation_summary(conversation_history, collected_symptoms)
        return self.send_email(to_email, subject, body)


# Instance globale
email_service = EmailService()
