from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_meltano import meltano_resource
from .assets import dbt_resale_dbt_assets, pipeline_meltano
from .project import dbt_resale_project
from .schedules import schedules

defs = Definitions(
    assets=[pipeline_meltano, dbt_resale_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_resale_project),
        "meltano": meltano_resource.configured({
            "project_dir": "/Users/aiml/Documents/VSCode-Git/sctp-dsai-ds2-coaching-elt-e2e-dagster/meltano-resale"
        })
    },
)
