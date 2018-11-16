from lifoid.action import action
from lifoid.views import render_view
from lifoid.automaton import Automaton
from loggingmixin import LoggingMixin


STATES = ['ready', 'ask_name']
TRANSITIONS = [
    {
        'trigger': 'greeting', 'source': 'ready',
        'dest': '=',
        'unless': 'user_unknown',
        'after': 'say_hello'
    },
    {
        'trigger': 'greeting', 'source': 'ready',
        'dest': 'ask_name', 'conditions': ['user_unknown'],
        'after': ['say_hello', 'ask_name']
    },
    {
        'trigger': 'user_name', 'source': 'ask_name',
        'dest': 'ready',
        'after': ['store_name', 'say_hello']
    },
    {
        'trigger': 'unknown', 'source': 'ask_name',
        'dest': '=', 'conditions': ['ask_name_counter'],
        'after': ['ask_name']
    },
    {
        'trigger': 'unknown', 'source': '*',
        'dest': 'ready',
        'after': ['dont_understand']
    }
]


class MQTTBot(Automaton, LoggingMixin):
    """
    Example of automaton based MQTT Bot
    """
    def __init__(self, lifoid_id):
        self.states = STATES
        self.transitions = TRANSITIONS
        self.initial = 'ready'
        super(MQTTBot, self).__init__(lifoid_id)

    def user_unknown(self, _render, _message):
        return self.get('name', None) is None

    def store_name(self, _render, message):
        parsed_message = message.payload.text.split(' ')
        self['name'] = parsed_message[-1]
        return True

    def say_hello(self, render, _message):
        self['ask_name_counter'] = 0
        return render_view(render, 'hello.yml', context=self)

    def ask_name(self, render, _message):
        self['ask_name_counter'] += 1
        return render_view(render, 'ask_name.yml', context=self)

    def ask_name_counter(self, _render, _message):
        return bool(self['ask_name_counter'] < 4)

    def dont_understand(self, render, _message):
        return render_view(render, 'dont_understand.yml', context=self)


@action(lambda message, _: 'hello' in message.payload.text)
def greeting(render, message, mqtt_bot):
    mqtt_bot.greeting(render, message)


@action(lambda message, _: 'name' in message.payload.text)
def user_name(render, message, mqtt_bot):
    mqtt_bot.user_name(render, message)


@action()
def unknown(render, message, mqtt_bot):
    mqtt_bot.unknown(render, message)
