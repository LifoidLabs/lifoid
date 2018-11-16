"""
Lifoid main application
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import sys
from six import add_metaclass, string_types
from loggingmixin import LoggingMixin
from singleton import Singleton
import lifoid.signals as signals


@add_metaclass(Singleton)
class Plugator(LoggingMixin):
    def __init__(self, plugins, plugins_paths, conf):
        self._plugins_paths = plugins_paths
        self._plugins = []
        self.logger.debug('Temporarily adding PLUGIN_PATHS to system path')
        _sys_path = sys.path[:]
        self.init_paths(plugins_paths)
        self.init_plugins(plugins)
        self.logger.debug('Restoring system path')
        sys.path = _sys_path
        signals.get_conf.send(conf)

    def init_paths(self, plugins_paths):
        if self._plugins_paths is not None:
            for pluginpath in self._plugins_paths:
                sys.path.insert(0, pluginpath)

    def init_plugins(self, plugins):
        if plugins is not None:
            for plugin in plugins:
                # if it's a string, then import it
                if isinstance(plugin, string_types):
                    self.logger.debug("Loading plugin `%s`", plugin)
                    try:
                        plugin = __import__(plugin, globals(), locals(),
                                            str('module'))
                    except ImportError as e:
                        self.logger.error(
                            "Cannot load plugin `%s`\n%s", plugin, e)
                        continue

                self.logger.debug("Registering plugin `%s`", plugin.__name__)
                plugin.register()
                self._plugins.append(plugin)

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
