"""
Load static files on Amazon S3

Author:   Romary Dupuis <romary@me.com>

Copyright (C) 2017-2018 Romary Dupuis
"""
from importlib import import_module
from commis import Command, color
from flask_s3 import create_all
from lifoid.constants import HEADER
from lifoid.plugin import Plugator
import lifoid.signals as signals


class LoadstaticCommand(Command):
    """
    CLI to load static files needed by Lifoid web app on Amazon S3
    """
    name = 'loadstatic'
    help = 'load static files'
    args = {
        '--bucket': {
            'metavar': 'BUCKET',
            'required': True,
            'help': 'name of bucket on Amazon S3'
        }
    }

    def handle(self, args):
        """
        CLI to run the lifoid HTTP API server application.
        """
        from lifoid.config import settings
        try:
            app_settings_module = import_module(
                settings.lifoid_settings_module
            )
            Plugator(
                app_settings_module.PLUGINS,
                app_settings_module.PLUGIN_PATHS,
                settings).get_plugins(signals.get_command)
        except ModuleNotFoundError:
            color.format("No settings module found. Have you initialized your project with `lifoid init` command? ", color.RED)
        print(HEADER)
        from lifoid.www.app import app
        app.config['FLASKS3_BUCKET_NAME'] = args.bucket
        create_all(app)
        return color.format(" * Static files loaded", color.GREEN)
