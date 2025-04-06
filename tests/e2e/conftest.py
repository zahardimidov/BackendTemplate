import logging
import os
import subprocess
import time
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

import pytest
from requests.models import Response

from app.main import app

logging.info(f"E2E testing for application: {app.title}")

BASE_DIR = Path(__file__).parent.parent.parent.resolve()
DOCKER_DIR = BASE_DIR.joinpath("docker").resolve()

def get_env():
    env = os.environ.copy()
    for file in DOCKER_DIR.glob("*.yml"):
        path = file.resolve().__str__()
        command = "grep -o '${[A-Z_]*}' " + path + " | sort -u"
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        for i in result.stdout.strip().split():
            key = i.replace("${", "").replace("}", "")
            value = os.environ.get(key)
            if value:
                env[key] = value
    return env

env_variables = get_env()

docker_compose_file = DOCKER_DIR.joinpath("docker-compose.testing.yml")
docker_cmd = f"docker compose -f {docker_compose_file}"


def docker_comnpose_down():
    logging.info(f"Command is: {docker_cmd}")

    cmd = docker_cmd + " down"

    result = subprocess.run(cmd.split(), capture_output=True, text=True, env=env_variables)

    if result.returncode != 0:
        logging.error(f"Docker Compose failed to stop: {result.stderr}")
    else:
        logging.info("Docker Compose stoped")


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    try:
        docker_comnpose_down()

        cmd = docker_cmd + " up --build -d"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, env=env_variables)

        if result.returncode != 0:
            logging.critical(f"Failed to start Docker Compose: {result.stderr}")
            pytest.exit("Docker Compose failed to start")
        else:
            logging.info("Docker Compose started")
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
