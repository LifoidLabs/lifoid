"""
API that allows to retrieve user's messages
"""
import traceback
import json
from decimal import Decimal
from flask import Blueprint, request, make_response, jsonify, abort
from loggingmixin import ServiceLogger
from lifoid.message.repository import MessageRepository
from lifoid.utils.asdict import namedtuple_asdict
from lifoid.auth import get_user
from lifoid.config import settings
logger = ServiceLogger()

messages = Blueprint('messages', __name__)

JSONEncoder_olddefault = json.JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, Decimal):
        return str(o)
    return JSONEncoder_olddefault(self, o)


json.JSONEncoder.default = JSONEncoder_newdefault


@messages.route('/messages', methods=['POST'])
def index():
    """
    Retrieve user's messages from a specified datetime
    """
    logger.debug('Blueprint messages invoked')
    data = json.loads(request.get_data())
    user = get_user(data)
    if user is None:
        abort(403)
    try:
        rep = MessageRepository(settings.repository,
                                settings.message_prefix)
        if 'from_date' in data:
            response = rep.history(
                '{}:{}'.format(data['chatbot_id'], user['username']),
                _from=data['from_date'],
                _desc=False)
        else:
            response = rep.history(
                '{}:{}'.format(data['chatbot_id'], user['username']),
                _to=data['to_date'],
                _desc=True)
        logger.debug('messages: {}'.format(response))
        return jsonify([namedtuple_asdict(message) for message in response])
    except KeyError:
        logger.error('Missing key argument')
        logger.error(traceback.format_exc())
        return make_response('Missing key argument', 404)
    except:
        logger.error(request.get_data())
        logger.error(traceback.format_exc())
        return make_response('', 500)
