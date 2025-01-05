from dagster import asset, Output
from dagster import AssetExecutionContext
from dagster import AssetSpec

from dagster_dbt import DbtCliResource, dbt_assets
from dagster_gcp import BigQueryResource

from .project import proptech_dbt_project
from .resources import bigquery_resource
from .constant import HDB_TRANS_2017_ONWARDS_TABLE_NAME, HDB_TRANS_2017_ONWARDS_API_DATASET_ID
from .utils import fetch_all_rows_from_api

import requests
import pandas as pd

hdb_resale_transactions_2015_2016 = AssetSpec(
    key="hdb_resale_transactions_2015_2016",
    group_name="bigquery_sources",              
    description="Manually uploaded table for 2015-2016 resale transactions",
    kinds={"bigquery"},
    metadata={
        "dataset": "dl_property_transactions",
        "table": "hdb_resale_transactions_2015-2016",
    },
)


@asset(
    kinds={"python", "bigquery"},
    group_name="bigquery_sources",
)
def hdb_resale_transactions_2017_onwards(context: AssetExecutionContext, bigquery: BigQueryResource):
    """Fetch data from API and load it into BigQuery."""
    # API request
    dataset_id = HDB_TRANS_2017_ONWARDS_API_DATASET_ID
    context.log.info("Fetching data from API")
    
    df = fetch_all_rows_from_api(dataset_id=dataset_id)
    df = df.drop(columns='_id', errors='ignore')
    context.log.info(f"Fetched {len(df)} rows from API.")
    
    # Load to BigQuery
    table_name = HDB_TRANS_2017_ONWARDS_TABLE_NAME
    with bigquery.get_client() as client:
        job = client.load_table_from_dataframe(
            dataframe=df,
            destination=table_name,
        )
        job.result()
    
    return Output(
        value=None,
        metadata={
            "rows_loaded": len(df),
            "max_month": df.month.max(),
            "bigquery_table": table_name,
        },
    )


@dbt_assets(manifest=proptech_dbt_project.manifest_path)
def proptech_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    