from dagster import asset
from dagster import AssetExecutionContext
from dagster import AssetSpec

from dagster_dbt import DbtCliResource, dbt_assets
from dagster_gcp import BigQueryResource

from .project import proptech_dbt_project
from .resources import bigquery_resource


hdb_resale_transactions_2015_2016 = AssetSpec(
    key="hdb_resale_transactions_2015_2016",    # Unique identifier for the asset
    group_name="bigquery_sources",              # Optional, group assets logically
    description="Manually uploaded table for 2015-2016 resale transactions",
    metadata={
        "dataset": "dl_property_transactions",
        "table": "hdb_resale_transactions_2015-2016",
    },
)

hdb_resale_transactions_2017_onwards = AssetSpec(
    key="hdb_resale_transactions_2017_onwards",    # Unique identifier for the asset
    group_name="bigquery_sources",              # Optional, group assets logically
    description="Manually uploaded table resale transactions from 2017 onwards",
    metadata={
        "dataset": "dl_property_transactions",
        "table": "hdb_resale_transactions_2017_onwards",
    },
)


@dbt_assets(manifest=proptech_dbt_project.manifest_path)
def proptech_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    