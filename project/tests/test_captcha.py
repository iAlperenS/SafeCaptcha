import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_get_captcha(client):
    res = client.get("/api/v1/captcha")
    assert res.status_code == 200
    data = res.get_json()
    assert "id" in data and "captcha_img" in data
    assert "signature" in data
