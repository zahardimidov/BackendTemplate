import asyncio
import logging
import os
from pathlib import Path

from app.config import BASE_DIR, ENGINE
from app.infra.database.session import run_database
from app.main import app

logging.info(f"UNIT testing for application: {app.title}")

def find_files_with_python(filename):
    matching_files = []
    path = Path(BASE_DIR.parent)
    for file in path.rglob(f"*{filename}*"):
        if file.is_file():
            matching_files.append(file)
    return matching_files


async def init_database():
    filename = ENGINE.split("/")[-1]

    for file in find_files_with_python(filename):
        os.remove(file)
        logging.info(f"Removed database file: {str(file)}")

    await run_database()
    await asyncio.sleep(1)


async def setup():
    await init_database()


asyncio.run(setup())
