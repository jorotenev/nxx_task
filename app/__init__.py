from flask import Flask
from logging.config import dictConfig

"""
http://flask.pocoo.org/docs/1.0/logging/
"If possible, configure logging before creating the application object.
"""
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def _base_app(config_name):
    """
    initialise a barebone flask app.
    :arg config_name [string] - the name of the environment; must be a key in the "config" dict
    """
    from config import configs
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)
    return app


def create_app(config_name):
    """
    Creates the Flask app.
    """
    from config import EnvironmentName
    print("Creating an app for environment: [%s]" % config_name)

    if config_name not in EnvironmentName.all_names():
        raise KeyError('config_name must be one of [%s]' % ", ".join(EnvironmentName.all_names()))

    app = _base_app(config_name=config_name)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
