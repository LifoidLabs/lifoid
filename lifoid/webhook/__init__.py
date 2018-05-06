"""
Simple Lifoid message handler
Author: Romary Dupuis <romary@me.com>
Copyright (C) 2018 Romary
"""
import lifoid.signals as signals
from lifoid.webhook.handler import Handler


def get_handler(app):
    return Handler()


def register():
    signals.get_handler.connect(get_handler)