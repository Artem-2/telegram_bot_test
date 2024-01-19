from dataclasses import dataclass
from typing import List
from environs import Env
from tgbot.misc.dot_env_craete import dot_env_craete
import sys

@dataclass
class DbConfig:
    pass


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    proxy: str
    number_of_changes_rename: int
    time_update: int


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            proxy=env.str("PROXY"),
            number_of_changes_rename=env.int("number_of_changes_rename"),
            time_update=env.int("time_update"),
        ),
        db=DbConfig(
        ),
        misc=Miscellaneous()
    )

try:
    config = load_config("config.env")
except:
    dot_env_craete()
    sys.exit("введите все данные в конфиг файл config.env")
if config.tg_bot.token == "<bot_token>" or config.tg_bot.admin_ids == "<admins>" or config.tg_bot.admin_ids == []:
    sys.exit("введите все данные в конфиг файл config.env")