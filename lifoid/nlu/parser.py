"""
Parser definition
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2018 Romary Dupuis
"""
from lifoid.logging.mixin import LoggingMixin


class Parser(lifoid.loggingmixin):
    """
    Definition of parser
    """
    def parse(self, message, context):
        """
        Generic parse method
        """
        raise NotImplementedError