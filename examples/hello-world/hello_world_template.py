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
    Depending on the templates you want to use: YAML or TXT
    you get either messages as Chat objects or raw text
    """
    def render(self, messages, receiver_id):
        for message in self.convert(messages):
            if isinstance(message.payload, Chat):
                print('--> {}'.format(message.payload.text))
            else:
                print('--> {}'.format(message.payload))

    def convert(self, messages):
        return messages


@action(lambda message, context: 'Bob' in message.payload.text and
        message.message_type == CHAT)
def hello_bob(render, _message, _context):
    """
    Simply say hello to Bob
    We are using a YAML template with a Chat object, see ./templates/hello.yml
    """
    return render_view(render, 'hello.yml', context={'name': 'Bob'})


@action(lambda message, context: 'John' in message.payload.text and
        message.message_type == CHAT)
def hello_john(render, _message, _context):
    """
    Simply say hello to John
    We are using a TXT template with a raw output text
    see ./templates/hello.txt
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
# --> hello John

# Hello John
resp = lifoid.reply(
    LifoidMessage(
        payload=Chat(text='I am John'),
        message_type=CHAT
    )
)
# --> hello John
