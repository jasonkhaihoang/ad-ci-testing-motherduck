{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stage_summary as (
    select
        stage_name,
        count(*) as opportunity_count,
        sum(amount) as total_amount,
        avg(amount) as avg_amount,
        sum(case when is_won then 1 else 0 end) as won_count,
        sum(case when is_closed and not is_won then 1 else 0 end) as lost_count
    from opportunities
    group by stage_name
)

select * from stage_summary
