# Simple MQTT bot

Make sure there is a MQTT Broker available, e.g. Mosquitto.

Here is an example to launch the bot with a local MQTT broker:

```
lifoid mqtt --host localhost --port 1883 --lifoid_id simple-bot
```

Then let's chat with this bot:

```
lifoid chat --host localhost --port 1883 --lifoid_id simple-bot
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
