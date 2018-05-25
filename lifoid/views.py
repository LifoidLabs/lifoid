#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis
"""
Template views system based on Jinja2
"""
from os import walk
from os.path import join
import yaml
import datetime
import time
from jinja2 import TemplateNotFound, Template
from flask import render_template as flask_render_template
from flask_babel import gettext as flask_gettext
from jsonrepo.repository import Repository
from jsonrepo.record import DictRecord
from lifoid.config import settings
from lifoid.message import (LifoidMessage, Attachment, ButtonAction, Option,
                            Table, MenuAction, Payload)
from loggingmixin import ServiceLogger
logger = ServiceLogger()

MSG_SPLIT = '1234567890ab'


def load_templates_path(path):
    for (dirpath, dirnames, filenames) in walk(path):
        for _file in filenames:
            logger.debug('load {}'.format(_file))
            with open(join(path, _file)) as file_handler:
                yield {
                    'name': _file,
                    'content': file_handler.read()
                }


class TemplateRecord(dict, DictRecord):
    """
    Generic Lifoid message
    """
    def __init__(self):
        date = datetime.datetime.utcnow().isoformat()[:-3]
        self['ttl'] = int(time.mktime(time.strptime(
            date, "%Y-%m-%dT%H:%M:%S.%f")))
        self['date'] = date


class TemplateRepository(Repository):
    """
    Messages Repository
    """
    klass = TemplateRecord


def get_template(lifoid_id, name, lang):
    template_key = '{}:{}:{}'.format(lifoid_id, name, lang)
    logger.debug('Get template {}'.format(template_key))
    template = TemplateRepository(
        settings.repository,
        settings.template_prefix).latest(template_key)
    if template is None:
        raise TemplateNotFound
    return Template(template['content'])


def lifoid_render_template(template_name, **kwargs):
    template = get_template(kwargs['lifoid_id'], template_name, kwargs['lang'])
    return template.render(**kwargs)


def template_extension(template_name):
    els = template_name.split('.')
    if len(els) > 1:
        return els[1]
    return False


def render_view(render, template_name, **kwargs):
    if template_extension(template_name) == 'yaml':
        return render(get_yaml_view(template_name, **kwargs))
    else:
        return render(get_text_view(template_name, **kwargs))


def get_yaml_view(template_name, **kwargs):
    try:
        content = yaml.load(render_template(template_name, **kwargs))
        attachments = []
        if 'attachments' in content:
            for attachment in content['attachments']:
                if 'file_url' in attachment.keys():
                    attachments.append(Attachment(
                        file_url=attachment['file_url'],
                        text=attachment['text']))
                if 'buttons' in attachment.keys():
                    actions = []
                    for button in attachment['buttons']:
                        if isinstance(button, dict):
                            actions.append(ButtonAction(name=button['text'],
                                                        value=button['value']))
                        else:
                            actions.append(ButtonAction(name=button))
                    attachments.append(Attachment(actions=actions))
                if 'select' in attachment.keys():
                    options = []
                    for option in attachment['select']:
                        if isinstance(option, dict):
                            options.append(
                                Option(text=option['text'],
                                       value=option.get('value',
                                                        option['text']))
                            )
                        else:
                            options.append(Option(text=option, value=option))
                    attachments.append(Attachment(actions=[
                        MenuAction(name='menu_select', options=options)
                    ]))
                if 'table' in attachment.keys():
                    attachments.append(Attachment(table=Table(
                        title=attachment['table']['title'],
                        name=attachment['table']['name'],
                        columns=attachment['table']['columns'],
                        rows=attachment['table']['rows'],
                        types=attachment['table']['types']
                    )))
    except KeyError:
        logger.error('malformed content in template {}'.format(template_name))
        raise
    except AttributeError:
        logger.error('malformed content in template {}'.format(template_name))
        raise
    except yaml.parser.ParserError:
        logger.error('malformed content in template {}'.format(template_name))
        raise
    return [LifoidMessage(
        payload=Payload(
            text=content['text'],
            attachments=attachments))]


def get_text_view(template_name, **kwargs):
    """
    Render a template view with a specific context
    """
    content = render_template(template_name, MSG_SPLIT=MSG_SPLIT, **kwargs)
    return [LifoidMessage(
        payload=Payload(
            text=text,
            attachments=None)) for text in content.split(MSG_SPLIT)]


gettext = flask_gettext
if settings.templates == 'repository':
    render_template = lifoid_render_template
else:
    render_template = flask_render_template
