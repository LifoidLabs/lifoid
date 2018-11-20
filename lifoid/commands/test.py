"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import os
import sys
import traceback
import yaml
import unittest
import json
from importlib import import_module
from commis import Command, color
from lifoid.exceptions import LifoidTestError
from lifoid.constants import HEADER
from lifoid.config import settings
from lifoid.message.repository import MessageRepository
from lifoid.webhook.handler import Handler

sys.path.insert(0, os.getcwd())


PATH = FILE = None


class ConversationsTestCase(unittest.TestCase):
    """
    Conversations test class
    """
    FILE = None
    PATH = None

    def setUp(self):
        """
        Tests initialization
        """
        from lifoid.www.app import app
        app.testing = True
        self.app = app.test_client()
        app_settings_module = import_module(
            settings.lifoid_settings_module
        )
        app_settings_module.HANDLERS = [Handler]
        self.test_file = ConversationsTestCase.FILE
        if ConversationsTestCase.PATH is not None:
            self.tests_path = ConversationsTestCase.PATH
        else:
            self.tests_path = app_settings_module.TESTS_PATH
        self.messages = MessageRepository(
            settings.repository,
            settings.message_prefix
        )
        settings.dev_auth = 'yes'

    def tearDown(self):
        pass

    def test_conversation(self):
        if self.test_file is not None:
            self.run_test(self.test_file)
        else:
            for filename in os.listdir(self.tests_path):
                self.run_test(os.path.join(self.tests_path, filename))

    def run_test(self, filepath):
        print(color.format(filepath, color.CYAN))
        with open(filepath) as file_handle:
            loaded = yaml.load(file_handle.read())
            print('{} messages loaded...'.format(len(loaded)))
            tests = [(loaded[i], loaded[i + 1])
                     for i in range(0, len(loaded) - 1, 2)]
            for mess, resp in tests:
                print(color.format('> {}', color.CYAN, mess))
                try:
                    try:
                        mess = json.loads(mess)
                        rv = self.app.post(
                            '/webhook',
                            data=json.dumps(mess),
                            content_type='application/json',
                            follow_redirects=True)
                    except Exception:
                        rv = self.app.post(
                            '/webhook',
                            data=json.dumps({
                                'lifoid_id': ConversationsTestCase.LIFOID_ID,
                                'access_token': 'access_token',
                                'q': {
                                    'text': mess,
                                    'attachments': None
                                },
                                'user': {
                                    'username': 'me'
                                }
                            }),
                            content_type='application/json',
                            follow_redirects=True)
                    from_date = rv.data.decode('utf8')
                    assert('200' in rv.status)
                    rv = self.app.post(
                        '/messages',
                        data=json.dumps({
                            'lifoid_id': ConversationsTestCase.LIFOID_ID,
                            'access_token': 'access_token',
                            'from_date': from_date,
                            'user': {
                                'username': 'me'
                            }
                        }),
                        content_type='application/json',
                        follow_redirects=True)
                    json_rv = json.loads(rv.data.decode('utf8'))
                    assert('200' in rv.status)
                    valid = True
                    if resp != 'DONT_CARE':
                        valid = False
                        for el in json_rv:
                            if resp in el['payload']['text']:
                                valid = True
                    self.assertTrue(valid)
                    for msg in json_rv:
                        print(color.format('< {}',
                              color.GREEN,
                              msg['payload']['text']))
                except AssertionError:
                    print(color.format(filepath, color.RED))
                    print(color.format('Expected: {}', color.RED, resp))
                    print(color.format('Received: {}', color.RED,
                          json_rv))
                    raise


class TestCommand(Command):
    name = 'test'
    help = 'Run tests suite'
    args = {
        '--path': {
            'metavar': 'PATH',
            'required': False,
            'help': 'location of a group of test files'
        },
        '--file': {
            'metavar': 'FILEPATH',
            'required': False,
            'help': 'location of a test file'
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
        CLI to test to lifoid
        """
        from lifoid.config import settings
        print(HEADER)
        settings.async = 'no'
        ConversationsTestCase.LIFOID_ID = args.lifoid_id
        if args.path is not None:
            ConversationsTestCase.PATH = args.path
            print(color.format('* Run tests suite from {}'.format(args.path),
                               color.GREEN))
        else:
            ConversationsTestCase.FILE = args.file
            print(color.format('* Run tests suite from {}'.format(args.file),
                               color.GREEN))
        try:
            # unittest.main()
            suite = unittest.TestLoader().loadTestsFromTestCase(
                ConversationsTestCase)
            test_result = unittest.TextTestRunner(verbosity=2).run(suite)
            if len(test_result.errors) > 0 or len(test_result.failures) > 0:
                raise LifoidTestError()
            return color.format("* all tests passed", color.GREEN)
        except LifoidTestError as exc:
            print(color.format('* tests suite failed', color.RED))
        except Exception:
            print(traceback.format_exc())
        return color.format("* bye bye", color.GREEN)
