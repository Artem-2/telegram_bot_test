from dataclasses import dataclass
from typing import List
from environs import Env


@dataclass
class DbConfig:
    pass


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    proxy: str


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
        ),
        db=DbConfig(
        ),
        misc=Miscellaneous()
    )

config = load_config(".env")
config2 = config