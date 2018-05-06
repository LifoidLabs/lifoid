import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
ROUTER_CONF = 'agent.router'
TEMPLATES_PATH = os.path.join(PROJECT_ROOT, 'templates')
TRANSLATIONS_PATH = os.path.join(PROJECT_ROOT, 'translations')
NODES_PATH = os.path.join(PROJECT_ROOT, 'nodes')
TESTS_PATH = os.path.join(PROJECT_ROOT, 'tests')
PLUGIN_PATHS = []
PLUGINS = [
    'lifoid.webhook',
]