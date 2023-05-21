from aiogram.client.session.aiohttp import AiohttpSession
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str                  # Токен бота
    admin_ids: list[int]        # Список id админов

@dataclass
class Server:
    proxy: AiohttpSession

@dataclass
class Config:
    tg_bot: TgBot
    server: Server
    db: str

def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path=path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), 
                                admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  server=Server(proxy=AiohttpSession(proxy=env('PROXY'))),
                  db=env('DATABASE'))

