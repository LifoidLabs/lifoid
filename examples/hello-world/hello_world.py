import os
from lifoid import Lifoid
from lifoid.action import action
from lifoid.message import LifoidMessage
from lifoid.message.message_types import TXT
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


@action(lambda message, context: message.message_type == TXT and
        'hello' in message.payload)
def hello_world(render, _message, _context):
    """
    Simply say hello
    """
    return render([
        LifoidMessage(
            message_type=TXT,
            payload='hello world'
        )
    ])


lifoid = Lifoid(LIFOID_ID, actions=[hello_world],
                renderer=HelloWorldRenderer())

# Say Hello
resp = lifoid.reply(
    LifoidMessage(
        payload='hello',
        message_type=TXT
    )
)

# --> hello world