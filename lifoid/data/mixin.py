# -*- coding: utf8 -*-
"""
Storage Mixin
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017 Romary Dupuis
"""
from awesomedecorators import memoized
from lifoid.logging.mixin import LoggingMixin


class StorageMixin:
    """
    Mix in storage capacity with singleton
    """
    @memoized
    def storage(self):
        """
        Instantiates and returns a storage instance
        """
        self.logger.debug(f'backend\t{self.backend}')
        self.logger.debug(f'prefix\t{self.prefix}')
        self.logger.debug(f'secondary_indexes\t{self.secondary_indexes}')
        return self.backend(
            self.prefix,
            self.secondary_indexes
        )
