{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stage_metrics as (
    select
        stage_name,

        count(opportunity_id)                                           as opportunity_count,
        count(case when is_won = true then 1 end)                      as won_count,
        count(case when is_closed = true and is_won = false then 1 end) as lost_count,
        count(case when is_closed = false then 1 end)                   as open_count,

        sum(amount)                                                     as total_amount,
        sum(case when is_closed = false then amount else 0 end)         as open_pipeline_amount,
        sum(case when is_won = true then amount else 0 end)             as won_amount,

        avg(probability)                                                as avg_probability,

        avg(
            case when is_closed = true and days_until_close is not null
            then abs(days_until_close)
            end
        )                                                               as avg_days_to_close,

        min(created_date)                                               as earliest_created_date,
        max(created_date)                                               as latest_created_date

    from opportunities
    group by stage_name
)

select * from stage_metrics
