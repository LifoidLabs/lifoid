"""
Launch lifoid server
Author:   Romary Dupuis <romary@me.com>
Copyright (C) 2017-2018 Romary Dupuis
"""
import traceback
from importlib import import_module
from commis import Command, color
from lifoid.views import (TemplateRepository, TemplateRecord,
                          load_templates_path)


def load_template(lifoid_id, path, lang):
    template_rep = TemplateRepository()
    for template in load_templates_path(path):
        record = TemplateRecord()
        record.update(template)
        template_rep.save('{}:{}:{}'.format(lifoid_id,
                                            template['name'],
                                            lang),
                          record['date'], record)


class LoadTemplatesCommand(Command):
    """
    CLI to load chabots templates in the repository
    """
    name = 'load_templates'
    help = 'Load templates in the repository'
    args = {
        '--path': {
            'metavar': 'PATH',
            'default': False,
            'help': 'path where template files are located'
        },
        '--lifoid_id': {
            'metavar': 'LIFOID_ID',
            'required': True,
            'help': 'unique id of lifoid chatbot'
        },
        '--lang': {
            'metavar': 'LANG',
            'required': True,
            'help': 'language of templates'
        }
    }

    def handle(self, args):
        """
        CLI to run the lifoid HTTP API server application.
        """
        from lifoid.config import settings
        try:
            app_settings_module = import_module(
                settings.lifoid_settings_module
            )
        except ModuleNotFoundError:
            color.format("No settings module found. Have you initialized your project with `lifoid init` command? ", color.RED)
        path = args.path or app_settings_module.TEMPLATES_PATH
        try:
            load_template(args.lifoid_id, path, args.lang)
        except Exception:
            print(traceback.format_exc())
            return color.format(" * Error while loading templates", color.RED)
        return color.format(" * Conversational model loaded", color.GREEN)
