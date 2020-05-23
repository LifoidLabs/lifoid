""""
Special CLI oriented renderer for talk command
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018-2018 Romary Dupuis
"""
import boto3
from lifoid.renderer import Renderer
from lifoid.loggingmixin import LoggingMixin
from lifoid.utils.asdict import namedtuple_asdict


IOT_CLIENT = boto3.client('iot-data', region_name='eu-west-1')


class Renderer(Renderer, LoggingMixin):
    """
    Prototype of Lifoid renderer
    """
    api = 'lifoid'

    def convert(self, messages):
        return messages

    def render(self, messages, receiver_id):
        for msg in self.convert(messages):
            import json
            self.logger.debug(
                'Response: {}'.format(json.dumps(namedtuple_asdict(msg))))
            response = IOT_CLIENT.publish(
                topic='multibot/{}'.format(receiver_id),
                qos=1,
                payload=json.dumps(namedtuple_asdict(msg))
            )

