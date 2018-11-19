from lifoid import Lifoid
from lifoid.action import action
from lifoid.message import LifoidMessage, Chat
from lifoid.message.message_types import CHAT
from lifoid.renderer import Renderer
from lifoid.views import render_view


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


@action(lambda message, context: 'Bob' in message.payload.text and
        message.message_type == CHAT)
def hello_bob(render, _message, _context):
    """
    Simply say hello
    """
    return render_view(render, 'hello.yml', context={'name': 'Bob'})


@action(lambda message, context: 'John' in message.payload.text and
        message.message_type == CHAT)
def hello_john(render, _message, _context):
    """
    Simply say hello
    """
    return render_view(render, 'hello.txt', context={'name': 'John'})


lifoid = Lifoid(LIFOID_ID, actions=[hello_bob, hello_john],
                renderer=HelloWorldRenderer())

# Hello Bob
resp = lifoid.reply(
    LifoidMessage(
        payload=Chat(text='I am Bob'),
        message_type=CHAT
    )
)
# --> {'text': 'hello Bob'}

# Hello John
resp = lifoid.reply(
    LifoidMessage(
        payload=Chat(text='I am John'),
        message_type=CHAT
    )
)
# --> hello John
