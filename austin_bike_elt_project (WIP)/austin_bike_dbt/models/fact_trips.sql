{{ config(
    materialized='table'
) }}
SELECT
    trip_id,
    subscriber_type,
    bike_id,
    bike_type,
    start_time,
    start_station_id,
    start_station_name,
    end_station_id,
    end_station_name,
    duration_minutes
FROM {{ source('austin_bike_meltano_raw', 'public_austin_bikeshare_trips') }}
