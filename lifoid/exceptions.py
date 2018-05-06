# Exceptions
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis

from __future__ import unicode_literals


class LifoidError(Exception):
    """The root of all errors in lifoid library"""
    pass


class LifoidRequestUnknownError(LifoidError):
    pass


class LifoidRequestForbiddenError(LifoidError):
    pass


class LifoidTestError(Exception):
    """Raised when a test fails"""
    pass


class LifoidCmdError(LifoidError):
    """Base exceptions for all lifoid command Exceptions"""
    pass


class ConfigurationError(LifoidCmdError):
    """Error in configuration of lifoid command"""
    pass


class TimeoutError(Exception):
    """
    An operation timed out
    """
    pass