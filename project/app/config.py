import os

class Config:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    CAPTCHA_EXPIRY = int(os.getenv("CAPTCHA_EXPIRY", 60))
    MAX_WRONG_ATTEMPTS = int(os.getenv("MAX_WRONG_ATTEMPTS", 5))
    RATE_LIMIT_CAPTCHA = os.getenv("RATE_LIMIT_CAPTCHA", "10/minute")
    RATE_LIMIT_VERIFY = os.getenv("RATE_LIMIT_VERIFY", "5/second")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SIGNING_SECRET = os.getenv("SIGNING_SECRET", "change_this_secret")