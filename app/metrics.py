from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request
import time

# Metrik tanımları
# Metric definitions
REQUEST_COUNT = Counter(
    'captcha_api_requests_total',
    'Toplam HTTP istek sayısı',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'captcha_api_request_latency_seconds',
    'HTTP istek gecikme süresi (saniye)',
    ['endpoint']
)

def before_request():
    request._start_time = time.time()

def after_request(response):
    if hasattr(request, '_start_time'):
        latency = time.time() - request._start_time
        endpoint = request.path
        method = request.method
        status_code = str(response.status_code)

        # Karmaşık işler
        # ... complex
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

    return response

def init_metrics(app):
    # Flaske ekleyelim
    # Add to flask
    app.before_request(before_request)
    app.after_request(after_request)

    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
