{{ config(materialized='table') }}
-- Dimension table for opportunity stages: pipeline volume per stage.
-- Added for VD-2289/VD-2290 gate-3/gate-4 validation.

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stage_summary as (
    select
        stage_name,
        count(*) as opportunity_count,
        sum(amount) as total_amount,
        avg(probability) as avg_probability,
        sum(case when is_won then 1 else 0 end) as won_count,
        sum(
            case when is_closed and not is_won then 1 else 0 end
        ) as lost_count,
        sum(case when not is_closed then 1 else 0 end) as open_count
    from opportunities
    group by stage_name
)

select * from stage_summary
