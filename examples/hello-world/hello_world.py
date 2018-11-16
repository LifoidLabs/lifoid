import os
from lifoid import Lifoid
from lifoid.action import action
from lifoid.message import LifoidMessage, Payload
from lifoid.message.message_types import CHAT
from lifoid.renderer import Renderer


LIFOID_ID = 'hello_world'


class HelloWorldRenderer(Renderer):
    """
    Stdout renderer
    """
    def render(self, messages, receiver_id):
        for message in self.convert(messages):
            print('--> {}'.format(message.payload))

    def convert(self, messages):
        return messages


@action(lambda message, context: 'hello' in message.payload and
        message.message_type == CHAT)
def hello_world(render, _message, _context):
    """
    Simply say hello
    """
    return render([
        LifoidMessage(
            message_type=CHAT,
            payload='hello world'
        )
    ])


lifoid = Lifoid(LIFOID_ID, actions=[hello_world],
                renderer=HelloWorldRenderer())

# Say Hello
resp = lifoid.reply(
    LifoidMessage(
        payload=Payload(text='hello'),
        message_type=CHAT
    )
)

# --> hello world