# schedules.py
"""
To add a schedule that materializes your dbt assets.
"""
from dagster import define_asset_job, ScheduleDefinition
from .assets import dbt_austin_bikeshare_dbt_assets, meltano_austin_bikeshare_pipeline

# Create a job that includes both assets
e2e_etl_job = define_asset_job(
    name="materialize_elt",
    selection=[meltano_austin_bikeshare_pipeline, dbt_austin_bikeshare_dbt_assets]
)

# Create schedule for the job
schedules = [
    ScheduleDefinition(
        job=e2e_etl_job,
        cron_schedule="0 6 5 * *",  # 5th of every month at 6 AM
        name="monthly_etl_schedule"
    )
]