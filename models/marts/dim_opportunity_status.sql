{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stage_summary as (
    select
        stage_name,
        count(*) as opportunity_count,
        count(case when is_won = true then 1 end) as won_count,
        count(
            case when is_closed = true and is_won = false then 1 end
        ) as lost_count,
        count(case when is_closed = false then 1 end) as open_count,
        sum(amount) as total_pipeline_value,
        avg(probability) as avg_probability
    from opportunities
    group by stage_name
),

final as (
    select
        opportunity_count,
        won_count,
        lost_count,
        open_count,
        total_pipeline_value,
        avg_probability,
        stage_name as opportunity_stage,
        case
            when stage_name like '%Closed Won%' then 'Won'
            when stage_name like '%Closed Lost%' then 'Lost'
            else 'Open'
        end as stage_category,
        case
            when opportunity_count > 0
                then round(won_count * 100.0 / opportunity_count, 2)
        end as win_rate_pct
    from stage_summary
)

select * from final
