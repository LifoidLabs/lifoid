#!/usr/bin/env python

# __main__ for lifoid command
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis

"""
Definition of the lifoid app and commands
"""
from importlib import import_module
import logging
from commis import color
from commis import ConsoleProgram
from lifoid.commands.run import RunCommand
from lifoid.commands.init import InitCommand
from lifoid.commands.test import TestCommand
from lifoid.commands.load_static import LoadstaticCommand
from lifoid.commands.cli import CliCommand
from lifoid.commands.load_templates import LoadTemplatesCommand
from lifoid.commands.mqtt_bot import MQTTBotCommand
from lifoid.commands.mqtt_client import MQTTClientCommand
from lifoid.config import settings
from lifoid.signals import get_command
from lifoid.plugin import Plugator

log = logging.getLogger(__name__)

DESCRIPTION = "Management and administration commands for lifoid"
EPILOG = \
"""
If there are any bugs or concerns, submit an issue on Github:
https://www.github.com/romaryd/lifoid.git
"""
COMMANDS = [
    InitCommand,
    CliCommand,
    TestCommand,
    RunCommand,
    LoadstaticCommand,
    LoadTemplatesCommand,
    MQTTBotCommand,
    MQTTClientCommand
]


class LifoidApp(ConsoleProgram):
    """
    lifoid CLI app
    """
    description = color.format(DESCRIPTION, color.CYAN)
    epilog = color.format(EPILOG, color.MAGENTA)

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        try:
            app_settings_module = import_module(
                settings.lifoid_settings_module
            )
            command_plugins = Plugator(
                app_settings_module.PLUGINS,
                app_settings_module.PLUGIN_PATHS,
                settings).get_plugins(get_command)
            for command in command_plugins:
                utility.register(command)
        except ModuleNotFoundError:
            pass
        return utility


def cli():
    app = LifoidApp.load()
    app.execute()



if __name__ == '__main__':  # pragma: no cover
    cli()
