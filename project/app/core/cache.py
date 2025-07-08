import time
from flask import current_app
import logging

logger = logging.getLogger(__name__)

captcha_cache = {}
# Captcha idlerini memde saklıyoruz redis kullanılmalı
# Saving captcha ids in mem - use redis

def set_captcha(cid, data: dict):
    captcha_cache[cid] = data

def get_captcha(cid: str):
    return captcha_cache.get(cid)

def delete_captcha(cid: str):
    captcha_cache.pop(cid, None)

def cleanup_cache():
    now = time.time()
    expiry = current_app.config.get('CAPTCHA_EXPIRY', 60)
    expired = [cid for cid, val in captcha_cache.items() if now - val['timestamp'] > expiry]
    for cid in expired:
        delete_captcha(cid)
        logger.info(f"[Cache] Captcha {cid} süresi dolduğu için temizlendi.")
