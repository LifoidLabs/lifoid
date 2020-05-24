# -*- coding: utf8 -*-
"""
Logging utility
Author: Romary Dupuis <romary@me.com>
Credits: Benjamin Bengfort <benjamin@bengfort.com>
"""
import os
import logging
import logging.config
import getpass
import warnings
from dotenv import load_dotenv

# Load Environment variables if available
ENV_PATH = os.path.abspath('.env')
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

from lifoid.logging.config import CONFIGURATION

logging.config.dictConfigClass(CONFIGURATION).configure()
if os.environ.get('LOGGING_DEBUG', 'yes') == 'yes':
    logging.captureWarnings(True)


class WrappedLogger:
    """
    Wraps the Python logging module's logger object to ensure that all process
    logging happens with the correct configuration as well as any extra
    information that might be required by the log file (for example, the user
    on the machine, hostname, IP address lookup, etc).

    Subclasses must specify their logger as a class variable so all instances
    have access to the same logging object.
    """

    logger = None

    def __init__(self, **kwargs):
        self.raise_warnings = kwargs.pop('raise_warnings',
                                         os.environ.get('LOGGING_DEBUG', 'yes')
                                         is 'yes')
        self.logger = kwargs.pop('logger', self.logger)

        if not self.logger or not hasattr(self.logger, 'log'):
            raise TypeError(
                "Subclasses must specify a logger, not {}"
                .format(type(self.logger))
            )

        self.extras = kwargs

    def log(self, level, message, *args, **kwargs):
        """
        This is the primary method to override to ensure logging with extra
        options gets correctly specified.
        """
        extra = self.extras.copy()
        extra.update(kwargs.pop('extra', {}))

        kwargs['extra'] = extra
        self.logger.log(level, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        return self.log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        return self.log(logging.INFO, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """
        Specialized warnings system. If a warning subclass is passed into
        the keyword arguments and raise_warnings is True - the warnning will
        be passed to the warnings module.
        """
        warncls = kwargs.pop('warning', None)
        if warncls and self.raise_warnings:
            warnings.warn(message, warncls)

        return self.log(logging.WARNING, message, *args, **kwargs)

    # Alias warn to warning
    warn = warning

    def error(self, message, *args, **kwargs):
        return self.log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        return self.log(logging.CRITICAL, message, *args, **kwargs)


class ServiceLogger(WrappedLogger):
    """
    Performs logging for a service with the log options above.
    """

    logger = logging.getLogger(os.environ.get('LOGGING_SERVICE',
                                              'process'))

    def __init__(self, **kwargs):
        self._user = kwargs.pop('user', None)
        super(ServiceLogger, self).__init__(**kwargs)

    @property
    def user(self):
        if not self._user:
            self._user = getpass.getuser()
        return self._user

    def log(self, level, message, *args, **kwargs):
        """
        Provide current user as extra context to the logger
        """
        extra = kwargs.pop('extra', {})
        extra.update({
            'user': self.user
        })

        kwargs['extra'] = extra
        super(ServiceLogger, self).log(level, message, *args, **kwargs)


class LoggingMixin:
    """
    Mix in to classes that need their own logging object!
    """

    @property
    def logger(self):
        """
        Instantiates and returns a ServiceLogger instance
        """
        if not hasattr(self, '_logger') or not self._logger:
            self._logger = ServiceLogger()
        return self._logger
