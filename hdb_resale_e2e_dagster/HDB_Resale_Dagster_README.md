# SCTP DSAI DS2 Coaching ELT  E2E Dagster - HDB Resale Price End to End Orchestration

You can change the current GCP settings in Meltano and dbt to get the project run. If you want to practice, you can create a new project folder as follows:

```bash
mkdir hdb_resale_e2e_dagster # Use different folder name for your practice
```

## HDB Resale Price End to End Orchestration Setup Meltano
This is the identical copy of the exercise in 2.6. We can use the same environment `dagster` which we created.

### Add an Extractor to Pull Data from Postgres (Supabase)

We will use the `tap-postgres` extractor to pull data from a Postgres database hosted on [Supabase](https://supabase.com). 

The Postgres database table with the HDB housing data of resale flat prices based on registration date from Jan-2017 onwards. It is the same data that we used in 2.6. We will be extracting data from a data ready postgres server, if you want to setup and upload your data please refer to the setup guide in exercise 2.6.

From Supabase, take note of your connection details from the Connection window, under Session Spooler:

```yaml
host: aws-0-us-east-2.pooler.supabase.com
port: 5432
database: postgres
user: postgres.ufkutyufdohbogiqgjel
pool_mode: session
```

We're going to add an extractor for Postgres to get our data. An extractor is responsible for pulling data out of any data source. We will use the `tap-postgress` extractor to pull data from the Supabase server. 

At the root folder, create a new Meltano project by running:

```bash
meltano init meltano_hdb_resale
cd meltano_hdb_resale
```

To add the extractor to our project, run:

```bash
meltano add extractor tap-postgres
```

Next, configure the extractor by running:

```bash
meltano config tap-postgres set --interactive
```

Configure the following options:

- `database`: `postgres`
- `filter_schemas`: `['public']`
- `host`: `aws-0-ap-southeast-1.pooler.supabase.com` *(example)*
- `password`: *database password*
- `user`: *postgres.username*


Next, we need to select the table that we need:
```bash
meltano select tap-postgres "public-resale_flat_prices_from_jan_2017"
```

Use the following command to list
```bash
meltano select tap-postgres --list
```

Test your configuration:
```bash
meltano config tap-postgres test
```

### Add an Loader to Load Data to BigQuery
We will now add a loader to load the data into BigQuery.
```bash
meltano add loader target-bigquery
```

```bash
meltano config target-bigquery set --interactive
```

Set the following options:

- `batch_size`: `104857600`
- `credentials_path`: _full path to the service account key file_
- `dataset`: `resale`
- `denormalized`: `true`
- `flattening_enabled`: `true`
- `flattening_max_depth`: `1`
- `method`: `batch_job`
- `project`: *your_gcp_project_id*


### Run Supabase (Postgres) to BigQuery

We can now run the full ingestion (extract-load) pipeline from Supabase to BigQuery.

```bash
meltano run tap-postgres target-bigquery
```

You will see the logs printed out in your console. Once the pipeline is completed, you can check the data in BigQuery.



## HDB Resale Price End to End Orchestration Setup dbt

Let's create a Dbt project to transform the data in BigQuery. 

To create a new dbt project. (make sure you exited the meltano folder)

```bash
dbt init dbt_hdb_resale
```

Fill in the required config details. 
- use service account
- add your path of the json key file
- dataset: resale
- project: your GCP project ID

Please note that the profiles is located at the hidden folder .dbt of your home folder. The `profiles.yml` that is located in the home folder includes multiple projects. Alternatively, you can create a separate `profiles.yml` for each project.

To create separate profiles for each project, create a new file called `profiles.yml` under `resale_flat` folder. Then copy the following to `profiles.yml`. Remember to change your key file location and your project ID.
```yaml
resale_flat:
  outputs:
    dev:
      dataset: resale
      job_execution_timeout_seconds: 300
      job_retries: 1
      keyfile: /Users/zanelim/Downloads/personal/secret/meltano-learn-03934027c1d8.json # Use your path of key file
      location: US
      method: service-account
      priority: interactive
      project: meltano-learn # enter your google project id
      threads: 1
      type: bigquery
  target: dev
```

### Create source and models

We can start to create the source and models in the dbt project.

> 1. Create a `source.yml` which points to the `ingestion` schema and `resale_flat_prices_from_jan_2017` table.
> 2. Create a `prices.sql` model (materialized table) which selects all columns from the source table, cast the `floor_area_sqm` to numeric, then add a new column `price_per_sqm` which is the `resale_price` divided by `floor_area_sqm`.
> 3. Create a `prices_by_town_type_model.sql` model (materialized table) which selects the `town`, `flat_type` and `flat_model` columns from `prices`, group by them and calculate the average of `floor_area_sqm`, `resale_price` and `price_per_sqm`. Finally, sort by `town`, `flat_type` and `flat_model`.

### Run Dbt

Check dbt connection first

```bash
dbt debug
```

Optional: you can run `dbt clean` to clear any logs or run file in the dbt folders.

Run the dbt project to transform the data.

```bash
dbt run
```

You should see 2 new tables in the `resale_flat` dataset.

## Dagster Using Subprocess

This is similar to lesson 2.7 Extra - Hands-on with Orchestration I, where we use the code of pipelinetwo.py as our assets. We did modified the dbt seed into meltano command.

First the create a project at root project folder

```bash
dagster project scaffold --name dagster_hdb_resale_subprocess
```

Please check the `assets.py` and `definitions.py` for details.

```python
# assets.py
from dagster import asset
import subprocess


@asset
def pipeline_meltano()->None:
    """
    Runs meltano tap-postgres target-bigquery
    """
    cmd = ["meltano", "run", "tap-postgres", "target-bigquery"]
    # path to meltano folder
    cwd = '/path/to/your/folder/meltano_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)

@asset(deps=[pipeline_meltano])
def pipeline_dbt_run()->None:
    """
    Runs dbt run 
    """
    cmd = ["dbt", "run"]
    cwd = '/path/to/your/folder/dbt_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)

@asset(deps=[pipeline_dbt_run])
def pipeline_dbt_test()->None:
    """
    Runs dbt test 
    """
    cmd = ["dbt", "test"]
    cwd = '/path/to/your/folder/dbt_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)  
```

```python
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
    cron_schedule="0 2 * * *",
    name="daily_elt_schedule",
    description="Daily resale data pipeline"
)

defs = Definitions(
    assets=all_assets,
    jobs=[elt_job],
    schedules=[daily_schedule],
)

```

The resulting lineage graph is as follows:

![assets/subprocess.png](../assets/subprocess.png)


While this process works, we cannot the much details in dbt. Thankfully, there is dbt and Dagster integration as follows.

## Dagster Using dbt Integration

This is similar to lesson 2.7 Extra - Hands-on with Orchestration II, where we create a dbt-dagster integrated project and we add meltano as a subprocess.

Use the following command:

```bash
dagster-dbt project scaffold --project-name dagster_dbt_integration_hdb_resale --dbt-project-dir #full-path-to-the-resale-flat-dbt-project-directory
```
If you run `dagster dev` at this stage, you can see the asset lineage graph as follows:

![alt text](../assets/dbt-integration-raw.png)

If you have more complex dimension table, it will present here and the dependencies are automatically resolved by Dagster. Furthermore, we do not need to run dbt test, if you look at the box under `prices`, there is a row call `check`. So when they are materializing the prices table, it will perform dbt test at the same time.

Next we would like to add meltano as subprocess.

```python
# assets.py
from dagster import AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets

from .project import dbt_hdb_resale_project

import subprocess

@asset(compute_kind="meltano")
def pipeline_meltano()->None:
    """
    Runs meltano tap-postgres target-bigquery
    """
    cmd = ["meltano", "run", "tap-postgres", "target-bigquery"]
    cwd = '/path/to/meltano/folder/meltano_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)

@dbt_assets(manifest=dbt_hdb_resale_project.manifest_path)
def dbt_hdb_resale_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
```

On `definitions.py` we add meltano pipeline into the definitions
```python
# definitions.py
from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_hdb_resale_dbt_assets, pipeline_meltano
from .project import dbt_hdb_resale_project
from .schedules import schedules

defs = Definitions(
    assets=[pipeline_meltano, dbt_hdb_resale_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_hdb_resale_project)
    },
)
```

If you run `dagster dev` at this stage, you can see the lineage graph as follows:

![alt text](../assets/dbt-integration-meltano.png)

This lineage graph is not ideal as there is no dependency between meltano and dbt.

The dependency can be set in dbt `source.yml` as follows:

```yml
version: 2
sources:
  - name: resale
    tables:
      - name: public_resale_flat_prices_from_jan_2017
        meta:
          dagster:
            asset_key: ["pipeline_meltano"]
```

The final lineage graph is as follows:

![alt text](../assets/dbt-integration-final.png)