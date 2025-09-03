# assets.py
from dagster import asset
import subprocess


@asset(compute_kind="meltano")
def pipeline_meltano()->None:
    """
    Runs meltano tap-postgres target-bigquery
    """
    cmd = ["meltano", "run", "tap-postgres", "target-bigquery"]
    # path to meltano folder
    cwd = '/Users/aiml/Downloads/sctp-dsai-ds2-coaching-elt-e2e-dagster/hdb_resale_elt_dagster_project/meltano_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)

@asset(deps=[pipeline_meltano], kinds={"dbt", "bigquery"})
def pipeline_dbt_run()->None:
    """
    Runs dbt run 
    """
    cmd = ["dbt", "run"]
    cwd = '/Users/aiml/Downloads/sctp-dsai-ds2-coaching-elt-e2e-dagster/hdb_resale_elt_dagster_project/dbt_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output)

@asset(deps=[pipeline_dbt_run], kinds={"dbt", "bigquery"})
def pipeline_dbt_test()->None:
    """
    Runs dbt test 
    """
    cmd = ["dbt", "test"]
    cwd = '/Users/aiml/Downloads/sctp-dsai-ds2-coaching-elt-e2e-dagster/hdb_resale_elt_dagster_project/dbt_hdb_resale'
    try:
        output= subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
            output = e.output.decode()
            raise Exception(output) 
