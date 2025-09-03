from dagster import AssetExecutionContext, multi_asset, AssetOut, MaterializeResult, MetadataValue, AssetKey
from dagster_dbt import DbtCliResource, dbt_assets
from typing import Tuple
import subprocess
import os

from .project import dbt_austin_bikeshare_project

# =============================================================================
# MELTANO EXTRACTION ASSETS
# =============================================================================

@multi_asset(
    outs={
        "austin_bikeshare_stations": AssetOut(key=["meltano", "public_austin_bikeshare_stations"]),
        "austin_bikeshare_trips": AssetOut(key=["meltano", "public_austin_bikeshare_trips"])
    },
        description="Extract Austin bikeshare data from Postgres to BigQuery via Meltano",
    compute_kind="meltano",
)
def meltano_austin_bike_pipeline(context: AssetExecutionContext) -> Tuple[MaterializeResult, MaterializeResult]:
    """
    Multi-asset function that runs a single Meltano job to extract and load 2 tables.
    """
    # Path to Meltano project directory
    meltano_project_dir = os.path.join(os.path.dirname(__file__), "..", "..", "meltano_austin_bikeshare")

    # Execute Meltano job via subprocess
    result = subprocess.run(
        ["meltano", "run", "meltano_elt_bq"],  # Actual job name
        cwd=meltano_project_dir,
        capture_output=True,
        text=True
    )

    # Log output for debugging
    context.log.info(f"Meltano stdout: {result.stdout}")
    if result.stderr:
        context.log.info(f"Meltano stderr: {result.stderr}")
    
    # Handle errors
    if result.returncode != 0:
        context.log.error(f"Meltano job failed with return code {result.returncode}")
        raise Exception("Meltano job failed. Check logs above for details.")
    
    # Return tuple of MaterializeResult (order matches outs definition)
    return (
        MaterializeResult(
            asset_key=AssetKey(['meltano', 'public_austin_bikeshare_trips']),
            metadata={
                "meltano_job": MetadataValue.text("meltano_elt_bq"),
                "table": MetadataValue.text("public_austin_bikeshare_trips"),
                "extraction_method": MetadataValue.text("meltano_subprocess")
            }
        ),
        MaterializeResult(
            asset_key=AssetKey(['meltano', 'public_austin_bikeshare_stations']),
            metadata={
                "meltano_job": MetadataValue.text("meltano_elt_bq"),
                "table": MetadataValue.text("public_austin_bikeshare_stations"),
                "extraction_method": MetadataValue.text("meltano_subprocess")
            }
        )
    )

@dbt_assets(manifest=dbt_austin_bikeshare_project.manifest_path)
def dbt_austin_bikeshare_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    