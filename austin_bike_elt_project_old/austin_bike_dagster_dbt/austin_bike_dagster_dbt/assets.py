from dagster import AssetExecutionContext, multi_asset, AssetOut
from dagster_dbt import DbtCliResource, dbt_assets
import subprocess
from typing import Tuple
from .project import austin_bike_dbt_project

@multi_asset(
    outs={
        "austin_bikeshare_stations": AssetOut(key=["meltano", "austin_bikeshare_stations"]),
        "austin_bikeshare_trips": AssetOut(key=["meltano", "austin_bikeshare_trips"])
    }
)
def meltano_austin_bike_pipeline() -> Tuple[None, None]:
    """
    Runs meltano tap-postgres target-bigquery
    """
    cmd = ["meltano", "run", "tap-postgres", "target-bigquery"]
    cwd = '/Users/aiml/Documents/VSCode-Git/sctp-dsai-ds2-coaching-elt-e2e-dagster/austin_bike_elt_project/meltano-austin-bike'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)
    return (None, None)

@dbt_assets(manifest=austin_bike_dbt_project.manifest_path)
def austin_bike_dbt_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    