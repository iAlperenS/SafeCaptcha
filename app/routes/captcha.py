from flask import Blueprint, request, jsonify
from app.core.utils import sign_id, verify_signature, hash_answer
from app.core.cache import set_captcha, get_captcha, delete_captcha, cleanup_cache
from app.core.errors import CaptchaError, ExpiredCaptchaError, TooManyAttemptsError, NotFoundCaptchaError
from app.captcha.apocaptcha import APOCaptcha
from app.captcha.generate_image import create_base64_image
from app.metrics import REQUEST_LATENCY, REQUEST_COUNT
from app import limiter
import time

# Difficulty eklenicek hepsi medium
# Difficulty will be added - default medium

captcha_bp = Blueprint("captcha", __name__, url_prefix="/api/v1")

@captcha_bp.route("/captcha", methods=["GET"])
@limiter.limit("10/minute")
def generate_captcha():
    start = time.time()
    cleanup_cache()

    difficulty = request.args.get("difficulty", "medium").lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "medium"

    captcha = APOCaptcha().result()
    cid = captcha["id"]
    sig = sign_id(cid)
    img_base64 = create_base64_image(captcha["raw"])

    set_captcha(cid, {
        "answer_hash": hash_answer(captcha["answer"]),
        "timestamp": captcha["time"],
        "wrong_attempts": 0,
        "difficulty": difficulty
    })

    REQUEST_LATENCY.labels(endpoint='/api/v1/captcha').observe(time.time() - start)
    REQUEST_COUNT.labels(method="GET", endpoint="/api/v1/captcha", http_status="200").inc()

    return jsonify({
        "id": cid,
        "signature": sig,
        "captcha_img": f"data:image/png;base64,{img_base64}",
        "expires_in": 60,
        "expire_at": captcha["time"] + 60,
        "difficulty": difficulty
    })


@captcha_bp.route("/captcha/refresh", methods=["POST"])
@limiter.limit("10/minute")
def refresh_captcha():
    start = time.time()
    cleanup_cache()

    data = request.get_json(force=True)
    old_id = data.get("id")
    signature = data.get("signature")

    if not old_id or not signature:
        raise CaptchaError("Eksik id veya signature")

    verify_signature(old_id, signature)
    delete_captcha(old_id)

    captcha = APOCaptcha().result()
    cid = captcha["id"]
    sig = sign_id(cid)
    img_base64 = create_base64_image(captcha["raw"])

    set_captcha(cid, {
        "answer_hash": hash_answer(captcha["answer"]),
        "timestamp": captcha["time"],
        "wrong_attempts": 0,
        "difficulty": "medium"
    })

    REQUEST_LATENCY.labels(endpoint='/api/v1/captcha/refresh').observe(time.time() - start)
    REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/captcha/refresh", http_status="200").inc()

    return jsonify({
        "id": cid,
        "signature": sig,
        "captcha_img": f"data:image/png;base64,{img_base64}",
        "expires_in": 60,
        "expire_at": captcha["time"] + 60,
        "difficulty": "medium"
    })


@captcha_bp.route("/verify", methods=["POST"])
@limiter.limit("5/second")
def verify_captcha():
    start = time.time()
    cleanup_cache()

    data = request.get_json(force=True)
    cid = data.get("id")
    signature = data.get("signature")
    answer = data.get("answer")

    if not cid or not signature or answer is None:
        raise CaptchaError("Eksik alanlar: id, signature, answer")

    verify_signature(cid, signature)
    entry = get_captcha(cid)
    if not entry:
        raise NotFoundCaptchaError()

    if time.time() - entry["timestamp"] > 60:
        delete_captcha(cid)
        raise ExpiredCaptchaError()

    if entry["wrong_attempts"] >= 5:
        delete_captcha(cid)
        raise TooManyAttemptsError()

    if hash_answer(answer) == entry["answer_hash"]:
        delete_captcha(cid)
        REQUEST_LATENCY.labels(endpoint='/api/v1/verify').observe(time.time() - start)
        REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/verify", http_status="200").inc()
        return jsonify(success=True)

    entry["wrong_attempts"] += 1
    set_captcha(cid, entry)
    attempts_left = 5 - entry["wrong_attempts"]
    raise CaptchaError(f"Yanlış cevap. {attempts_left} deneme kaldı.")
