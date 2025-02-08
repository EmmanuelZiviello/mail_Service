import smtplib
import ssl
import logging

from flask import render_template
import utils.credentials as credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configura il logger
logging.basicConfig(filename='email_errors.log', level=logging.ERROR)

def send_mail_registrazione_medico(codice_identificativo, password_temporanea, email_nutrizionista, email_paziente):
    # Crea il messaggio per il nutrizionista
    message_nutrizionista = MIMEMultipart("alternative")
    message_nutrizionista["Subject"] = f""" Identificativo F-taste paziente "{email_paziente}" """
    message_nutrizionista["From"] = credentials.mail_sender_email
    message_nutrizionista["To"] = email_nutrizionista

    # Usa render_template per il contenuto dell'email per il nutrizionista
    html_nutrizionista = render_template("nutrizionista/email_template.html", 
                                         codice_identificativo=codice_identificativo, 
                                         email_paziente=email_paziente)
    body_nutrizionista = MIMEText(html_nutrizionista, "html")
    message_nutrizionista.attach(body_nutrizionista)

    # Crea il messaggio per il paziente
    message_paziente = MIMEMultipart("alternative")
    message_paziente["Subject"] = " Identificativo F-taste "
    message_paziente["From"] = credentials.mail_sender_email
    message_paziente["To"] = email_paziente

    # Usa render_template per il contenuto dell'email per il paziente
    html_paziente = render_template("paziente/email_template.html", 
                                    codice_identificativo=codice_identificativo, 
                                    password_temporanea=password_temporanea)
    body_paziente = MIMEText(html_paziente, "html")
    message_paziente.attach(body_paziente)

    # Invia le email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(credentials.smtp_server, credentials.port, context=context) as server:
        try:
            server.login(credentials.mail_sender_email, credentials.mail_sender_password)
            server.sendmail(credentials.mail_sender_email, email_paziente, message_paziente.as_string())
            server.sendmail(credentials.mail_sender_email, email_nutrizionista, message_nutrizionista.as_string())
        except smtplib.SMTPException as e:
            if isinstance(e, smtplib.SMTPRecipientsRefused):
                error_message = f"{email_paziente} not exist or rejected"
                logging.error(f"Error sending email to {email_paziente}: {error_message}")
                raise EmailNotFound(error_message)
            else:
                logging.error(f"Unexpected error: {str(e)}")
                raise e


def send_mail_registrazione_paziente(codice_identificativo, email_paziente):
    message_paziente = MIMEMultipart("alternative")
    message_paziente["Subject"] = " Identificativo F-taste "
    message_paziente["From"] = credentials.mail_sender_email
    message_paziente["To"] = email_paziente

    # Usa render_template per il contenuto dell'email per il paziente
    html_paziente = render_template("paziente/email_template.html", 
                                    codice_identificativo=codice_identificativo)
    body_email_paziente = MIMEText(html_paziente, "html")
    message_paziente.attach(body_email_paziente)

    # Invia l'email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(credentials.smtp_server, credentials.port, context=context) as server:
        try:
            server.login(credentials.mail_sender_email, credentials.mail_sender_password)
            server.sendmail(credentials.mail_sender_email, email_paziente, message_paziente.as_string())
        except smtplib.SMTPException as e:
            if isinstance(e, smtplib.SMTPRecipientsRefused):
                error_message = f"{email_paziente} not exist or rejected"
                logging.error(f"Error sending email to {email_paziente}: {error_message}")
                raise EmailNotFound(error_message)
            else:
                logging.error(f"Unexpected error: {str(e)}")
                raise e


def send_mail_refresh_paziente(email_paziente, link_refresh, id_paziente):
    message_paziente = MIMEMultipart("alternative")
    message_paziente["Subject"] = " Recupero password \"f-taste\" "

    html_paziente = render_template("paziente/email_reset_password.html", link_refresh=link_refresh, id=id_paziente)
    body_email_paziente = MIMEText(html_paziente, "html")
    message_paziente.attach(body_email_paziente)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(credentials.smtp_server, credentials.port, context=context) as server:
        try:
            server.login(credentials.mail_sender_email, credentials.mail_sender_password)
            server.sendmail(credentials.mail_sender_email, email_paziente, message_paziente.as_string())
        except smtplib.SMTPException as e:
            if isinstance(e, smtplib.SMTPRecipientsRefused):
                error_message = f"{email_paziente} not exist or rejected"
                logging.error(f"Error sending email to {email_paziente}: {error_message}")
                raise EmailNotFound(error_message)
            else:
                logging.error(f"Unexpected error: {str(e)}")
                raise e


class EmailNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        # Log the error message
        logging.error(f"Email not found: {self.message}")
