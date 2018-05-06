"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import traceback
from importlib import import_module
import requests
import json
from commis import Command, color
from lifoid.constants import HEADER
from lifoid.plugin import Plugator
import lifoid.signals as signals


def send_message(url, mess, lifoid_id):
    try:
        mess = json.loads(mess)
        rv = requests.post(
            '{}/webhook'.format(url),
            data=json.dumps(mess))
    except Exception:
        rv = requests.post(
            '{}/webhook'.format(url),
            data=json.dumps({
                'chatbot_id': lifoid_id,
                'access_token': 'access_token',
                'q': {
                    'text': mess,
                    'attachments': None
                },
                'user': {
                    'username': 'me'
                }
            }))
    from_date = rv.text
    rv = requests.post(
        '{}/messages'.format(url),
        data=json.dumps({
            'chatbot_id': lifoid_id,
            'access_token': 'access_token',
            'from_date': from_date,
            'user': {
                'username': 'me'
            }
        }))
    json_rv = rv.json()
    print(color.format('< {}',
          color.GREEN,
          json_rv[0]['payload']['text']))


class TalkCommand(Command):

    name = 'talk'
    help = 'talk to lifoid server via CLI; A lifoid server must have been launched'
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
        },
        '--lifoid_id': {
            'metavar': 'LIFOID_ID',
            'required': True,
            'help': 'unique id of lifoid chatbot'
        }
    }

    def handle(self, args):
        """
        CLI to talk to lifoid
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
        print(color.format('* I am listening', color.GREEN))
        while True:
            try:
                input_msg = input('> ')
            except KeyboardInterrupt:
                break
            if input_msg == 'exit':
                return color.format("* bye bye", color.RED)
            try:
                send_message(
                    'http://{}:{}'.format(
                        args.host or settings.server.host,
                        args.port or settings.server.port
                    ),
                    input_msg,
                    args.lifoid_id
                )
            except Exception:
                print(traceback.format_exc())
        return color.format("* bye bye", color.RED)
