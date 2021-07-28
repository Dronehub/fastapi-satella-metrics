import logging
import typing as tp

from fastapi.routing import APIRouter
from satella.instrumentation.metrics import getMetric
from satella.instrumentation.metrics.exporters import (
    metric_data_collection_to_prometheus,
)

logger = logging.getLogger(__name__)


__all__ = ['PrometheusExporter']


def PrometheusExporter(
    extra_labels: tp.Optional[dict] = None, url: str = "/metrics"
) -> APIRouter:
    """
    Return a router that exports metrics

    :param extra_labels: extra labels to attach to every metric collected
    :param url: custom URL to use. /metrics is the default one
    :return: an APIRouter, to be added via :code:`app.include_router`
    """
    labels = extra_labels or {}

    router = APIRouter()

    @router.get(url)
    def export_prometheus():
        metric = getMetric()
        metric_data = metric.to_metric_data()
        new_values = set()
        for datum in metric_data.values:
            if not datum.internal:
                new_values.add(datum)
        metric_data.values = new_values
        metric_data.add_labels(labels)

        return metric_data_collection_to_prometheus(metric_data)

    return router
