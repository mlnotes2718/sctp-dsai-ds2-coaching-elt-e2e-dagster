from pathlib import Path

from dagster_dbt import DbtProject

austin_bike_dbt_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "austin_bike_dbt").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
austin_bike_dbt_project.prepare_if_dev()