# lifoid #

**Simple and flexible bot application development framework for the IoT**

(Project initialization is on-going: cleaning up source code, making tests suite, writing proper documentation)

---

## Vision ##

Unlike most of chatbot development frameworks, we consider that a chatbot must
be able to deal with messages that are not only conversation based, e.g. we
would like to deal with messages from the IoT, sensors and actuators. A bot
application in the Internet of Things must be able to combine interactions with
humans and machines at the same time.

## Features ##

Lifoid provides:
- a message routing system that looks like Flask routing for urls.
- a message pipeline system for NLU processing and automatic translation
- a context management system that expends from a simple object to a full
FSM based automaton. Context objects are stored and retrieved from key/value
stores either in process memory, on Redis or Dynamodb.
- services for:
  - deploying a mqtt based bot
  - chatting with a bot using mqtt
  - chatting with a bot using an HTTP API
  - accessing chat messages log using an HTTP API

## Quick Start ##

You should look at the examples provided in this repository.

Lifoid provides both a programmatic interface and servicesi, whose
full documentation will be provided below (soon).

## Installation ##

```bash
$ pip install lifoid
```

## How to make a bot project ##

After installing Lifoid:

**Start a project**

The command line:
```bash
$ mkdir bot
$ cd bot
$ lifoid init
```

will create a new bot project structure:

```bash
.env # Environment variables
agent/ # example of bot name and package
agent/__init_.py # it defines the package
agent/settings.py # project settings 
agent/router.py # define where we can find actions and models
agent/actions.py # define actions and routing conditions
agent/templates/ # template views used to generate responses
tests/ # test files
```

.env file sets:
``
LIFOID_SETTINGS_MODULE=agent.settings
``

This is similar to the Django Web Framework and you tell Lifoid where to
find the projet settings module, which contains mandatory settings for
the Lifoid framework.


The ``settings.py`` module defines the global parameter:
``
ROUTER_CONF = 'agent.router'
`` 

``
ROUTER_CONF
``
tells Lifoid which module contains the parameter ``actions``.

In agent/router.py we find:

```python
from lifoid.actions import hello

actions = [hello]
```

``actions`` is a list of function names, each method has a decorator ``@action`` that defines
the conditions to get into the function.

``
@action
``
is a decorator defined in the module ``lifoid.action``.

Accordingly we find agent/actions.py with:

```python
# -*- coding: utf-8 -*-
from lifoid.action import action
from lifoid.message import LifoidMessage, Chat


@action(lambda message, context: 'hello' in message.payload.text.lower())
def hello(render, message, context):
    return render([
      LifoidMessage(payload=Chat(text='Hello'))
    ])
```

**Configuration**

Setup your environment parameters in a .env file, e.g:

```
DEBUG=False
LOGGING_FILE=lifoid.log
LOGGING_LEVEL=INFO
# Make sure a bot answers in due time
TIMEOUT=180
# Where se find our project settings file
LIFOID_SETTINGS_MODULE=agent.settings
# We want to use a Redis backend
REPOSITORY=redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PREFIX=lifoid
# Lifoid server settings
SERVER_HOST=localhost
SERVER_PORT=3000
# NLU server settings
PARSER=lifoid
NLU_URL=http://127.0.0.1:5000
```

**CLI**

**mqtt** Launches a Lifoid mqtt bot instance
```bash
lifoid mqtt --host localhost --port 1883 --lifoid_id simple-bot
```

**run** Launches a Lifoid server instance with configured webhooks
```bash
$ lifoid run --host localhost --port 5000
```

**talk** Allows to talk to a Lifoid server with a terminal:

Over MQTT:
Make sure a MQTT broker is available and make sure you have started a MQTT
instance of Lifoid with `run`.

```bash
$ lifoid talk --protocol mqtt --host localhost --port 1883
```

Over HTTP:
Make sure you have started an HTTP instance of a Lifoid bot with `run`.

```bash
$ lifoid talk --protocol http --host localhost --port 5000
```

**Test** Allows to run test dialogues

Run one test file:

```bash
$ lifoid test --file <file>
```

Run all test files in a folder:

```bash
$ lifoid test --path <path>
```

A file test is a YAML file that looks like that:

```yaml
---
- Hello
- What's your name?
- John
- Hello John
```

## Data store ##

Contexts of discussions are by default stored in the process memory.
This is not scalable but it's very convenient for development or a light service
deployment.

In order to deploy several processes with a shared data store it's possible to
use plugins that define new data store backends such as Redis and DynamoDB.

## Development ##

**Setup Lifoid**

Download latest version of Lifoid repository.

```bash
$ git clone git@bitbucket.org:romary/lifoid.git
$ cd lifoid
```

Create a virtualenv and install dependencies

```bash
$ virtualenv venv
$ source venv/bin/activate
```

Install Lifoid for development
```bash
$ pip install -e ./
```

Check the changelog:
```bash
$ git log --oneline --decorate --color
```

**Testing**

Run the tests to make sure everything is OK.

```bash
$ pip install tox
$ tox
```
 
or with setuptools
```bash
$ python setup.py test
```

## Getting help

To get help with Lifoid, please contact Romary on romary@me.com


---

*Author:*   Romary Dupuis <romary@me.com>

*Copyright (C) 2017-2018 Romary Dupuis*



