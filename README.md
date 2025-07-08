# 🔐 SafeCAPTCHA Verification API

A production-ready, modular CAPTCHA verification system built with Flask. This project focuses on security, scalability, and observability — designed to prevent bot abuse, brute-force attacks, and automate protection mechanisms.

---

## 🚀 Features

- ✅ **CAPTCHA Generation (Easy / Medium / Hard)**
- 🔐 **HMAC-Signed Captcha IDs** for tamper-proof verification
- 🚫 **Rate Limiting** with `Flask-Limiter` to block abuse & bots
- 📊 **Prometheus Metrics** for monitoring (latency, request counts)
- 🧪 **Unit Testing** with `pytest`
- 🐳 **Docker Support** for isolated deployment
- 🧱 **Modular Flask Structure** (easy to maintain and extend)

---

## 🛠️ Technologies Used

- Python 3.13
- Flask
- Pillow (for image rendering)
- Flask-Limiter (rate-limiting)
- Prometheus Client (metrics)
- Pytest (unit testing)
- HMAC & SHA-256 (secure signatures)
- Docker

---

## ⚠️ Production Usage Recommendations
- By default, Flask-Limiter uses in-memory storage for rate limiting, which is suitable for development and small projects but not recommended for production.

- For production environments, it’s best to use a persistent storage backend like Redis or Memcached to store rate limit data reliably and enable scalability.

- You can configure Flask-Limiter with Redis by setting the storage_uri parameter, for example:
- storage_uri="redis://localhost:6379"

- Using Redis (or similar) also ensures consistent rate limiting across multiple instances in distributed setups.

---

## 📦 Project Structure
```bash
project/
├── app/
│ ├── init.py # App Factory
│ ├── config.py # Environment configs
│ ├── captcha/
│ │ ├── apocaptcha.py # Captcha logic
│ │ └── generate_image.py # Base64 image generator
│ ├── core/
│ │ ├── cache.py # Cleanup & caching logic
│ │ ├── utils.py # Hashing, HMAC, signing
│ │ └── errors.py # Custom exceptions
│ ├── routes/
│ │ ├── captcha.py # API: /captcha, /verify, /refresh
│ │ └── health.py # API: /health, /
│ └── metrics.py # Prometheus metrics
├── tests/
│ └── test_captcha.py # Pytest test cases
├── run.py # Entry point
├── Dockerfile # Docker container
└── requirements.txt
```

---

## 📄 API Endpoints

### 🎨 `GET /api/v1/captcha`
> Generate a new captcha  
Returns: `captcha_img`, `id`, `signature`, `expire_at`

### ♻️ `POST /api/v1/captcha/refresh`
> Refresh a captcha with old `id` and `signature`

### ✅ `POST /api/v1/verify`
> Verify the captcha  
Input: `{ "id": "...", "signature": "...", "answer": "..." }`

### 🩺 `GET /health`
> Simple health check

### 📈 `GET /metrics`
> Prometheus metrics endpoint

---

## ⚙️ Running the Project

### 🔧 Local (Dev Mode)

```bash
# 1. Clone
git clone https://github.com/iAlperenS/SafeCAPTCHA.git
cd SafeCAPTCHA

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
python run.py
```

---

## 🐳 With Docker
```bash
docker build -t SafeCAPTCHA .
docker run -p 5000:5000 SafeCAPTCHA
```

## ✅ Testing
```bash
pytest tests/
```
- Rate-limiting warnings may show — they're expected in local testing.

---

## 🔐 Security Highlights
- All captcha IDs are signed using HMAC (SHA-256) to prevent tampering

- Rate limits are enforced on all endpoints to prevent abuse (DDoS, brute force)

- Captchas expire in configurable time (default: 60 seconds)

- Wrong attempts are limited (default: 5 tries per ID)

---

### 📄 License
MIT License

---

### 🤝 Contributing
**Pull requests are welcome. Feel free to submit issues, enhancements, or suggestions!**

---

Made with ❤️ by iAlperenS & cagatay_seper
---
Contact: alperendevv@gmail.com
