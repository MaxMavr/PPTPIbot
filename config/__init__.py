import os
import logging
import logging.handlers
from dataclasses import dataclass, field
from pathlib import Path
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv, find_dotenv
from config.const import BASE_DIR

load_dotenv(find_dotenv())

Path(BASE_DIR / 'logs').mkdir(exist_ok=True)
Path(BASE_DIR / 'temp').mkdir(exist_ok=True)


@dataclass
class LogConfig:
    level: str = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_path: str = 'logs/bot.log'
    max_size: int = 10  # MB
    backup_count: int = 3


@dataclass
class TgBot:
    token: str
    password: str
    main_admin_id: str
    message_max_symbols: int = 400


@dataclass
class YandexMusic:
    token: str
    ynison_device_info: dict = field(default_factory=lambda: {'app_name': 'Chrome', 'type': 1})
    ynison_gry_main_url: str = 'wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison'
    ynison_pys_main_url: str = 'wss://%%/ynison_state.YnisonStateService/PutYnisonState'


@dataclass
class Config:
    tg_bot: TgBot
    yandex_music: YandexMusic
    log: LogConfig


def load_config() -> Config:
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            password=os.getenv('PASSWORD'),
            main_admin_id=os.getenv('MAIN_ADMIN_ID')
        ),
        yandex_music=YandexMusic(os.getenv('YANDEX_TOKEN')),
        log=LogConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file_path=os.getenv('LOG_FILE', 'logs/bot.log'),
            max_size=int(os.getenv('LOG_MAX_SIZE', 10)),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', 3))
        )
    )


def setup_logging(cfg: LogConfig):
    logging.basicConfig(
        level=getattr(logging, cfg.level),
        format=cfg.format,
        handlers=[
            logging.handlers.RotatingFileHandler(
                filename=BASE_DIR / cfg.file_path,
                maxBytes=cfg.max_size * 1024 * 1024,
                backupCount=cfg.backup_count,
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('aiogram').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.INFO)


config: Config = load_config()
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))

setup_logging(config.log)
