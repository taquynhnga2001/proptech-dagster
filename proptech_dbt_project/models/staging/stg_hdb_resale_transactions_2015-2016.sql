WITH source AS (
    SELECT
        * 
    FROM {{ source('property_trans', 'hdb_resale_transactions_2015-2016') }}
)

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
    CONCAT(remaining_lease, ' years') as remaining_lease,
    resale_price,
    current_timestamp() AS ingestion_timestamp,
FROM source
ORDER BY month