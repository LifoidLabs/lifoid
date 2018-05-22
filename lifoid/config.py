"""
Configuration management
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import os
import warnings
from six import add_metaclass
from dotenv import load_dotenv
from singleton import Singleton
from loggingmixin import LoggingMixin


class ImproperlyConfigured(Exception):
    """
    The user did not properly set a configuration value.
    """
    pass


class ConfigurationMissing(Exception):
    """
    Warn the user that an optional configuration is missing.
    """
    pass


# Load Environment variables if available
ENV_PATH = os.path.abspath('.env')
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)


def environ_setting(name, default=None, required=True):
    """
    Fetch setting from the environment. The bahavior of the setting if it
    is not in environment is as follows:

        1. If it is required and the default is None, raise Exception
        2. If it is requried and a default exists, return default
        3. If it is not required and default is None, return  None
        4. If it is not required and default exists, return default
    """
    if name not in os.environ and default is None:
        message = "The {0} ENVVAR is not set.".format(name)
        if required:
            raise ImproperlyConfigured(message)
        else:
            warnings.warn(ConfigurationMissing(message))

    return os.environ.get(name, default)


@add_metaclass(Singleton)
class Configuration:
    def __getitem__(self, key):
        """
        Main configuration access method. Performs a case insensitive
        lookup of the key on the class, filtering methods and pseudo
        private properties. Raises KeyError if not found. Note, this makes
        all properties that are uppercase invisible to the options.
        """
        key = key.lower()
        if hasattr(self, key):
            attr = getattr(self, key)
            if not callable(attr) and not key.startswith('_'):
                return attr
        raise KeyError("%s has no configuration '%s'" % (
            self.__class__.__name__,
            key))

    def get(self, key, default=None):
        """
        Fetches a key from the configuration without raising a KeyError
        exception if the key doesn't exist in the config, instead it
        returns the default (None).
        """
        try:
            return self[key]
        except KeyError:
            return default

    def options(self):
        """
        Returns an iterable of sorted option names in order to loop
        through all the configuration directives specified in the class.
        """
        keys = self.__class__.__dict__.copy()
        keys.update(self.__dict__)
        keys = sorted(keys.keys())

        for opt in keys:
            val = self.get(opt)
            if val is not None:
                yield opt, val

    def __repr__(self):
        return str(self)

    def __str__(self):
        s = ""
        for opt, val in self.options():
            r = repr(val)
            r = " ".join(r.split())
            wlen = 76 - max(len(opt), 10)
            if len(r) > wlen:
                r = r[:wlen - 3] + "..."
            s += "%-10s = %s\n" % (opt, r)
        return s[:-1]


class RedisConfiguration(Configuration):
    """
    Configuration for the database server
    """
    host = environ_setting('REDIS_HOST', 'localhost', required=False)
    port = int(environ_setting('REDIS_PORT', 6379, required=False))
    db = int(environ_setting('REDIS_DB', 0, required=False))


class DynamoDBConfiguration(Configuration):
    """
    Configuration for the database server
    """
    key = environ_setting('DYNAMODB_KEY', 'key', required=False)
    sort_key = environ_setting('DYNAMODB_SORT_KEY', 'date', required=False)


class ServerConfiguration(Configuration):
    """
    Configuration for the web server to run an admin UI.
    """
    host = environ_setting('SERVER_HOST', 'localhost', required=False)
    port = int(environ_setting('SERVER_PORT', 8888, required=False))


class LifoidConfiguration(Configuration, LoggingMixin):
    """
    Meaningful defaults and required configurations.
    """
    # Main
    debug = False
    lifoid_id = environ_setting('LIFOID_ID', 'agent', required=False)
    lifoid_name = environ_setting('LIFOID_NAME', 'Bot', required=False)
    lifoid_settings_module = environ_setting('LIFOID_SETTINGS_MODULE',
                                             'agent.settings',
                                             required=False)
    # Authentication
    dev_auth = environ_setting('DEV_AUTH', 'no', required=False)

    # Database backends
    templates = environ_setting('TEMPLATES', 'fs', required=False)
    repository = environ_setting('REPOSITORY', 'dict', required=False)
    redis = RedisConfiguration()
    dynamodb = DynamoDBConfiguration()
    server = ServerConfiguration()
    context_prefix = environ_setting('CONTEXT_PREFIX',
                                     'lifoid-context', required=False)
    message_prefix = environ_setting('MESSAGE_PREFIX',
                                     'lifoid-message', required=False)
    model_prefix = environ_setting('MODEL_PREFIX',
                                   'lifoid-model', required=False)
    template_prefix = environ_setting('TEMPLATE_PREFIX',
                                      'lifoid-template', required=False)
    bot_prefix = environ_setting('BOT_PREFIX',
                                 'lifoid-bot', required=False)
    # Processing mode
    async = environ_setting('ASYNC', 'no', required=False)
    timeout = int(environ_setting('TIMEOUT', 180, required=False))

    # Misc
    language = environ_setting('LANGUAGE', 'en', required=False)
    web_static_bucket = environ_setting('WEB_STATIC_BUCKET',
                                        '', required=False)
    unified_events = environ_setting('UNIFIED_EVENTS',
                                     'false', required=False)

    # Logging
    logfile = environ_setting('LOGGING_FILE', 'lifoid.log', required=False)
    loglevel = environ_setting('LOGGING_LEVEL', 'INFO', required=False)


# Load settings immediately for import
settings = LifoidConfiguration()


if __name__ == '__main__':
    print(settings)
