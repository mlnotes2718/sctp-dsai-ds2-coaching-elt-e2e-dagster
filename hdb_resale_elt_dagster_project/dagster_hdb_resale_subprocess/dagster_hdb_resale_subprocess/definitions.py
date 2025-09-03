# definitions.py
from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)
# import all assets
import dagster_hdb_resale_subprocess.assets as assets_module

all_assets = load_assets_from_modules([assets_module])

# Complete ELT pipeline job
elt_job = define_asset_job(
    name="daily_elt_pipeline",
    selection="*",
    description="Meltano extraction → dbt transformation → data quality tests"
)

# Daily schedule at 2 AM
daily_schedule = ScheduleDefinition(
    job=elt_job,
    cron_schedule="0 11 * * *", # Daily at 11 AM
    name="daily_elt_schedule",
    description="Daily resale data pipeline"
)

defs = Definitions(
    assets=all_assets,
    jobs=[elt_job],
    schedules=[daily_schedule],
)
