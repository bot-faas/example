from urllib.request import urlopen
import qqbot
from pkg.openapi import OpenAPI, PicUpload

token, sandbox = OpenAPI()
msg_api = qqbot.MessageAPI(token, sandbox)

# 请将"bot.icodef.com/api/v1/open/guild/pic"加入qq机器人管理的消息URL配置
def handle(data: qqbot.Message):
    ret = PicUpload("test.png", urlopen(
        "https://bbs.tampermonkey.net.cn/uc_server/avatar.php?uid=4&size=big&ts=1").read())
    if ret['code'] == 0:
        return msg_api.post_message(data.channel_id, qqbot.MessageSendRequest(image=ret['data']['url'], msg_id=data.id))
    return msg_api.post_message(data.channel_id, qqbot.MessageSendRequest("<@!" + data.author.id + ">图片发送失败:"+ret['msg'], data.id))
