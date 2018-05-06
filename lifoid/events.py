# list of handlers for messaging applications
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
from importlib import import_module
from awesomedecorators import timeit
from lifoid.plugin import Plugator
from lifoid.config import settings
import lifoid.signals as signals


@timeit
def process_event(e_type, event, async=True):
    """
    Look through a list of protocol handlers to pass an event.
    """
    app_settings_module = import_module(
        settings.lifoid_settings_module
    )
    handlers = Plugator(
        app_settings_module.PLUGINS,
        app_settings_module.PLUGIN_PATHS,
        settings).get_plugins(signals.get_handler)
    for handler in handlers:
        resp = handler.process(e_type, event, async)
        if resp is not None:
            return resp
    return None