import random
import time

from flask import Flask, render_template_string, abort
from prometheus_client import generate_latest, REGISTRY, Counter, Gauge, Histogram

app = Flask(__name__)

REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])

IN_PROGRESS = Gauge('http_requests_inprogress', 'Number of in progress HTTP requests')

TIMINGS = Histogram('http_request_duration_seconds', 'HTTP request latency (seconds)')


@app.route('/')
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def hello_world():
    REQUESTS.labels(method='GET', endpoint="/", status_code=200).inc()  
    return 'Hello, World!'

@app.route('/slow')
@TIMINGS.time()
@IN_PROGRESS.track_inprogress()
def slow_request():
    v = random.expovariate(1.0 / 1.3)
    if v > 3:
        REQUESTS.labels(method='GET', endpoint="/slow", status_code=500).inc()
        abort(500)
    time.sleep(v)
    REQUESTS.labels(method='GET', endpoint="/slow", status_code=200).inc()
    return render_template_string('<h1>Wow, that took {{v}} s!</h1>', v=v)


@app.route('/hello/<name>')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def index(name):
    REQUESTS.labels(method='GET', endpoint="/hello/<name>", status_code=200).inc()
    return render_template_string('<b>Hello {{name}}</b>!', name=name)

@app.route('/metrics')
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def metrics():
    REQUESTS.labels(method='GET', endpoint="/metrics", status_code=200).inc()
    return generate_latest(REGISTRY)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)