from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class CaptchaError(Exception):
    status_code = 400
    message = "Captcha error"

    def __init__(self, message=None):
        if message:
            self.message = message

    def to_response(self):
        return jsonify(success=False, error=self.message), self.status_code


class ExpiredCaptchaError(CaptchaError):
    status_code = 403
    message = "CAPTCHA süresi dolmuş"


class TooManyAttemptsError(CaptchaError):
    status_code = 403
    message = "Max yanlış deneme sayısına ulaşıldı, yeni captcha alın"


class NotFoundCaptchaError(CaptchaError):
    status_code = 400
    message = "Geçersiz veya süresi dolmuş CAPTCHA"


class InvalidSignatureError(CaptchaError):
    status_code = 400
    message = "Geçersiz imza"


def register_error_handlers(app):
    @app.errorhandler(CaptchaError)
    def handle_captcha_error(e):
        logger.warning(f"[CaptchaError] {e.message}")
        return e.to_response()

    @app.errorhandler(429)
    def handle_rate_limit(e):
        logger.warning("[RateLimit] 429 Too Many Requests")
        return jsonify(error="Çok fazla istek, lütfen daha sonra tekrar deneyin."), 429

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        logger.exception(f"[UnhandledException] {str(e)}")
        return jsonify(success=False, error="Sunucu hatası, tekrar deneyin."), 500
