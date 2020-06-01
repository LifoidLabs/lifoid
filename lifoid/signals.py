"""
Signals that allow third parties to develop plugins for Lifoid
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
from __future__ import print_function, unicode_literals
from blinker import signal

get_conf = signal('get_conf')

initialized = signal('lifoid_initialized')
get_parser = signal('get_parser')
get_translator = signal('get_translator')
get_translation = signal('get_translation')
get_handler = signal('get_handler')
get_blueprint = signal('get_blueprint')
get_command = signal('get_command')
get_user = signal('get_user')
get_bot_conf = signal('get_bot_conf')
get_action = signal('get_action')
get_backend = signal('get_backend')
