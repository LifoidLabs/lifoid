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


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, _flags, _result_code):
    #print(
    #    color.format("Connected with result code "+str(result_code),
    #                 color.BLUE))
    client.subscribe(userdata['lifoid_id'], 1)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(_client, userdata, msg):
    json_obj = json.loads(msg.payload.decode('utf-8'))
    if json_obj['to_user'] in [userdata['user_id'], '*']:
        print('from {} --> {}'.format(
            json_obj['from_user'],
            json_obj['payload']['text']
        ))


class ChatCommand(Command):

    name = 'chat'
    help = 'Chat with a lifoid bot via MQTT; A MQTT Broker must be available'
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
            'required': True,
            'help': 'unique id of lifoid chatbot'
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

        mqtt_client.connect(args.host, args.port, 60)

        mqtt_client.loop_start()
        print(HEADER)
        print(color.format('* PLease type in your messages below', color.GREEN))
        while True:
            try:
                input_msg = input()
            except KeyboardInterrupt:
                break
            if input_msg != 'exit':
                data = json.dumps({
                    'lifoid_id': args.lifoid_id,
                    'from_user': user_id,
                    'to_user': args.lifoid_id,
                    'payload': {
                        'text': input_msg,
                        'attachments': None
                    },
                })
                mqtt_client.publish(args.lifoid_id, data)
            else:
                mqtt_client.loop_stop()
                break
        return color.format("* bye bye", color.RED)
