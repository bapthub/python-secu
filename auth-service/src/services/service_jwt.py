import datetime
from jwt import encode,decode
from src.setup import SECRET_KEY

def encode_payload(duration):
    encoded_jwt = encode({"some": "cryptomail", "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours = duration)}, 
                            SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def check_payload(encoded_jwt):
    try:
        decoded_jwt = decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])
        return True
    except Exception as e:
        return e
