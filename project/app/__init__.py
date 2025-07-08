import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from .config import Config
from .core.errors import register_error_handlers
from .metrics import init_metrics
from .logger import setup_logger

# Limiter global tanımlanır app ile initialize edilir
# Limiter was defined as global and initialize with app
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS ve rate limiter kur / Setup the CORS and rate limiter
    # rate limiter yerine redis kullanmak lazm / use redis instead of rate limiter
    # Kalıcı olması için / for permanent
    CORS(app)
    limiter.init_app(app)

    # kayıtlar / saves register
    init_metrics(app)
    setup_logger(app)

    # Blueprints import & register
    from .routes.captcha import captcha_bp
    from .routes.health import health_bp

    app.register_blueprint(captcha_bp)
    app.register_blueprint(health_bp)

    # Hata yöneticilerini kur / Setup the error handlers
    register_error_handlers(app)

    return app
