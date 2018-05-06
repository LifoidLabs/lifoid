# Retrieve user information from registered authorization handlers
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
from importlib import import_module
from lifoid.plugin import Plugator
from lifoid.config import settings
import lifoid.signals as signals


def get_user(data):
    """
    Ask for authorization from all listening authentication handlers
    """
    app_settings_module = import_module(
        settings.lifoid_settings_module
    )
    authorizations = Plugator(
        app_settings_module.PLUGINS,
        app_settings_module.PLUGIN_PATHS,
        settings).get_plugins(signals.get_user, data=data)
    for user in authorizations:
        if user is not None:
            return user
    return None