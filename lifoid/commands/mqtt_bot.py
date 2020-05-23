import json
import traceback
import paho.mqtt.client as mqtt
from commis import Command, color
from lifoid import Lifoid
from lifoid.constants import HEADER
from lifoid.message import LifoidMessage
from lifoid.message.message_types import CHAT, M2M
from lifoid.renderer.mqtt import MQTTRenderer


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, _flags, result_code):
    print(
        color.format("Connected with result code "+str(result_code),
                     color.BLUE))
    print(HEADER)
    print(color.format('* I am {}'.format(
        userdata['lifoid_id']), color.GREEN))
    client.subscribe('#', 1)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when am PUBLISH message is received from the server.
def on_message(_client, userdata, mqtt_msg):
    lifoid_obj = Lifoid(
        lifoid_id=userdata['lifoid_id'],
        renderer=MQTTRenderer()
    )
    try:
        # Identify the message type
        json_loaded = json.loads(mqtt_msg.payload.decode('utf-8'))
        if (isinstance(json_loaded, dict) and \
            json_loaded['message_type'] == CHAT):
            lifoid_msg = LifoidMessage(**json_loaded)
            if lifoid_msg.to_user == userdata['lifoid_id']:
                lifoid_obj.logger.info(
                    'Request {}'.format(mqtt_msg.payload.decode('utf-8'))
                )
                lifoid_obj.reply(lifoid_msg, reply_id=mqtt_msg.topic)
        else:
            lifoid_msg = LifoidMessage(
                topic=mqtt_msg.topic,
                payload=mqtt_msg.payload.decode('utf-8'),
                lifoid_id=userdata['lifoid_id'],
                message_type=M2M
            )
            lifoid_obj.reply(lifoid_msg, reply_id=mqtt_msg.topic)
    except Exception:
        lifoid_obj.logger.error(traceback.format_exc())


class MQTTBotCommand(Command):
    name = 'mqtt_bot'
    help = 'Launch MQTT Lifoid Bot'
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
            'help': 'unique id of lifoid chatbot',
            'default': 'bot'
        }
    }

    def handle(self, args):
        try:
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
