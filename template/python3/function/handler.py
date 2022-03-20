import qqbot
from pkg.openapi import OpenAPI

token, sandbox = OpenAPI()
msg_api = qqbot.MessageAPI(token, sandbox)


def handle(data: qqbot.Message):
    send = qqbot.MessageSendRequest("<@!" + data.author.id + ">ok", data.id)
    return msg_api.post_message(data.channel_id, send)
