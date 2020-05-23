# Make a new chat bot project
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis

import traceback
import os
from commis import Command, color
from lifoid.constants import HEADER
from lifoid.views import TemplatesLoader

PROJECT_TEMPLATE_PATH = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../app/')
SETTINGS_MODULE = 'settings.py'
SETTINGS_TEMPLATE = 'settings_template.py'
ACTIONS_MODULE = 'actions.py'
ACTIONS_TEMPLATE = 'actions_template.py'
ROUTER_MODULE = 'router.py'
ROUTER_TEMPLATE = 'router_template.py'
PROJECT_NAME = 'bot'


class InitCommand(Command):

    name = 'init'
    help = 'initialize a chatbot project'
    template_loader = TemplatesLoader('lifoid', 'app')

    def mkdir(self, path):
        os.makedirs(path)

    def make_env(self, path, name):
        print(color.format('create .env', color.CYAN))
        h = open(os.path.join(path, '.env'), 'w')
        h.write('LIFOID_SETTINGS_MODULE={}.settings'.format(name))
        h.write('LOGGING_LEVEL=INFO')
        h.write('LOGGING_SERVICE=lifoid')
        h.write('LOGGING_HANDLERS=console,logfile')
        h.write('LOGGING_DEBUG=no')
        h.close()

    def make_project_dir(self, path):
        print(color.format('create {}'.format(path), color.CYAN))
        self.mkdir(path)

    def render_template(self, name, **kwargs):
        template = self.template_loader.get_template(name)
        content = template.render(**kwargs)
        return content

    def make_template(self, path, name, template, **kwargs):
        handle = open(os.path.join(path, name), 'w')
        handle.write(self.render_template(template, **kwargs))
        handle.close()

    def make_settings(self, path, templates_path, project_name):
        print(color.format('create settings.py', color.CYAN))
        self.make_template(path, SETTINGS_MODULE, SETTINGS_TEMPLATE,
                           project_name=project_name,
                           templates_path=templates_path)

    def make_router(self, path, project_name):
        print(color.format('create router.py', color.CYAN))
        self.make_template(path, ROUTER_MODULE, ROUTER_TEMPLATE,
                           project_name=project_name)

    def make_actions(self, path):
        print(color.format('create actions.py', color.CYAN))
        self.make_template(path, ACTIONS_MODULE, ACTIONS_TEMPLATE)

    def make_project(self, cwd, name):
        self.make_env(cwd, name)
        project_path = os.path.join(cwd, name)
        templates_path = os.path.join(project_path, 'templates')
        self.make_project_dir(project_path)
        h = open(os.path.join(project_path, '__init__.py'), 'w')
        h.close()
        self.make_project_dir(templates_path)
        self.make_settings(project_path, templates_path, name)
        self.make_router(project_path, name)
        self.make_actions(project_path)

    def handle(self, args):
        """
        CLI to generate a default lifoid agent project
        """
        print(HEADER)
        print(color.format('* initializing projet',
                           color.CYAN))
        try:
            cwd = os.getcwd()
            self.make_project(cwd, PROJECT_NAME)
        except:
            print(traceback.format_exc())
            return color.format('* error while creating the project', color.RED)
        return color.format('* project initialized',
                            color.GREEN)
