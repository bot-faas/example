# BotFaaS例子
> 可以在[BotFaaS](https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=aVNjt&appChannel=share&businessType=9&from=181074&biz=ka&shareSource=5)频道获取更多资讯与技术支持

## [nonebot](./nonebot)
nonebot目录为nonebot机器人的目录，其中`function/drivers/botfaas.py`是一个驱动器，将BotFaaS`handler/handle`所接受到的数据转化为`nonebot.adapters.qqguild`所支持的协议。

`plugins`是nonebot机器人的插件目录，已经适配了一个`头像表情包`的插件作为示例

## [template 函数模板](./template)
该目录为函数模板，可以由该系列模板创建自己的项目

