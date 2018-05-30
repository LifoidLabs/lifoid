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
    klass = Bot
    sort_key = ''
