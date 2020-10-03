import sys
import os
import json
import traceback
import importlib
from flask import request, make_response, Blueprint, abort
from lifoid.config import settings
from lifoid.logging.mixin import ServiceLogger
from lifoid.constants import E_GET, E_POST
from lifoid.events import process_event
from lifoid.exceptions import (LifoidRequestForbiddenError,
                               LifoidRequestUnknownError)
sys.path.insert(0, os.getcwd())
logger = ServiceLogger()
try:
    app_settings_module = importlib.import_module(
        settings.lifoid_settings_module
    )
    logger.debug('Templates path: {}'.format(
        app_settings_module.TEMPLATES_PATH))
    webhook = Blueprint('webhook', __name__,
                        template_folder=app_settings_module.TEMPLATES_PATH)
except ImportError:
    logger.error('No templates path configured')
    webhook = Blueprint('webhook', __name__)


@webhook.route('/webhook', methods=['GET', 'POST'])
def index():
    """
    Universal webhook endpoint for all messenger applications.
    """
    logger.debug('Webhook blueprint invoked')
    try:
        if request.method == 'POST':
            e_type = E_POST
            data = request.get_data()
            if data.startswith(b'payload'):
                event = json.loads(request.form['payload'])
            else:
                event = json.loads(request.get_data())
        elif request.method == 'GET':
            e_type = E_GET
            event = request.args
        else:
            return make_response('Request method not supported', 404)
        logger.debug('{} {}'.format(e_type, event))
        asynchronous = settings.pasync == 'yes'
        resp, perf = process_event(e_type, event, asynchronous)
        logger.info('Request processed in {}'.format(perf))
        if resp is not None:
            logger.debug('Http Response: {}'.format(resp))
            return make_response(resp, 200)
        return make_response('OK', 200)
    except KeyError:
        logger.error(traceback.format_exc())
        logger.error('Missing key argument')
        return make_response('Missing key argument', 404)
    except LifoidRequestForbiddenError:
        return abort(403)
    except LifoidRequestUnknownError:
        return make_response('Unknown request', 404)
    except:
        logger.error(request.get_data())
        logger.error(traceback.format_exc())
        return make_response('', 200)
