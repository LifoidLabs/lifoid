"""
Generic webhook handler for Lifoid
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import datetime
from multiprocessing import Process
from six import add_metaclass
from singleton import Singleton
from loggingmixin import LoggingMixin
from lifoid import Lifoid
from lifoid.message.message_types import TEXT
from lifoid.message import LifoidMessage, Payload
from lifoid.constants import E_POST
from lifoid.webhook.renderer import Renderer
from lifoid.exceptions import LifoidRequestForbiddenError
from lifoid.auth import get_user
from loggingmixin import ServiceLogger
logger = ServiceLogger()


def process_event(event):
    """
    Make sure the processing of the request is asynchronous.
    """
    msg = LifoidMessage(
        from_user=event['user']['username'],
        to_user='lifoid',
        payload=Payload(text=event['q']['text'],
                        attachments=event['q'].get('attachments', None)),
        type=TEXT,
        date=event['date'],
    )
    return Lifoid(
        lifoid_id=event['chatbot_id'],
        lang=event.get('lang', 'en'),
        renderer=Renderer()
    ).reply(msg, event['user']['username'],
            context_id='simple:{}'.format(event['user']['username']))


@add_metaclass(Singleton)
class Handler(LoggingMixin):
    """
    Proposes a simplified protocol for our own IM independant
    applications.
    """
    def process(self, e_type, event, async):
        """
        Checks if the event is compliant with our simple protocol and
        returns a response
        """
        if e_type == E_POST and 'q' in event and 'access_token' in event\
           and 'chatbot_id' in event:
            user = get_user(event)
            if user is None:
                raise LifoidRequestForbiddenError()
            event['date'] = datetime.datetime.utcnow().isoformat()[:-3]
            if async:
                try:
                    from zappa.async import run
                    run(process_event, args=(event,))
                except ModuleNotFoundError:
                    p_reply = Process(target=process_event,
                                      args=(event,))
                    p_reply.start()
            else:
                process_event(event)
            return event['date']
