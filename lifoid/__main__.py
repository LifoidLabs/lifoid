#!/usr/bin/env python

# __main__ for lifoid command
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis

"""
Definition of the lifoid app and commands
"""

import logging
from commis import color
from commis import ConsoleProgram
from lifoid.commands.run import RunCommand
from lifoid.commands.talk import TalkCommand
from lifoid.commands.init import InitCommand
from lifoid.commands.test import TestCommand
from lifoid.commands.load_static import LoadstaticCommand
from lifoid.commands.cli import CliCommand
from lifoid.commands.load_template import LoadTemplatesCommand


log = logging.getLogger(__name__)

DESCRIPTION = "Management and administration commands for lifoid"
EPILOG = "If there are any bugs or concerns, submit an issue on Github: https://www.github.com/romaryd/lifoid.git"
COMMANDS = [
    InitCommand,
    CliCommand,
    TestCommand,
    RunCommand,
    TalkCommand,
    LoadstaticCommand,
    LoadTemplatesCommand,
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
        return utility


def cli():
    app = LifoidApp.load()
    app.execute()



if __name__ == '__main__':  # pragma: no cover
    cli()
