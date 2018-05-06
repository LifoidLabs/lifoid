"""
Translator definition
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2018 Romary Dupuis
"""
from loggingmixin import LoggingMixin


class Translator(LoggingMixin):
    """
    Definition of translator
    """
    def translate(self, query, target, source, _dirty):
        """
        Generic translate method
        """
        raise NotImplementedError