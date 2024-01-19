from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.misc.config import config


class AdminFilter(BaseFilter):
    key = 'is_admin'

    def __init__(self, is_admin: Optional[bool] = None):
        self.is_admin = is_admin

    async def __call__(self, message: Message):
        if self.is_admin is None:
            return False
        return message.from_user.id in config.tg_bot.admin_ids

