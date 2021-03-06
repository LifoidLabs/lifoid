# routing of messages with actions
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
from functools import wraps as wraps
from commis import color
from lifoid.logging.mixin import ServiceLogger

LOGGER = ServiceLogger()


def action(route_func=None):
    """
    Decorator that checks if conditions to get into an action have been
    fulfiled.
    """
    def receive_func(func):
        """
        Decorated route.
        """
        @wraps(func)
        def wrapper(message, context):
            if route_func is None or route_func(message, context):
                LOGGER.info(f'Action {func.__name__}')
                return True, func
            return False, None
        return wrapper
    return receive_func
