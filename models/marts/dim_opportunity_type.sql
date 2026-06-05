{{ config(materialized='table') }}

with opportunities as (

    select * from {{ ref('stg_salescloud__opportunity') }}

),

types as (

    select distinct opportunity_type
    from opportunities
    where opportunity_type is not null

),

final as (

    select
        opportunity_type,
        row_number() over (order by opportunity_type) as opportunity_type_id
    from types

)

select * from final
