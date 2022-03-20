import qqbot
from pkg.db.mongo import MongoDB
from pkg.openapi import OpenAPI  # 此处引入数据库组件

# @var mongodb database.Database
mongodb = MongoDB()

token, sandbox = OpenAPI()
msg_api = qqbot.MessageAPI(token, sandbox)


def handle(msg: qqbot.Message):
    col = mongodb["count"]
    data = col.find_one({"uid": msg.author.id})
    if data is None:
        col.insert_one({"uid": msg.author.id, "count": 1})
        data["count"] = 1
    else:
        col.update_one({"uid": msg.author.id}, {"$inc": {"count": 1}})
        data["count"] += 1
    pass

    msg_api = qqbot.MessageAPI(token, sandbox)
    send = qqbot.MessageSendRequest(
        "<@!" + msg.author.id + ">"+"这是第"+str(data["count"])+"条消息", msg.id)
    msg_api.post_message(msg.channel_id, send)
