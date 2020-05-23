# -*- coding: utf8 -*-
"""
Lifoid flask app
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import sys
import os
import importlib
from flask import Flask
from flask_s3 import FlaskS3
from flask_babel import Babel
from flask_cors import CORS
from commis import color
from lifoid.loggingmixin import ServiceLogger
from lifoid.constants import HEADER
from lifoid.config import settings
from lifoid.www.api.webhook import webhook
from lifoid.www.api.messages import messages
from lifoid.plugin import Plugator
import lifoid.signals as signals
sys.path.insert(0, os.getcwd())

logger = ServiceLogger()
if settings.web_static_bucket != '':
    s3 = FlaskS3()


def create_app():
    """
    Configure and launch flask app
    """
    try:
        app_settings_module = importlib.import_module(
            settings.lifoid_settings_module
        )
        flask_app = Flask(__name__)
        flask_app.jinja_env.trim_blocks = True
        flask_app.jinja_env.keep_trailing_newline = True
        if settings.web_static_bucket != '':
            flask_app.config['FLASKS3_BUCKET_NAME'] = \
                settings.web_static_bucket
            flask_app.config['FLASKS3_FORCE_MIMETYPE'] = True
        plugator = Plugator(
            app_settings_module.PLUGINS,
            app_settings_module.PLUGIN_PATHS,
            settings
        )
        translations = plugator.get_plugins(signals.get_translation)
        translation_directories = translations + \
            [app_settings_module.TRANSLATIONS_PATH]
        flask_app.config['BABEL_TRANSLATION_DIRECTORIES'] = \
            ';'.join(translation_directories)
        flask_app.register_blueprint(webhook)
        flask_app.register_blueprint(messages)
        blueprints = plugator.get_plugins(signals.get_blueprint, flask_app)
        logger.debug('blueprints {}'.format(blueprints))
        for blueprint in blueprints:
            flask_app.register_blueprint(blueprint)
        if settings.web_static_bucket != '':
            s3.init_app(flask_app)
        return flask_app
    except ImportError:
        raise
        return None


app = create_app()
babel = Babel(app)
CORS(app)


def launch_app(reloader=False, **kwargs):
    print(HEADER)
    print(color.format(' * Server is running on {} port {}'
                       .format(kwargs['host'], kwargs['port']),
                       color.GREEN))
    app.run(use_reloader=reloader, **kwargs)
