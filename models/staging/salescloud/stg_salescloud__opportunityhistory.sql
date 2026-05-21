{{ config(materialized='view') }}

-- VD-2097: brand-new model to exercise Gate 5 brand-new-artifact rendering.
-- Constant SELECT avoids depending on prod source columns we can't verify
-- pre-CI. The point of this model is to land in the deployment manifest
-- with pre_existing_in_prod: false so Gate 5 routes it to brand-new.
select
    cast(1 as bigint)               as opportunity_history_id,
    cast('opp-1' as string)         as opportunity_id,
    cast('Stage' as string)         as field_name,
    cast('Prospecting' as string)   as old_value,
    cast('Qualification' as string) as new_value,
    cast(current_timestamp as timestamp) as created_at,
    cast('user-1' as string)        as created_by_id
