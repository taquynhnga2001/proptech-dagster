from dagster import Definitions

from dagster_dbt import DbtCliResource
from dagster_gcp import BigQueryResource

from .assets import (
    proptech_dbt_assets, 
    hdb_resale_transactions_2015_2016, 
    hdb_resale_transactions_2017_onwards
)
from .project import proptech_dbt_project
from .schedules import wed_midnight_schedules
from .resources import bigquery_resource

defs = Definitions(
    assets=[hdb_resale_transactions_2015_2016, hdb_resale_transactions_2017_onwards, proptech_dbt_assets],
    schedules=[wed_midnight_schedules],
    resources={
        "dbt": DbtCliResource(project_dir=proptech_dbt_project),
        "bigquery": bigquery_resource
    },
)