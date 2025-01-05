{{ config(
    cluster_by="month"
    ) 
}}

WITH trans_2015_to_2016 AS (
    SELECT  
        month,
        town,
        flat_type,
        block,
        street_name,
        storey_range,
        floor_area_sqm,
        flat_model,
        lease_commence_date,
        remaining_lease,
        resale_price
    FROM {{ ref('stg_hdb_resale_transactions_2015-2016') }}
),

trans_2017_onwards AS (
    SELECT  
        month,
        town,
        flat_type,
        block,
        street_name,
        storey_range,
        floor_area_sqm,
        flat_model,
        lease_commence_date,
        remaining_lease,
        resale_price
    FROM {{ ref('stg_hdb_resale_transactions_2017_onwards') }}
),

all_trans AS (
    SELECT * FROM trans_2015_to_2016
    UNION ALL 
    SELECT * FROM trans_2017_onwards
)


SELECT 
    *,
    current_timestamp() AS ingestion_timestamp
FROM all_trans
