from setuptools import find_packages, setup

setup(
    name="proptech_dagster",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "proptech_dagster": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-bigquery<1.9",
        "dbt-bigquery<1.9",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)