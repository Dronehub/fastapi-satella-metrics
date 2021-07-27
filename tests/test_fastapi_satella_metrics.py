import unittest

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from satella.coding.sequences import choose
from satella.instrumentation.metrics import getMetric

import fastapi_satella_metrics
from fastapi_satella_metrics.prometheus_exporter import PrometheusExporter

app = FastAPI()
app.include_router(PrometheusExporter({"service_name": "my_service"}))
app.add_middleware(fastapi_satella_metrics.SatellaMetricsMiddleware)


@app.get("/")
def endpoint():
    return ""


@app.get("/error")
def error():
    raise HTTPException(status_code=500)


test_client = TestClient(app)


class TestFastApiSatellaMetrics(unittest.TestCase):
    def test_satella_metrics(self):
        getMetric("my.internal.metric", "counter", internal=True)
        q = test_client.get("http://localhost:5000/")
        self.assertEqual(q.status_code, 200)

        q = test_client.get("http://localhost:5000/error")
        self.assertEqual(q.status_code, 500)

        root_metric = getMetric().to_metric_data()
        request_codes = choose(
            lambda metric: metric.name == "requests_response_codes"
            and metric.labels == {"response_code": 200},
            root_metric.values,
        )
        self.assertEqual(request_codes.value, 1)
        request_codes = choose(
            lambda metric: metric.name == "requests_response_codes"
            and metric.labels == {"response_code": 500},
            root_metric.values,
        )
        self.assertEqual(request_codes.value, 1)

        q = test_client.get("http://localhost:5000/metrics")
        self.assertEqual(q.status_code, 200)
        self.assertIn('service_name=\\"my_service\\"', q.text)
        self.assertIn("requests_response_codes", q.text)
        self.assertNotIn("my_internal_metric", q.text)
