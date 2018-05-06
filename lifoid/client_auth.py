# Authorization handler that allows idenfitication from client side
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
from lifoid.config import settings
import lifoid.signals as signals


def get_dev_user(app, data):
    if settings.dev_auth == 'yes':
        return data.get('user', None)
    return None


def register():
    signals.get_user.connect(get_dev_user)
