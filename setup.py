"""Setup for pipeline."""

import setuptools

setuptools.setup(
    name="dataflow",
    python_requires=">=3.8.12",
    version="1.0.0",
    install_requires=[
        "apache-beam[gcp]==2.35.0",
        "google-cloud-bigquery==2.32.0",
        "pendulum==2.1.2",
        "wheel==0.37.1",
    ],
    packages=setuptools.find_packages(),
)
