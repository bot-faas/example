from io import BytesIO
from PIL import Image
from PIL.Image import Image as IMG
from dataclasses import dataclass
from typing import List, Tuple, Union, Protocol

from nonebot.adapters.qqguild.api import User


class UserInfo:
    def __init__(self, user: User, group: str = "", img_url: str = ""):
        self.user: User = user
        self.group: str = group
        self.name: str = user.username
        self.gender: str = "male"  # male 或 female 或 unknown
        self.img_url: str = user.avatar
        self.img: IMG = Image.new("RGBA", (640, 640))


class Func(Protocol):
    async def __call__(self, users: List[UserInfo], **kwargs) -> Union[str, BytesIO]:
        ...


@dataclass
class Command:
    keywords: Tuple[str, ...]
    func: Func
    convert: bool = True
    arg_num: int = 0
