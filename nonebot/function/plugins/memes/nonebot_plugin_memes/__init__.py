import shlex
import traceback
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.adapters.qqguild import Message, MessageSegment
from nonebot.log import logger

from pkg.openapi import PicUpload

from .models import NormalMeme
from .download import DownloadError
from .utils import help_image
from .normal_meme import normal_memes
from .gif_subtitle_meme import gif_subtitle_memes


__help__plugin_name__ = "memes"
__des__ = "表情包制作"
__cmd__ = "发送“表情包制作”查看表情包列表"
__short_cmd__ = __cmd__
__example__ = """
鲁迅说 我没说过这句话
王境泽 我就是饿死 死外边 不会吃你们一点东西 真香
""".strip()
__usage__ = f"{__des__}\n\nUsage:\n{__cmd__}\n\nExamples:\n{__example__}"


help_cmd = on_command("表情包制作", block=True, priority=12)

memes = normal_memes + gif_subtitle_memes


@help_cmd.handle()
async def _():
    img = await help_image(memes)
    if img:
        ret = PicUpload('help.gif', img.getvalue())
        if ret['code'] == 0:
            return await help_cmd.finish(MessageSegment.image(ret['data']['url']))
        await help_cmd.finish(MessageSegment.text("图片发送失败:" + ret['msg']))

async def handle(matcher: Matcher, meme: NormalMeme, text: str):
    arg_num = meme.arg_num
    if arg_num == 1:
        texts = [text]
    else:
        try:
            texts = shlex.split(text)
        except:
            await matcher.finish(f"参数解析错误，若包含特殊符号请转义或加引号")

    if len(texts) < arg_num:
        await matcher.finish(f"该表情包需要输入{arg_num}段文字")
    elif len(texts) > arg_num:
        await matcher.finish(f"参数数量不符，需要输入{arg_num}段文字，若包含空格请加引号")

    try:
        res = await meme.func(texts)
    except DownloadError:
        logger.warning(traceback.format_exc())
        await matcher.finish("资源下载出错，请稍后再试")
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish("出错了，请稍后再试")

    if isinstance(res, str):
        await matcher.finish(res)
    else:
        ret = PicUpload('avatar.gif', res.getvalue())
        if ret['code'] == 0:
            return await matcher.send(MessageSegment.image(ret['data']['url']))
        await matcher.send(MessageSegment.text("图片发送失败:" + ret['msg']))


def create_matchers():
    def create_handler(meme: NormalMeme) -> T_Handler:
        async def handler(matcher: Matcher, msg: Message = CommandArg()):
            text = msg.extract_plain_text().strip()
            if not text:
                await matcher.finish()
            await handle(matcher, meme, text)

        return handler

    for meme in memes:
        on_command(
            meme.keywords[0], aliases=set(meme.keywords), block=True, priority=13
        ).append_handler(create_handler(meme))


create_matchers()
