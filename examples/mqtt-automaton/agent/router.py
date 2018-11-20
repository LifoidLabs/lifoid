from agent.actions import (greeting, user_name,
                           query_temperature,
                           temperature_change,
                           MQTTChatbot)


actions = [
    greeting,
    user_name,
    query_temperature,
    temperature_change
]

bot_model = MQTTChatbot
