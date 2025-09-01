# SCTP DSAI DS2 Coaching ELT E2E Dagster

In this coaching exercise, we will be performing an end-to-end Dagster orchestration using the HDB resale price dataset which we have practice in lesson 2.6 and lesson 2.7.

The detailed instruction is under the folder `hdb_resale_e2e_dagster`.

This folder has 
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
    |   └── HDB_Resale_Dagster_README.md (Detailed instructions for HDB resale Dagster Orchestration)
    └── README.md (this instruction)
```

- Under the folder `hdb_resale_e2e_dagster`, we have two different implementation of the dagster orchestration. Please choose one of them.
- So in Dagster orchestration, we should have 3 separate folder, one for Dagster, one for Meltano and one for dbt.
- To practice this orchestration, you can use the current `hdb_resale_e2e_dagster` folder and change the profiles setting and GCP settings in the Meltano folder and run the project.
- If you want to practice a new setup, you can create another project folder with different name and copy the instruction to the new project folder and follow the instructions.  
