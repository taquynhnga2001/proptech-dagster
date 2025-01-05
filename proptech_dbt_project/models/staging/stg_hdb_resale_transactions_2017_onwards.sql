{{ config(
    materialized = 'incremental',
    on_schema_change='fail'
    )
}}

WITH source AS (
    SELECT 
        CAST(month AS STRING) AS month,
        CAST(town AS STRING) AS town,
        CAST(flat_type AS STRING) AS flat_type,
        CAST(block AS STRING) AS block,
        CAST(street_name AS STRING) AS street_name,
        CAST(storey_range AS STRING) AS storey_range,
        CAST(floor_area_sqm AS FLOAT64) AS floor_area_sqm,
        CAST(flat_model AS STRING) AS flat_model,
        CAST(lease_commence_date AS INT64) AS lease_commence_date,
        CAST(remaining_lease AS STRING) AS remaining_lease,
        CAST(resale_price AS FLOAT64) AS resale_price,
        CONCAT(
            month, '_', town, '_', flat_type, '_', block, '_', street_name, '_', 
            storey_range, '_', floor_area_sqm, '_', flat_model, '_', lease_commence_date,
            '_', remaining_lease, '_', resale_price
        ) as concat_columns
    FROM {{ source('property_trans', 'hdb_resale_transactions_2017_onwards_') }}
)

SELECT 
    source.*,
    current_timestamp() AS ingestion_timestamp,
FROM source

{% if is_incremental() %}
LEFT JOIN {{ this }} AS stg
    ON source.concat_columns = stg.concat_columns
WHERE stg.concat_columns IS NULL
{% endif %}