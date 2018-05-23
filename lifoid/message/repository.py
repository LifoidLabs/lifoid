"""
webhook handler
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
from jsonrepo.repository import Repository
from lifoid.config import settings
from lifoid.message import Message


class MessageRepository(Repository):
    """
    Messages Repository
    """
    backend = settings.repository
    prefix = settings.message_prefix
    klass = Message
    key = settings.key
    sort_key = settings.sort_key