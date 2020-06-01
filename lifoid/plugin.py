"""
Lifoid main application
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import sys
from six import add_metaclass, string_types
from lifoid.logging.mixin import LoggingMixin
from singleton import Singleton
import lifoid.signals as signals
from lifoid.config import settings


@add_metaclass(Singleton)
class Plugator(LoggingMixin):
    def __init__(self):
        self._plugins_paths = []
        self._plugins = []

    def add_plugin_path(self, plugin_path):
        if plugin_path not in self._plugins_paths:
            self.logger.debug(f'add_plugin_path\t{plugin_path}')
            self._plugins_paths.append(plugin_path)
            sys.path.insert(0, plugin_path)

    def add_plugin(self, plugin):
        if isinstance(plugin, string_types):
            self.logger.debug(f'add_plugin_path\t{plugin}')
            try:
                plugin = __import__(plugin, globals(), locals(),
                                    str('module'))
                self.logger.debug("Registering plugin `%s`", plugin.__name__)
                plugin.register()
                self._plugins.append(plugin)
                self.logger.debug('Get plugin configuration')
                signals.get_conf.send(settings)
            except ImportError as e:
                self.logger.error(
                    "Cannot load plugin `%s`\n%s", plugin, e)

    def _init_paths(self, plugins_paths):
        for plugin_path in plugins_paths:
            self.add_plugin_path(plugin_path)

    def _init_plugins(self, plugins):
        if plugins is not None:
            for plugin in plugins:
                self.add_plugin(plugin)

    def register_plugin(self, plugin, plugin_path):
        self.add_plugin_path(plugin_path)
        self.add_plugin_path(plugin)

    def get_plugins(self, plugin, *args, **kwargs):
        return [w for (_, w) in plugin.send(*args, **kwargs)]

    def get_plugin(self, plugin, *args, **kwargs):
        plugins = [w for (_, w) in plugin.send(*args, **kwargs)]
        plugins_found = len(plugins)
        if plugins_found == 0:
            return None
        else:
            plugin = plugins[0]
            if plugins_found == 1:
                self.logger.debug('Found plugin: %s', plugin)
            else:
                self.logger.warning(
                    '%s plugins found, using only first one: %s',
                    plugins_found, plugin)
            return plugin


def init_plugins(self, plugins, plugins_path):
    if plugins is None:
        if self.app_settings_module is not None:
            self.plugins = self.app_settings_module.PLUGINS
            self.plugins_path = self.app_settings_module.PLUGIN_PATHS
    else:
        self.plugins = plugins
        if plugins_path is not None:
            self.plugins_path = plugins_path


plugator = Plugator()
