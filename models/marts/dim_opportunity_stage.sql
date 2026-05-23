{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stages as (
    select distinct
        stage_name,
        is_closed

    from opportunities
),

final as (
    select
        -- Primary key (natural key)
        stage_name as opportunity_stage_id,

        -- Stage attributes
        stage_name,
        is_closed,
        case
            when stage_name = 'Closed Won' then true
            when is_closed = true then false
            else false
        end as is_won_stage

    from stages
)

select * from final
