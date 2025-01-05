from dagster import ScheduleDefinition, define_asset_job
from dagster import AssetSelection
from dagster_dbt import build_schedule_from_dbt_selection

from .assets import proptech_dbt_assets

# Define a job to materialize all assets
materialize_all_job = define_asset_job(
    "materialize_all_job", 
    selection=AssetSelection.all())

# Define the schedule using ScheduleDefinition
wed_midnight_schedules = ScheduleDefinition(
    name="materialize_all",
    cron_schedule="0 0 * * 3",  # Every Wednesday at midnight
    job=materialize_all_job,
)