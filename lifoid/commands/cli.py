"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import traceback
import json
from commis import Command, color
from lifoid import Lifoid
from lifoid.message import LifoidMessage, Chat
from lifoid.message.message_types import CHAT
from lifoid.renderer.talk import SimpleToTalkRenderer
from lifoid.constants import HEADER


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
                            type=CHAT,
                            payload=Chat(text='',
                                         attachments=input_msg),
                            lifoid_id=lifoid_id
                        )
                    else:
                        msg = LifoidMessage(
                            from_user='me',
                            to_user='talk',
                            type=CHAT,
                            payload=Chat(text=input_msg,
                                         attachments=None),
                            lifoid_id=lifoid_id
                        )
                    Lifoid(
                        lifoid_id=lifoid_id,
                        renderer=SimpleToTalkRenderer()
                    ).reply(msg, 'cli')
                except Exception:
                    print(traceback.format_exc())
        return color.format("* bye bye", color.RED)