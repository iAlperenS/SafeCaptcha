import hashlib
import hmac
from flask import current_app
from .errors import InvalidSignatureError

# Attacklara karşı basit ama işlevli

def hash_answer(answer) -> str:
    return hashlib.sha256(str(answer).encode()).hexdigest()

def sign_id(cid: str) -> str:
    secret = current_app.config['SIGNING_SECRET']
    return hmac.new(secret.encode(), cid.encode(), hashlib.sha256).hexdigest()

def verify_signature(cid: str, signature: str):
    expected = sign_id(cid)
    if not hmac.compare_digest(expected, signature):
        raise InvalidSignatureError()
