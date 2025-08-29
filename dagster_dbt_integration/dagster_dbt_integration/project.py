from pathlib import Path

from dagster_dbt import DbtProject

dbt_resale_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "dbt_resale").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
dbt_resale_project.prepare_if_dev()