"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import traceback
import json
from commis import Command, color
from importlib import import_module
from lifoid import Lifoid
from lifoid.message import LifoidMessage, Payload
from lifoid.message.message_types import TEXT
from lifoid.renderer.talk import SimpleToTalkRenderer
from lifoid.constants import HEADER
from lifoid.plugin import Plugator
import lifoid.signals as signals


class CliCommand(Command):

    name = 'cli'
    help = 'talk to lifoid via CLI'
    args = {
        '--debug': {
            'action': 'store_true',
            'required': False,
            'help': 'force debug mode'
        },
        '--lifoid_id': {
            'metavar': 'LIFOID_ID',
            'required': False,
            'help': 'unique id of lifoid chatbot'
        }
    }

    def handle(self, args):
        """
        CLI to talk to lifoid
        """
        from lifoid.config import settings
        from lifoid.www.app import app
        try:
            app_settings_module = import_module(
                settings.lifoid_settings_module
            )
            Plugator(
                app_settings_module.PLUGINS,
                app_settings_module.PLUGIN_PATHS,
                settings).get_plugins(signals.get_command)
        except ModuleNotFoundError:
            return color.format("No settings module found. Have you initialized your project with `lifoid init` command? ",
                color.RED)
        with app.app_context():
            print(HEADER)
            print(color.format('* I am listening', color.GREEN))
            lifoid_id = args.lifoid_id or settings.lifoid_id
            while True:
                try:
                    input_msg = input('> ')
                except KeyboardInterrupt:
                    break
                try:
                    if input_msg == 'exit':
                        break
                    if input_msg[0] == '{':
                        input_msg = json.loads(input_msg)
                        msg = LifoidMessage(
                            from_user='me',
                            to_user='lifoid_id',
                            type=TEXT,
                            payload=Payload(text='',
                                            attachments=input_msg),
                        )
                    else:
                        msg = LifoidMessage(
                            from_user='me',
                            to_user='talk',
                            type=TEXT,
                            payload=Payload(text=input_msg,
                                            attachments=None),
                        )
                    Lifoid(
                        lifoid_id=lifoid_id,
                        renderer=SimpleToTalkRenderer()
                    ).reply(msg, 'cli')
                except Exception:
                    print(traceback.format_exc())
        return color.format("* bye bye", color.RED)