# SCTP DSAI DS2 Coaching ELT E2E Dagster

In this coaching exercise, we will be performing an end-to-end Dagster orchestration using the HDB resale price dataset which we have practice in lesson 2.6 and lesson 2.7.

This folder has 3 main folder, they are 
```tree
    .
    |-- hdb_resale_e2e_dagster/
    |-- austin_bikeshare_e2e_dagster/
    |-- meltano_csv_to_postgres/    
    └── README.md (this instruction)
```

- `hdb_resale_e2e_dagster` contain a full end-to-end dagster orchestration of an entire ELT pipeline, it includes a dagster folder, dbt folder and meltano folder. This project uses HDB resale data from lesson 2.6.
- `austin_bikeshare_e2e_dagster` is another dagster implementation, using Austin Bikeshare data from Google.
- `meltano_csv_to_postgres` is not a dagster implementation, however, it demonstrate the settings require to upload csv files to Postgres database (Supabase).


## HDB Resale ELT Dagster Orchestration
- `hdb_resale_e2e_dagster` contain a full end-to-end dagster orchestration, it includes a dagster folder, dbt folder and meltano folder.
- However, in this project, we show 2 different implementation of dagster, therefore we have 2 different dagster folder.
- The following is the folder structure. 
```tree
    .
    |-- hdb_resale_e2e_dagster/
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

- Under the folder `hdb_resale_e2e_dagster`, we have two different implementations of the dagster orchestration. Please choose one of them.
- The detailed instruction is under the folder `hdb_resale_e2e_dagster`.
- To practice this orchestration, you can use the current `hdb_resale_e2e_dagster` folder and change the GCP settings in the Meltano and dbt folder and run the project.
- If you want to practice a new setup, you can create another project folder with different name and copy the instruction to the new project folder and follow the instructions.  

## Austin Bikeshare ELT Dagster Orchestration
- `austin_bikeshare_e2e_dagster` contain a full end-to-end dagster orchestration, it includes a dagster folder, dbt folder and meltano folder.
- The following is the folder structure. 
```tree
    .
    |-- austin_bikeshare_e2e_dagster/
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

- Under `austin_bikeshare_e2e_dagster`, we should have 3 separate folder, one for Dagster, one for Meltano and one for dbt.
- The detailed instruction is under the folder `austin_bikeshare_e2e_dagster`.
- To practice this orchestration, you can use the current `austin_bikeshare_e2e_dagster` folder and change the GCP settings in the Meltano and dbt folder and run the project.
- If you want to practice a new setup, you can create another project folder with different name and copy the instruction to the new project folder and follow the instructions.  