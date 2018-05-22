# Special CLI oriented renderer for talk command
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
from commis import color
from lifoid.renderer import Renderer
from lifoid.api.facebook.template import (TextMessage, ImageMessage,
                                          QuickReplyMessage, ButtonMessage,
                                          GenericMessage)
from lifoid.message import LifoidMessage, ButtonAction, MenuAction
from lifoid.exceptions import LifoidTestError

DONT_CARE = 'DONT_CARE'


class TestRenderer(Renderer):
    """
    Special CLI oriented renderer for test command
    """
    api = 'test'

    def __init__(self, response):
        self.response = response
        super(TestRenderer, self).__init__()

    def convert(self, messages):
        return messages

    def render(self, messages, receiver_id):
        resp_color = color.RED
        for msg in self.convert(messages):
            if self.response in msg:
                resp_color = color.GREEN
                break
        if DONT_CARE in self.response:
            resp_color = color.GREEN
        for msg in self.convert(messages):
            # print('< {}'.format(msg))
            print(color.format('< %s' % (msg
                                         .replace('{', '{{')
                                         .replace('}', '}}')),
                               resp_color))
        if resp_color == color.RED:
            raise LifoidTestError('\nexpected:\n{}\nreceived:\n{}'.format(
                self.response,
                '\n'.join(self.convert(messages))))


class SimpleToTestRenderer(TestRenderer):
    """
    Convert Facebook messages to Talk messages.
    """
    def convert(self, messages):
        # convert facebook message format to talk format
        output = []
        for message in messages:
            if isinstance(message, LifoidMessage):
                output.append(message.payload.text)
                if message.payload.attachments is not None:
                    for attachment in message.payload.attachments:
                        if attachment.actions is not None:
                            for action in attachment.actions:
                                if isinstance(action, ButtonAction):
                                    output.append('{} {} {} {}'.format(
                                        action.name,
                                        action.style,
                                        action.text,
                                        action.value))
                                if isinstance(action, MenuAction):
                                    for option in action.options:
                                        output.append('{} {}'.format(
                                            option.text, option.value))
                        if attachment.table is not None:
                            table = attachment.table
                            output.append('Table {}'. format(table.title))
                            output.append(table.columns)
                            output.append(table.rows)
            else:
                return output.append(message)
        return output


class FacebookToTestRenderer(TestRenderer):
    """
    Convert Facebook messages to TestRenderer messages.
    """
    def convert(self, messages):
        # convert facebook message format to talk format
        text = []
        for message in messages:
            if isinstance(message, TextMessage):
                text.append(message.text)
            if isinstance(message, ImageMessage):
                text.append(message.url)
            if isinstance(message, QuickReplyMessage):
                text.append(message.text)
                for quick_reply in message.quick_replies:
                    text.append(quick_reply.payload)
            if isinstance(message, ButtonMessage):
                text.append(message.text)
                for button in message.buttons:
                    text.append(button.title)
            if isinstance(message, GenericMessage):
                for element in message.elements:
                    text.append('{} {} {} {} {}'.format(
                        button.title,
                        button.item_url,
                        button.image_url,
                        button.subtitle,
                        [b.title for b in button.buttons
                         if button.buttons is not None])
                    )
        return text
