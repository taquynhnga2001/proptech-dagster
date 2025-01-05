{{ config(
    materialized = 'incremental',
    on_schema_change='fail'
    )
}}

WITH source AS (
    SELECT 
        *,
        CONCAT(
            month, '_', town, '_', flat_type, '_', block, '_', street_name, '_', 
            storey_range, '_', floor_area_sqm, '_', flat_model, '_', lease_commence_date,
            '_', remaining_lease, '_', resale_price
        ) as concat_columns
    FROM {{ source('property_trans', 'hdb_resale_transactions_2017_onwards') }}
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