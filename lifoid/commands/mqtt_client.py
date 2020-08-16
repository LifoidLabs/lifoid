"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
from uuid import uuid4
import json
from commis import Command, color
import paho.mqtt.client as mqtt
from lifoid.constants import HEADER
from lifoid.config import settings


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, _flags, _result_code):
    #print(
    #    color.format("Connected with result code "+str(result_code),
    #                 color.BLUE))
    client.subscribe(
        '{}/{}'.format(userdata['lifoid_id'], userdata['user_id']),
        1)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(_client, userdata, msg):
    json_obj = json.loads(msg.payload.decode('utf-8'))
    if userdata['user_id'] in json_obj['to_user']:
        print('from {} --> {}'.format(
            json_obj['from_user'],
            json_obj['payload']['text']
        ))


class MQTTClientCommand(Command):

    name = 'mqtt_client'
    help = 'Talk to a lifoid MQTT bot'
    args = {
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
        """
        CLI to talk to lifoid
        """
        user_id = uuid4().hex
        mqtt_client = mqtt.Client(
            userdata={
                'lifoid_id': args.lifoid_id,
                'user_id': user_id
            }
        )
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        mqtt_client.connect(settings.mqtt.host, settings.mqtt.port, 60)

        mqtt_client.loop_start()
        print(HEADER)
        print(color.format('* PLease type in your messages below', color.GREEN))
        while True:
            try:
                input_msg = input()
            except KeyboardInterrupt:
                break
            if input_msg != 'exit':
                topic = '{}/{}'.format(args.lifoid_id,
                                       user_id)
                data = json.dumps({
                    'topic':topic,
                    'lifoid_id': args.lifoid_id,
                    'from_user': user_id,
                    'to_user': args.lifoid_id,
                    'payload': {
                        'text': input_msg,
                        'attachments': None
                    },
                    'message_type': 'chat'
                })
                mqtt_client.publish(topic, data)
            else:
                mqtt_client.loop_stop()
                break
        return color.format("* bye bye", color.RED)
