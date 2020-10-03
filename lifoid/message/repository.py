"""
webhook handler
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
from lifoid.data.repository import Repository
from lifoid.message import Message


class MessageRepository(Repository):
    """
    Messages Repository
    """
    klass = Message
    secondary_indexes = ['lifoid_id', 'ttl']
