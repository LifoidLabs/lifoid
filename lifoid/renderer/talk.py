# Special CLI oriented renderer for talk command
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
from commis import color
from lifoid.renderer import Renderer
from lifoid.message import LifoidMessage, ButtonAction, MenuAction


class TalkRenderer(Renderer):
    """
    Special CLI oriented renderer for talk command
    """
    api = 'talk'

    def convert(self, messages):
        return messages

    def render(self, messages, receiver_id):
        for msg in self.convert(messages):
            # print('< {}'.format(msg))
            print(color.format(
                '< %s' % (msg.replace('{', '{{').replace('}', '}}')),
                color.CYAN))


class SimpleToTalkRenderer(TalkRenderer):
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
                            output.append(','.join(table.columns))
                            for row in table.rows:
                                output.append(
                                    ','.join([row[key] for key in row.keys()]))
            else:
                return output.append(message)
        return output
