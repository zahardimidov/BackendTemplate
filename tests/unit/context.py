import asyncio
import logging
import os

os.environ['TEST_MODE'] = '1'

from pathlib import Path

from app.config import BASE_DIR, ENGINE
from app.infra.database.session import run_database

logging.basicConfig(level=logging.INFO)


def find_files_with_python(filename):
    matching_files = []
    path = Path(BASE_DIR.parent)
    for file in path.rglob(f'*{filename}*'):
        if file.is_file():
            matching_files.append(file)
    return matching_files


class Context(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if not cls._instances:
            asyncio.run(Context.init_database(cls))
        if cls not in cls._instances:
            cls._instances[cls] = super(Context, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    async def init_database(cls):
        filename = ENGINE.split('/')[-1]

        for file in find_files_with_python(filename):
            os.remove(file)
            logging.info(f'Removed database file: {str(file)}')

        await run_database()
        await asyncio.sleep(1)
