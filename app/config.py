from os import getenv
from pathlib import Path

import pytz

ENGINE = getenv("ENGINE", "sqlite+aiosqlite:///database.db")
TIMEZONE = pytz.timezone(getenv("TIMEZONE", "Europe/Moscow"))

TEST_MODE = bool(int(getenv('TEST_MODE', 0)))

BASE_DIR = Path(__file__).parent.resolve()

BOT_TOKEN = getenv('BOT_TOKEN')

WEBHOOK_HOST = getenv('WEBHOOK_HOST', '')
WEBHOOK_PATH = '/webhook'
WEBAPP_URL = getenv('WEBAPP_URL', '')
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

MINIO_ROOT_USER = getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = getenv('MINIO_ROOT_PASSWORD')
MINIO_URL = getenv('MINIO_URL')
