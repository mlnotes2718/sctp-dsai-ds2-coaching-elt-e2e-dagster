from pathlib import Path

from dagster_dbt import DbtProject

dbt_austin_bikeshare_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "dbt_austin_bikeshare").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
dbt_austin_bikeshare_project.prepare_if_dev()