from lifoid.action import action
from lifoid.message import LifoidMessage, Chat
from lifoid.message.message_types import UNKNOWN, CHAT


@action(lambda message, context: 'hello' in message.payload.text.lower())
def hello(render, message, context):
    return render([
        LifoidMessage(
            payload=Chat(text='Hello, what is your name?'),
            message_type=CHAT
        )
    ])


@action(lambda message, context: 'name' in message.payload.text.lower())
def name(render, message, context):
    tokens = message.payload.text.split()
    context['name'] = tokens[len(tokens) - 1]
    return render([
        LifoidMessage(
            payload=Chat(text='Hello {}'.format(context['name'])),
            message_type=CHAT
        )
    ])


@action(lambda message, _: message.type == UNKNOWN)
def unknown(render, message, context):
    return render([LifoidMessage(
        payload=Chat(text='Unkwnon message type'),
        message_type=CHAT
    )])
