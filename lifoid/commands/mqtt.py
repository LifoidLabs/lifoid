import json
import traceback
import paho.mqtt.client as mqtt
from paho.mqtt.publish import multiple
from commis import Command, color
from loggingmixin import LoggingMixin
from lifoid import Lifoid
from lifoid.utils.asdict import namedtuple_asdict
from lifoid.constants import HEADER
from lifoid.message import LifoidMessage, Payload
from lifoid.message.message_types import CHAT
from lifoid.renderer import Renderer


class MQTTRenderer(Renderer, LoggingMixin):
    """
    Prototype of Lifoid renderer
    """
    api = 'mqtt'

    def convert(self, messages):
        return messages

    def render(self, messages, receiver_id):
        msgs = []
        for msg in self.convert(messages):
            self.logger.debug(
                'Response: {}'.format(json.dumps(namedtuple_asdict(msg))))
            msgs.append(
                {
                    'topic': msg.to_user,
                    'payload': json.dumps(namedtuple_asdict(msg))
                }
            )
        multiple(msgs, hostname="localhost")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, _flags, result_code):
    print(
        color.format("Connected with result code "+str(result_code),
                     color.BLUE))
    print(HEADER)
    print(color.format('* I am listening {}'.format(
        userdata['lifoid_id']), color.GREEN))
    client.subscribe('#', 1)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when am PUBLISH message is received from the server.
def on_message(_client, userdata, msg):
    lifoid_obj = Lifoid(
        lifoid_id=userdata['lifoid_id'],
        renderer=MQTTRenderer()
    )
    try:
        # Identify the message type
        lifoid_obj.logger.debug(
                'MQTT {}'.format(msg.payload.decode('utf-8'))
            )
        json_loaded = json.loads(msg.payload.decode('utf-8'))
        if json_loaded['message_type'] == CHAT:
            msg = LifoidMessage(**json_loaded)
            msg.payload(LifoidMessage(**json_loaded['payload']))
        else:
            msg = LifoidMessage(
                topic=msg.topic,
                payload=msg.payload.decode('utf-8'),
                lifoid_id=userdata['lifoid_id']
            )
            lifoid_obj.reply(msg, msg.topic)
    except Exception:
        lifoid_obj.logger.error(traceback.format_exc())


class MQTTCommand(Command):
    name = 'mqtt'
    help = 'talk to lifoid via CLI'
    args = {
        '--host': {
            'metavar': 'ADDR',
            'default': 'localhost',
            'help': 'set the mqtt broker host'
        },
        '--port': {
            'metavar': 'PORT',
            'type': int,
            'default': 1883,
            'help': 'set the mqtt broker port'
        },
        '--debug': {
            'action': 'store_true',
            'required': False,
            'help': 'force debug mode'
        },
        '--lifoid_id': {
            'metavar': 'LIFOID_ID',
            'required': False,
            'help': 'unique id of lifoid chatbot'
        }
    }

    def handle(self, args):
        try:
            from lifoid.www.app import app
            with app.app_context():
                mqtt_client = mqtt.Client(
                    userdata={
                        'lifoid_id': args.lifoid_id
                    }
                )
                mqtt_client.on_connect = on_connect
                mqtt_client.on_message = on_message

                mqtt_client.connect(args.host, args.port, 60)

                mqtt_client.loop_forever()
        except KeyboardInterrupt:
            print(color.format('Keyboard interruption', color.RED))
        finally:
            mqtt_client.disconnect()
            print(color.format('Bye bye', color.RED))
