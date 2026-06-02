{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stage_summary as (
    select
        stage_name,
        count(*)                                                          as opportunity_count,
        sum(case when is_won then 1 else 0 end)                           as won_count,
        sum(case when is_closed and not is_won then 1 else 0 end)         as lost_count,
        sum(case when not is_closed then 1 else 0 end)                    as open_count,
        sum(amount)                                                        as total_pipeline_value,
        avg(probability)                                                   as avg_probability
    from opportunities
    group by stage_name
),

final as (
    select
        -- Primary key
        stage_name                                          as opportunity_stage,

        -- Stage classification
        case
            when stage_name ilike '%closed won%' then 'Won'
            when stage_name ilike '%closed lost%' then 'Lost'
            else 'Open'
        end                                                 as stage_category,

        -- Counts
        opportunity_count,
        won_count,
        lost_count,
        open_count,

        -- Pipeline value
        total_pipeline_value,
        avg_probability,

        -- Win rate (avoid divide-by-zero)
        case
            when opportunity_count > 0
                then round(won_count * 100.0 / opportunity_count, 2)
        end                                                 as win_rate_pct

    from stage_summary
)

select * from final
