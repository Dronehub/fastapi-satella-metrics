from setuptools import setup, find_packages

from fastapi_satella_metrics import __version__

setup(
    keywords=[
        'fastapi', 'satella', 'metrics', 'instrumentation', 'starlette', 'prometheus'
    ],
    packages=find_packages(include=[
        'fastapi_satella_metrics', 'fastapi_satella_metrics.*'
    ]),
    version=__version__,
    install_requires=[
        'satella', 'fastapi', 'stalette'
    ],
    test_require=["nose2", "mock", "coverage", "nose2[coverage_plugin]"],
    test_suite='nose2.collector.collector',
    python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*,!=3.6.*'
)
