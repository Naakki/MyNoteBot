from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str                  # Токен бота
    admin_ids: list[int]        # Список id админов


@dataclass
class Config:
    tg_bot: TgBot               
    db: str

def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path=path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), 
                                admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                    db=env('DATABASE'))

