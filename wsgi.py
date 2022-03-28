"""Wsgi/Asgi flask application."""
import json
import logging

from asgiref.wsgi import WsgiToAsgi

from flask import Flask


def create_application():
    """
    Create basic flask application with configs.

    Returns:
        return flask application
    """
    logger = logging.getLogger('apiLogger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('api_log.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S'),
    )

    logger.addHandler(file_handler)
    logger.info('Run server')

    application = Flask(__name__)

    from configs import create_configs
    create_configs()
    application.config.from_file('config.json', load=json.load)

    from views import views
    application.register_blueprint(views)
    return application


application = create_application()
asgi_application = WsgiToAsgi(application)
