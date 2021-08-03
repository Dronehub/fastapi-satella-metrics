import typing as tp
from collections import namedtuple

from satella.instrumentation.metrics.metric_types import SummaryMetric, HistogramMetric, \
    CounterMetric
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from satella.time import measure
from satella.instrumentation.metrics import getMetric

__version__ = "2.0.0"

__all__ = ["SatellaMetricsMiddleware", "__version__"]

MetricsContainer = namedtuple(
    "MetricsContainer", ["summary_metric", "histogram_metric", "response_codes_metric"]
)


class SatellaMetricsMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        exclude_metrics_endpoint: bool = False,
        summary_metric: tp.Optional[SummaryMetric] = None,
        histogram_metric: tp.Optional[HistogramMetric] = None,
        response_codes_metric: tp.Optional[CounterMetric] = None,
    ):

        super().__init__(app)
        self.app = app
        self.exclude_metrics_endpoint = exclude_metrics_endpoint
        self.app.metrics = MetricsContainer(
            summary_metric
            or getMetric(
                "requests_summary", "summary", quantiles=[0.2, 0.5, 0.9, 0.95, 0.99]
            ),
            histogram_metric or getMetric("requests_histogram", "histogram"),
            response_codes_metric or getMetric("requests_response_codes", "counter"),
        )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        if self.exclude_metrics_endpoint and request.url.path == "/metrics":
            return await call_next(request)

        time_measure = measure()

        response = await call_next(request)

        time_measure.stop()
        elapsed = time_measure()
        endpoint = str(request.url)
        self.app.metrics.summary_metric.runtime(elapsed, endpoint=endpoint)
        self.app.metrics.histogram_metric.runtime(elapsed, endpoint=endpoint)
        self.app.metrics.response_codes_metric.runtime(
            +1, response_code=response.status_code
        )

        return response
