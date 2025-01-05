from pathlib import Path

from dagster_dbt import DbtProject

proptech_dbt_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "proptech_dbt_project").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
proptech_dbt_project.prepare_if_dev()