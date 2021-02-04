import datetime
import jwt
import os
from dotenv import load_dotenv
from helpers.auth.exceptions import ReadTokenException

load_dotenv()
secret = os.getenv('secret', 'SUPER_SECRET_KEY')


def create_token(data: dict, *, lifetime: int = 1) -> str:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=lifetime),
    }
    payload.update(data)
    return jwt.encode(payload, secret, algorithm='HS256')


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except jwt.exceptions.PyJWTError:
        raise ReadTokenException
