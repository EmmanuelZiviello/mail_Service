#avvia l'app e farà solo da consumer kafka per poter inviare email in certi casi


import threading
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from smtplib import SMTPException
from mail_service import (
    send_mail_refresh_paziente,
    send_mail_registrazione_medico,
    send_mail_registrazione_paziente
)
# from flaskr.kafka_consumer import start_kafka_consumer

def create_app():
    # Crea e configura l'app
    app = Flask(__name__, instance_relative_config=True)

    # Enable CORS
    CORS(app)

    # Initialize Flask-Restx API
    api = Api(app, doc='/doc', title='Email Service API Documentation')

    # Starta Kafka consumer in un thread separato
    ''' 
    def run_kafka_consumer():
        start_kafka_consumer()

    kafka_thread = threading.Thread(target=run_kafka_consumer, daemon=True)
    kafka_thread.start()
    '''

    # Error handlers
    @api.errorhandler(SMTPException)
    def handle_smtp_exception(error: SMTPException):
        return {'message': 'Failed to send email'}, 500

    @api.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        return {'message': 'An unexpected error occurred'}, 500

    # Health check endpoint per verificare che il servizio sia online
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'ok'}, 200

    return app
