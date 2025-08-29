"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""
from dagster_dbt import build_schedule_from_dbt_selection
from dagster import ScheduleDefinition, define_asset_job
from .assets import dbt_resale_dbt_assets, pipeline_meltano

# Create a job that includes both assets
etl_job = define_asset_job(
    name="materialize_elt",
    selection=[pipeline_meltano, dbt_resale_dbt_assets]
)

# Create schedule for the job
schedules = [
    ScheduleDefinition(
        job=etl_job,
        cron_schedule="0 6 5 * *",  
        name="monthly_etl_schedule"
    )
]