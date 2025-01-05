from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import proptech_dbt_assets
from .project import proptech_dbt_project
from .schedules import schedules

defs = Definitions(
    assets=[proptech_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=proptech_dbt_project),
    },
)