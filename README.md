# SCTP DSAI DS2 Coaching ELT E2E Dagster

In this coaching exercise, we will be performing an end-to-end Dagster orchestration using the HDB resale price dataset which we have practice in lesson 2.6 and lesson 2.7.

This folder has 4 main folder, they are 
```tree
    .
    |-- hdb_resale_elt_dagster_project/
    |-- austin_bikeshare_elt_dagster_project/
    |-- austin_bikeshare_e2e_dagster_project/ (Different Implementation)  
    |-- meltano_csv_to_postgres/ (Not Dagster)    
    └── README.md (this instruction)
```

- `hdb_resale_elt_dagster_project` contain a full end-to-end dagster orchestration of an entire ELT pipeline, it includes 2 dagster folder, a dbt folder and a meltano folder. This project uses HDB resale data from lesson 2.6.
- `austin_bikeshare_elt_dagster_project` is another dagster implementation, using Austin Bikeshare data from Google.
- `austin_bikeshare_e2e_dagster_project` is a different dagster implementation using same data. In this implementation, we use methods recommended by Alvin.
- `meltano_csv_to_postgres` is not a dagster implementation. It demonstrate the steps and settings require to upload csv files to Postgres database (Supabase) using Austin Bikeshare data as an exmaple.


## HDB Resale ELT Dagster Orchestration
- `hdb_resale_elt_dagster_project` contain a full end-to-end dagster orchestration, it includes 2 dagster folder, a dbt folder and a meltano folder.
- In this project, we show 2 different implementation of Dagster.
- The following is the folder structure. 
```tree
    .
    |-- hdb_resale_elt_dagster_project/
    |   |-- dagster_dbt_integration_hdb_resale/
    |   |   └── ... --dagster sub folders--
    |   |-- dagster_dbt_resale_subprocess/
    |   |   └── ... --dagster sub folders--
    |   |-- dbt_hdb_resale/
    |   |   └── ... --dbt sub folders--
    |   |-- meltano_hdb_resale/
    |   |   └── ... --meltano sub folders--
    |   └── HDB_Resale_Dagster_README.md (Detailed instructions for HDB Resale Dagster Orchestration)
    |-- ... __other_folders__
    └── README.md (this instruction)
```

- Under the folder `hdb_resale_elt_dagster_project`, we have two different implementations of the dagster orchestration. You can choose one of them or implement both.
- The detailed instruction is under the folder `hdb_resale_elt_dagster_project`.
- To practice this orchestration, you can use the current `hdb_resale_elt_dagster_project` folder and change the GCP settings in the Meltano and dbt folder and run the project.
- If you want to practice a new setup, you can create another project folder with different name and copy the instruction to the new project folder and follow the instructions.  

## Austin Bikeshare ELT Dagster Orchestration I
- `austin_bikeshare_elt_dagster_project` contain a full end-to-end dagster orchestration, it includes a dagster folder, dbt folder and meltano folder.
- The following is the folder structure. 
```tree
    .
    |-- austin_bikeshare_elt_dagster_project/
    |   |-- dagster_dbt_integration_austin_bikeshare/
    |   |   └── ... --dagster sub folders--
    |   |-- dbt_austin_bikeshare/
    |   |   └── ... --dbt sub folders--
    |   |-- meltano_austin_bikeshare/
    |   |   └── ... --meltano sub folders--
    |   └── Austin_Bikeshare_Dagster_README.md (Detailed instructions for Austin Bikeshare Dagster Orchestration)
    |-- ... __other_folders__
    └── README.md (this instruction)
```

- Under `austin_bikeshare_elt_dagster_project`, we should have 3 separate folder, one for Dagster, one for Meltano and one for dbt.
- The detailed instruction is under the folder `austin_bikeshare_elt_dagster_project`.
- To practice this orchestration, you can use the current `austin_bikeshare_elt_dagster_project` folder and change the GCP settings in the Meltano and dbt folder and run the project.
- If you want to practice a new setup, you can create another project folder with different name and copy the instruction to the new project folder and follow the instructions.

## Austin Bikeshare ELT Dagster Orchestration II
- `austin_bikeshare_e2e_dagster_project` contain a full end-to-end dagster orchestration with different implementation.
- The key differences is that we create a job in meltano and run the job instead of running `meltano run tap-postgres target-bigquery`.
- We also add more context and materialized results in the asset definitions.