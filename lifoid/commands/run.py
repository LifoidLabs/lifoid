"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import traceback
from importlib import import_module
from commis import Command, color
from lifoid.plugin import Plugator
import lifoid.signals as signals


class RunCommand(Command):

    name = 'run'
    help = 'launch a lifoid server application'
    args = {
        '--host': {
            'metavar': 'ADDR',
            'default': False,
            'help': 'set the host to run the app on'
        },
        '--port': {
            'metavar': 'PORT',
            'type': int,
            'default': False,
            'help': 'set the port to run the app on'
        },
        '--debug': {
            'action': 'store_true',
            'required': False,
            'help': 'force debug mode'
        }
    }

    def handle(self, args):
        """
        CLI to run the lifoid HTTP API server application.
        """
        try:
            from lifoid.config import settings
            from lifoid.www.app import launch_app
            app_settings_module = import_module(
                settings.lifoid_settings_module
            )
            Plugator(
                app_settings_module.PLUGINS,
                app_settings_module.PLUGIN_PATHS,
                settings).get_plugins(signals.get_command)
            kwargs = {
                'host': args.host or settings.server.host,
                'port': args.port or settings.server.port,
                'debug': args.debug or settings.debug,
            }
            launch_app(False, **kwargs)
        except ModuleNotFoundError:
            color.format("No settings module found. Have you initialized your project with `lifoid init` command? ", color.RED)
        except:
            print(traceback.format_exc())
            return color.format(" * Error while launching Lifoid", color.RED)
        return color.format(" * Web application stopped", color.RED)
