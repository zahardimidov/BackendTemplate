import os
from datetime import UTC, datetime, timedelta

import jwt

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "my_secret_key")
ALGORITHM = "HS256"
EXPIRE = timedelta(days=7)


def create_jwt_token(data: dict, expire=EXPIRE) -> str:
    expiration = datetime.now(UTC) + expire
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str) -> dict:
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError as e:
        print(e)
