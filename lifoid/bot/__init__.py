"""
Bot definition
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import os
import binascii
import json
from lifoid.data.record import DictRecord
from lifoid.loggingmixin import LoggingMixin
from lifoid.config import settings

CTXT_ID_LENGTH = 12


class Bot(dict, DictRecord, LoggingMixin):
    """
    Bot object
    """
    VERSION = 0

    @classmethod
    def from_json(cls, json_dump):
        """
        How to get a context from a json dump
        """
        ctxt = json.loads(json_dump)
        if 'lifoid_id' not in ctxt:
            ctxt['lifoid_id'] = settings.lifoid_id
        context = cls(ctxt['lifoid_id'])
        for k in ctxt:
            context[k] = ctxt[k]
        return context

    def __init__(self, lifoid_id):
        self['__id__'] = str(binascii.hexlify(os.urandom(CTXT_ID_LENGTH)))
        self['__version__'] = Bot.VERSION
        self['__type__'] = self.__class__.__name__
        self['__lang__'] = settings.language
        self['lifoid_id'] = lifoid_id