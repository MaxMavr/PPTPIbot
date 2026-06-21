import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).parent.parent

USERS_PER_PAGE = 15
QUERIES_PER_PAGE = 6

CHANNEL_ID: str = os.getenv('CHANNEL_ID') or '@phasalotest'
