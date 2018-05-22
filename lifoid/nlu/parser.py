"""
Parser definition
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2018 Romary Dupuis
"""
from loggingmixin import LoggingMixin


class Parser(LoggingMixin):
    """
    Definition of parser
    """
    def parse(self, message, context):
        """
        Generic parse method
        """
        raise NotImplementedError