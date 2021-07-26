fastapi-satella-metrics
=====================

fastapi-satella-metrics is an application to seamlessly measure your FastAPI
application using Satella's metrics.

Example use:

```python
import fastapi
from fastapi_satella_metrics import SatellaMetricsMiddleware
app = fastapi.FastAPI()
app.add_middleware(SatellaMetricsMiddleware)
```

And to launch a Prometheus exporter use the following snippet:

```python
from satella.instrumentation.metrics.exporters import PrometheusHTTPExporterThread
phet = PrometheusHTTPExporterThread('0.0.0.0', 8080, {'service_name': 'my_service'})
phet.start()
```

Or, if you desire to export your metrics within FastAPI, just use:

```python
import fastapi
from fastapi_satella_metrics.prometheus_exporter import PrometheusExporter
app = fastapi.FastAPI()
app.include_router(PrometheusExporter({'service_name': 'my_service'}))
```