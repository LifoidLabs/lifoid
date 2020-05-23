import datetime
import time
from collections import namedtuple
from lifoid.data.record import NamedtupleRecord
from lifoid.loggingmixin import LoggingMixin
from lifoid.message.message_types import CHAT, TXT

_fields = ['date', 'ttl', 'from_user', 'to_user', 'payload',
           'message_type', 'lifoid_id', 'topic', 'type']


class Message(namedtuple('Message', _fields), NamedtupleRecord, LoggingMixin):
    """
    Generic Lifoid message
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _fields}
        default.update(kwargs)
        if default['date'] is None:
            default['date'] = datetime.datetime.utcnow().isoformat()[:-3]
        if default['ttl'] is None:
            default['ttl'] = int(time.mktime(time.strptime(
                default['date'], "%Y-%m-%dT%H:%M:%S.%f")))
        # backward compatibility
        if 'type' in kwargs.keys() and 'message_type' not in kwargs.keys():
            default['message_type'] = default['type']
        if (isinstance(default['payload'], dict) and \
            default['message_type'] == CHAT):
            default['payload'] = Chat(**default['payload'])
        if default['message_type'] == TXT:
            default['payload'] = default['payload']
        return super(Message, cls).__new__(
            cls, **default)


_chat_fields = ['text', 'attachments']


class Chat(namedtuple('Chat', _chat_fields)):
    def __new__(cls, **kwargs):
        default = {f: None for f in _chat_fields}
        default.update(kwargs)
        #if isinstance(default['attachments'], dict):
        #    default['attachments'] = Attachment(**default['attachments'])
        return super(Chat, cls).__new__(
            cls, **default)


_attachment_fields = [
    'text', 'image_url', 'actions', 'table', 'file_url', 'edit']


class Attachment(namedtuple('Attachment', _attachment_fields)):
    """
    Attachment field
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _attachment_fields}
        default.update(kwargs)
        return super(Attachment, cls).__new__(
            cls, **default)


_edit_fields = [
    'action', 'text', 'translation'
]


class Edit(namedtuple('Table', _edit_fields)):
    """
    Edit action
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _edit_fields}
        default.update(kwargs)
        return super(Edit, cls).__new__(
            cls, **default)


_table_fields = [
    'title', 'name', 'style', 'columns', 'rows', 'types'
]


class Table(namedtuple('Table', _table_fields)):
    """
    Table
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _table_fields}
        default.update(kwargs)
        return super(Table, cls).__new__(
            cls, **default)


_action_fields = [
    'action_type', 'name', 'text', 'style', 'value', 'options'
]


class Action(namedtuple('Action', _action_fields)):
    """
    Action
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _action_fields}
        default.update(kwargs)
        return super(Action, cls).__new__(
            cls, **default)


class ButtonAction(Action):
    """
    Specific action to get a button
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _action_fields}
        default.update(kwargs)
        default['action_type'] = 'button'
        if default['style'] is None:
            default['style'] = 'default'
        if (default['text'] is None and default['value'] is None and
           default['name'] is not None):
            default['text'] = default['value'] = default['name']
        return super(ButtonAction, cls).__new__(
            cls, **default)


class MenuAction(Action):
    """
    Specific action to get a selection menu
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _action_fields}
        default.update(kwargs)
        default['action_type'] = 'select'
        return super(MenuAction, cls).__new__(
            cls, **default)


_option_group_fields = ['text', 'options']


class OptionGroup(namedtuple('Option', _option_group_fields)):
    """
    Group of selection options
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _option_group_fields}
        default.update(kwargs)
        return super(OptionGroup, cls).__new__(
            cls, **default)


_option_fields = ['text', 'value']


class Option(namedtuple('Option', _option_fields)):
    """
    Option
    """
    def __new__(cls, **kwargs):
        default = {f: None for f in _option_fields}
        default.update(kwargs)
        return super(Option, cls).__new__(
            cls, **default)


class LifoidMessage(Message):
    """
    Get NLU add useful information to a message
    """
    def __new__(cls, **kwargs):
        return super(LifoidMessage, cls).__new__(
            cls, **kwargs)

    def __init__(self, **kwargs):
        self.parsed = False
        self.translated = False

    def parse(self, parser, context):
        """
        gets insight from NLU engine
        """
        if parser is None:
            return None

        self.logger.debug('Parse: {}'.format(self.payload.text))
        if self.translated:
            self.parsed = parser.parse(self.translated, context)
        else:
            self.parsed = parser.parse(self.payload.text, context)

    def translate(self, translator, _from, _to):
        if translator is None:
            return
        results = translator.translate(self.payload.text, source=_from,
                                       target=_to)
        self.logger.debug('translation: {}'.format(results))
        if len(results) > 0:
            self.translated = \
                results[0]['translatedText'].replace(
                    '&#39;',
                    '\'')
        self.logger.debug('Translation ({} -> {}): {} -> {}'.format(
            _from,
            _to,
            self.payload.text,
            self.translated)
        )
