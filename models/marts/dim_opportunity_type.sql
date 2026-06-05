{{ config(materialized='table') }}

with opportunities as (
    select distinct
        opportunity_type
    from {{ ref('stg_salescloud__opportunity') }}
    where opportunity_type is not null
)

select
    row_number() over (order by opportunity_type) as opportunity_type_id,
    opportunity_type
from opportunities
