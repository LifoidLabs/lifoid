# -*- coding: utf8 -*-
"""
Storage Mixin
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017 Romary Dupuis
"""
from awesomedecorators import memoized
from lifoid.data.backends.redis import RedisBackend
from lifoid.data.backends.memory import DictBackend


class StorageMixin(object):
    """
    Mix in storage capacity with singleton
    """
    @memoized
    def storage(self):
        """
        Instantiates and returns a storage instance
        """
        if self.backend == 'redis':
            return RedisBackend(self.prefix, self.secondary_indexes)
        return DictBackend(self.prefix, self.secondary_indexes)
