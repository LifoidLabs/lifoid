"""
Bot repository
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
from jsonrepo.repository import Repository
from lifoid.config import settings
from lifoid.bot import Bot


class BotRepository(Repository):
    """
    A place to store our bots
    """
    backend = settings.repository
    prefix = settings.context_prefix
    klass = Bot
    key = settings.dynamodb.key
    sort_key = settings.dynamodb.sort_key
