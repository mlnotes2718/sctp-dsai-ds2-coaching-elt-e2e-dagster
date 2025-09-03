# definitions.py
from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_austin_bikeshare_dbt_assets, meltano_austin_bike_pipeline
from .project import dbt_austin_bikeshare_project
from .schedules import schedules

defs = Definitions(
    assets=[dbt_austin_bikeshare_dbt_assets, meltano_austin_bike_pipeline],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_austin_bikeshare_project),
    },
)