# Meltano Tap-CSV Target-Postgres (Supabase)
This is not part of the orchestration. This is for anyone want to learn using Meltano to transfer csv files to Supabase (Postgres). 

We are using Austin Bikeshare data. `austin_bikeshare_stations.csv` is small. However, the data `bikeshare_trips.csv` is ver large (2million+ rows), it exceeded the size allowed for Supabase free tier. We only extracted 300,000 rows for practice. We use `split_data.py` to sample 300k records. 

To practice this meltano exercise, you can create a new folder at the root folder and copy this MD file to the new folder. We will be using the `dagster` environment.

```bash
conda activate dagster
```

1. Prepare and get read your csv files. You can also get the csv files from the current `meltano_csv_to_postgres` folder. You can also modified the `split_data.py` to reduce the data size.

2. Create Meltano project
```bash
meltano init meltano_csv_to_postgres # Use different folder name if you want to practice
cd meltano_csv_to_postgres
```

3. If you are creating a fresh project, make data directory and copy csv files.
```bash
mkdir data
```
- copy csv files to data folder
- (optional) add `/data` to `.gitignore` under the meltano folders

4. Add csv extractor
```bash
meltano add extractor tap-csv 
```

5. We can add the config, we found that for csv files, it is best to configure directly in the file `meltano.yml`:
```yml
plugins:
  extractors:
  - name: tap-csv
    variant: meltanolabs
    pip_url: git+https://github.com/MeltanoLabs/tap-csv.git
    config:
      files:
      - entity: austin_bikeshare_stations
        path: data/austin_bikeshare_stations.csv
        keys: [station_id]
      - entity: austin_bikeshare_trips
        path: data/austin_bikeshare_trips_small.csv
        keys: [trip_id]
```

6. Test tap configuration
```bash
meltano config tap-csv test
```

7. Add postgres target
```bash
meltano add loader target-postgres
```

8. Set target config
```bash
meltano config target-postgres set --interactive
```
Connection details is as follow:
```yaml
host: aws-0-us-east-2.pooler.supabase.com
port: 5432
database: postgres
user: postgres.ufkutyufdohbogiqgjel
pool_mode: session
```


9. Set config using the following settings
- `batch_size_rows`: 100000
- `database`: `postgres`
- `default_target_schema`: `public`
- `host`: `aws-0-ap-southeast-1.pooler.supabase.com` *(example)*
- `password`: *database password*
- `user`: *postgres.username*

In the `meltano.yml` file, the settings should be similar to below:
```yml
  loaders:
  - name: target-postgres
    variant: meltanolabs
    pip_url: meltanolabs-target-postgres
    config:
      batch_size_rows: 100000
      database: postgres
      default_target_schema: public
      host: aws-0-us-east-2.pooler.supabase.com
      user: postgres.ufkutyufdohbogiqgjel
```

10. Run the meltano ingestion
```bash
meltano run tap-csv target-postgres 
```

> Note: Depending on the time of the day and resource available by Supabase, the number of batch size by rows differs between 1000 to 200000. Please test with a smaller batch size and increase slowly.

> Note: You may need to enable row level security in Supabase.
