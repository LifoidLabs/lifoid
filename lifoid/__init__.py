"""
Lifoid main class
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""

from .version import get_version
import os
import sys
import importlib
from flask_babel import refresh
from flask import current_app as app
from awesomedecorators import memoized
from lifoid.renderer.stdout import StdoutRenderer
from lifoid.config import settings
from lifoid.bot import Bot
from lifoid.bot.repository import BotRepository
from lifoid.message import LifoidMessage
from lifoid.message.repository import MessageRepository
from lifoid.plugin import plugator
import lifoid.signals as signals
from lifoid.logging.mixin import LoggingMixin

sys.path.insert(0, os.getcwd())

__version__ = get_version()


class Lifoid(LoggingMixin):
    """
    Central application bot system
    """
    def __init__(self,
                 lifoid_id,
                 lang='en',
                 renderer=StdoutRenderer(),
                 actions=None,
                 bot_model=Bot,
                 plugins=None,
                 plugins_path=None):
        self.lifoid_id = lifoid_id
        self.lang = lang
        self.app_settings_module = None
        self.router_module = None
        self.context = None

        self.init_settings_module()

        self.init_plugins(plugins, plugins_path)

        self.renderer = renderer

        self.init_routing(actions)
        self.init_context_model(bot_model)

        self.logger.debug('Bot Type: {}'.format(self.bot_model))
        signals.initialized.send(self)

    def init_settings_module(self):
        try:
            self.app_settings_module = importlib.import_module(
                settings.lifoid_settings_module
            )
            self.router_module = importlib.import_module(
                self.app_settings_module.ROUTER_CONF
            )
        except ImportError:
            self.logger.debug('no settings configured')

    def init_plugins(self, plugins, plugins_path):
        if self.app_settings_module is not None:
            for path in self.app_settings_module.PLUGIN_PATHS:
                plugator.add_plugin_path(path)
            for plugin in self.app_settings_module.PLUGINS:
                plugator.add_plugin(plugin)
        if plugins is not None:
            for path in plugins_path:
                plugator.add_plugin_path(path)
            for plugin in plugins:
                plugator.add_plugin(plugin)

    def init_routing(self, actions):
        if actions is None:
            if self.router_module is not None:
                self.actions = self.router_module.actions
        else:
            self.actions = actions

    def init_context_model(self, bot_model):
        if self.router_module is not None:
            self.bot_model = self.router_module.bot_model
        else:
            self.bot_model = bot_model
        self.context = None

    @memoized
    def backend(self):
        return plugator.get_plugin(
            signals.get_backend
        )

    @memoized
    def context_rep(self):
        return BotRepository(self.backend,
                             settings.context_prefix)

    @memoized
    def message_rep(self):
        return BotRepository(self.backend,
                             settings.message_prefix)

    @memoized
    def parser(self):
        return plugator.get_plugin(signals.get_parser)

    @memoized
    def translator(self):
        return plugator.get_plugin(signals.get_translator)

    @memoized
    def bot_conf(self):
        return plugator.get_plugin(
            signals.get_bot_conf,
            lifoid_id=self.lifoid_id
        )

    def reply(self, message: LifoidMessage, reply_id=None, context_id=None):
        """
        Handles message and reply.

        In this method, the following operations are executed.

        - process message analysis based on a configurable pipeline
        - calls an action which matches to ``@action`` condition first
        - generates messages to reply by calling an action
        - make requests to API by calling renderer's ``render`` function
        """
        if context_id is None:
            context_id = reply_id
        self.context = self.context_rep.get(
            '{}:{}'.format(self.lifoid_id, context_id),
            None,
            klass=self.bot_model,
            lifoid_id=self.lifoid_id
        )

        self.message_rep.save(
            '{}:{}'.format(self.lifoid_id, reply_id),
            message.date, message)

        self.context['__lang__'] = self.lang

        if settings.pasync == 'no' and settings.templates == 'flask':
            try:
                from lifoid.www.app import app
                with app.app_context():
                    app.config['BABEL_DEFAULT_LOCALE'] = \
                        self.context['__lang__'].replace('-', '_')
                    refresh()
            except RuntimeError:
                pass

        if self.bot_conf is not None and\
           self.context['__lang__'] != self.bot_conf['language'] and\
           self.bot_conf['language'] not in self.context['__lang__']:
            self.logger.debug(
                'bot_conf language: {}'.format(self.bot_conf['language']))
            self.logger.debug(
                'context language: {}'.format(self.context['__lang__']))
            _from = self.context['__lang__'].split('-')[0]
            _to = self.bot_conf['language'].split('-')[0]
            message.translate(self.translator,
                              _from=_from,
                              _to=_to)
        message.parse(self.parser, self.context)

        if settings.templates == 'flask':
            from lifoid.www.app import app
            with app.app_context():
                self.process_actions(message, reply_id, context_id)
        else:
            self.process_actions(message, reply_id, context_id)

        return None

    def process_actions(self, message, reply_id, context_id):
        def render(messages):
            """
            Bridge to renderer's render method
            """
            for message in messages:
                msg = message._replace(
                    topic=reply_id,
                    from_user=self.lifoid_id,
                    to_user=reply_id,
                    lifoid_id=self.lifoid_id)
                self.message_rep.save(
                    '{}:{}'.format(self.lifoid_id, reply_id),
                    msg.date, msg)
                self.renderer.render([msg], reply_id)
            return messages
        for candidate in self.actions:
            match, action = candidate(message, self.context)
            if match:
                output = action(render, message, self.context)
                self.context_rep.save(
                    '{}:{}'.format(self.lifoid_id, context_id),
                    None, self.context)
                return output
        self.logger.warning('No action matched. Define fallback action.')
