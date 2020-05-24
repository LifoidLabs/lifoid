"""
Translator definition
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2018 Romary Dupuis
"""
from lifoid.logging.mixin import LoggingMixin


class Translator(lifoid.loggingmixin):
    """
    Definition of translator
    """
    def translate(self, query, target, source, _dirty):
        """
        Generic translate method
        """
        raise NotImplementedError