import logging
import subprocess
import sys
import time
import warnings
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv
from requests.models import Response

warnings.filterwarnings("ignore")


BASE_DIR = Path(__file__).parent.parent.parent.resolve()
DOCKER_DIR = BASE_DIR.joinpath('docker').resolve()

sys.path.insert(0, BASE_DIR.__str__())
sys.path.insert(0, BASE_DIR.joinpath('app').__str__())

docker_compose_file = DOCKER_DIR.joinpath('docker-compose.testing.yml')
env_file = DOCKER_DIR.joinpath('tests.env')
docker_cmd = f'docker compose -f {docker_compose_file} --env-file={env_file}'

load_dotenv(env_file, override=True)

from app.run import app

logging.info(app.title)


def docker_comnpose_down():
    cmd = docker_cmd + ' down'

    result = subprocess.run(cmd.split(), capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"Docker Compose failed to stop: {result.stderr}")
    else:
        logging.info("Docker Compose stoped")


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    try:
        docker_comnpose_down()

        cmd = docker_cmd + ' up --build -d'
        result = subprocess.run(cmd.split(), capture_output=True, text=True)

        if result.returncode != 0:
            logging.critical(f"Failed to start Docker Compose: {result.stderr}")
            pytest.exit("Docker Compose failed to start")
        else:
            logging.info('Docker Compose started')
        time.sleep(10)
        yield
    finally:
        wait = 10
        logging.info(f"Docker will be stoped in {wait} seconds")
        time.sleep(wait)

        docker_comnpose_down()


def pytest_tavern_beta_before_every_request(request_args: MutableMapping):
    message = f"Request: {request_args['method']} {request_args['url']}"

    params = request_args.get("params", None)
    if params:
        message += f"\nQuery parameters: {params}"

    message += f"\nRequest body: {request_args.get('json', '<no body>')}"

    logging.info(message)


def pytest_tavern_beta_after_every_response(expected: Any, response: Response) -> None:
    logging.info(f"Response: {response.status_code} {response.text}")
