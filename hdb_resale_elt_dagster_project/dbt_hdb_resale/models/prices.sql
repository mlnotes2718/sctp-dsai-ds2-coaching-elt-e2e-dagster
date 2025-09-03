{{ config(materialized='table') }}

WITH RAW AS (
    SELECT
        month,
        town,
        flat_type,
        block,
        street_name,
        storey_range,
        CAST(floor_area_sqm AS FLOAT64) AS floor_area_sqm,
        flat_model,
        lease_commence_date,
        remaining_lease,
        CAST(resale_price AS FLOAT64) AS resale_price
    FROM {{ source('raw_hdb_resale_elt', 'public_resale_flat_prices_from_jan_2017') }}
)
SELECT
    *,
    resale_price / floor_area_sqm AS price_per_sqm
FROM raw
