"""
setup.py for Lifoid module
"""
import os
import sys
import codecs
from setuptools import setup, find_packages

NAME = 'Lifoid'
DESCRIPTION = 'Lifoid - Light bot application development framework for Python'
AUTHOR = 'Romary Dupuis'
EMAIL = 'romary@me.com'
MAINTAINER = 'Romary Dupuis'
MAINTAINER_EMAIL = EMAIL
LICENSE = 'Apache 2.0'
REPOSITORY = 'https://github.com/romaryd/lifoid'
PACKAGE = 'lifoid'

KEYWORDS = ('chatbot', 'lifoid', 'AI', 'framework')

CLASSIFIERS = (
    'Programming Language :: Python',
    'Development Status :: 1 - Beta',
    'Natural Language :: English',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Utilities'
)

PROJECT = os.path.abspath(os.path.dirname(__file__))
REQUIRE_PATH = os.path.join(PROJECT, "requirements.txt")
VERSION_PATH = os.path.join(PACKAGE, "version.py")
EXCLUDES = (
    "tests", "bot"
)
PACKAGES = find_packages(PROJECT, exclude=EXCLUDES)


def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts),
                     'rb', 'utf-8') as source_file:
        return source_file.read()


def get_version(path=VERSION_PATH):
    """
    Reads the __init__.py defined in the VERSION_PATH to find the get_version
    function, and executes it to ensure that it is loaded correctly.
    """
    namespace = {}
    exec(read(path), namespace)
    return namespace['get_version']()


def get_requires(path=REQUIRE_PATH):
    """
    Yields a generator of requirements as defined by the REQUIRE_PATH which
    should point to a requirements.txt output by `pip freeze`.
    """
    for line in read(path).splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            yield line


CONFIG = {
    'name': NAME,
    'version': get_version(),
    'url': REPOSITORY,
    'license': LICENSE,
    'author': AUTHOR,
    'author_email': EMAIL,
    'maintainer': MAINTAINER,
    'maintainer_email': MAINTAINER_EMAIL,
    'install_requires': [
        'six',
        'python-singleton',
        'python-awesome-decorators',
        'python-dateutil',
        'python-jsonrepo',
        'dateparser',
        'python-dotenv',
        'commis',
        'colorama',
        'werkzeug',
        'flask',
        'flask_s3',
        'Flask-Babel',
        'flask-cors',
        'requests',
        'transitions',
        'PyYAML',
        'blinker',
        'paho-mqtt'
    ],
    'description': DESCRIPTION,
    'long_description': read('README.md'),
    'packages': PACKAGES,
    'include_package_data': True,
    'platforms': 'any',
    'entry_points': {
        'console_scripts': [
            'lifoid = lifoid.__main__:cli',
        ]
    },
    'classifiers': CLASSIFIERS,
    'keywords': KEYWORDS
}

if sys.argv[-1] == 'publish':
    if os.system('pip freeze | grep wheel'):
        print('wheel not installed.\nUse `pip install wheel`.\nExiting.')
        sys.exit()
    if os.system('pip freeze | grep twine'):
        print('twine not installed.\nUse `pip install twine`.\nExiting.')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    print('You probably want to also tag the version now:')
    print("  git tag -a {0} -m 'version {0}'".format(get_version('lifoid')))
    print('  git push --tags')
    sys.exit()


if __name__ == '__main__':
    setup(**CONFIG)
