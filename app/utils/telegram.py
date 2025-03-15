import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qsl

from app.config import BOT_TOKEN


def validate_qsl_init_data(init_data: str):
    initData: dict = dict(parse_qsl(init_data))
    return validate_init_data(init_data=initData)


def validate_init_data(init_data: dict):
    try:
        hash_ = init_data.pop('hash')
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(init_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=BOT_TOKEN.encode(), digestmod=hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        if calculated_hash == hash_:
            user = json.loads(init_data['user'])
            del user['allows_write_to_pm']
            return user
    except Exception:
        pass
