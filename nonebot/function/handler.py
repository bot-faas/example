import asyncio
import json
import threading

import nonebot.drivers.websockets
import qqbot
from nonebot.adapters.qqguild import Adapter as QQ_频道Adapter

global driver
global loop

def run():
    global driver
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nonebot.init(_env_file='./function/.env')
    driver = nonebot.get_driver()
    driver.register_adapter(QQ_频道Adapter)
    nonebot.load_plugin('function.plugins.echo')
    nonebot.load_plugin('function.plugins.petpet.nonebot_plugin_petpet.data_source')
    nonebot.run(app="__mp_main__:app")


threading.Thread(target=run).start()


def handle(data: qqbot.Message):
    data.__delitem__('edited_timestamp')

    driver.putMsg('AT_MESSAGE_CREATE', json.dumps(data))
    return None
