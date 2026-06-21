import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from config.const import BASE_DIR


@dataclass
class TgBot:
    token: str
    admin_password: str
    main_admin_id: str | None = None
    bot_name: str | None = None
    proxy_url: str | None = None
    metrics_port: int | None = None
    message_max_symbols: int = 400


@dataclass
class YandexMusic:
    token: str
    ynison_device_info: dict = field(default_factory=lambda: {'app_name': 'Chrome', 'type': 1})
    ynison_gry_main_url: str = 'wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison'
    ynison_pys_main_url: str = 'wss://%%/ynison_state.YnisonStateService/PutYnisonState'


@dataclass
class LogConfig:
    level: str = 'INFO'
    format: str = '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_path: str = 'logs/bot.log'
    max_size: int = 10
    backup_count: int = 3


@dataclass
class Config:
    tg_bot: TgBot
    yandex_music: YandexMusic
    log: LogConfig
    db_path: Path


def load_config() -> Config:
    load_dotenv(find_dotenv())
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            admin_password=os.getenv('PASSWORD'),
            main_admin_id=os.getenv('MAIN_ADMIN_ID') or None,
            bot_name=os.getenv('BOT_NAME') or None,
            proxy_url=os.getenv('PROXY_URL') or None,
            metrics_port=int(os.getenv('METRICS_PORT')) if os.getenv('METRICS_PORT') else None,
        ),
        yandex_music=YandexMusic(token=os.getenv('YANDEX_TOKEN')),
        log=LogConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file_path=os.getenv('LOG_FILE', 'logs/bot.log'),
            max_size=int(os.getenv('LOG_MAX_SIZE', 10)),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', 3)),
        ),
        db_path=BASE_DIR / 'db' / 'data.db',
    )
