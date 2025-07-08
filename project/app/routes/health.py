from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health_check():
    return jsonify(status="ok"), 200

@health_bp.route("/")
def root():
    return jsonify(message="CAPTCHA API çalışıyor. /api/v1/"), 200
