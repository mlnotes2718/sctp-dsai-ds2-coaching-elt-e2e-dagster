from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import austin_bike_dbt_dbt_assets, meltano_austin_bike_pipeline
from .project import austin_bike_dbt_project
from .schedules import schedules

defs = Definitions(
    assets=[
        meltano_austin_bike_pipeline, 
        austin_bike_dbt_dbt_assets
    ],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=austin_bike_dbt_project),
    },
)