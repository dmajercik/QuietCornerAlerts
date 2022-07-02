import time

import jwt

import configparser
from new.schemas import UserSchema, UserLoginSchema
config = configparser.RawConfigParser()
configFilePath = r'resources/secret.config'
config.read(configFilePath)

JWT_SECRET = config.get('key','jwt_secret_key')
JWT_ALGORITHM = config.get('key','jwt_auth')


def token_response(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}
