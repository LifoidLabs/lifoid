# Simple MQTT bot

This project structure was initialized with `lifoid init` command.

You can personalize the environment file `.env` according to the
`.env.example` file and specification provided in Lifoid project root.

Make sure there is a MQTT Broker available, e.g. Mosquitto.

Here is an example to launch the bot with a local MQTT broker:

```bash
lifoid mqtt_bot --host localhost --port 1883 --lifoid_id simple-bot
```

Then let's chat with this bot:

```bash
lifoid mqtt_client --host localhost --port 1883 --lifoid_id simple-bot
+-----------------------------------------------------------------------------+
|                                                                             |
|   Lifoid                                                                    |
|                                                                             |
|   Copyright (C) 2017-2018 Romary Dupuis                                     |
|                                                                             |
+-----------------------------------------------------------------------------+


* PLease type in your messages below
hello
from simple-bot --> Hello, what is your name?
My name is Bob
from simple-bot --> Hello Bob
```
