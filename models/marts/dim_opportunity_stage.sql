{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

stage_summary as (
    select
        -- Primary key
        stage_name,

        -- Stage counts
        count(*) as opportunity_count,

        count(case when is_closed = false then 1 end) as open_count,

        count(case when is_closed = true and is_won = true then 1 end) as won_count,

        count(case when is_closed = true and is_won = false then 1 end) as lost_count,

        -- Stage amounts
        sum(amount) as total_amount,

        sum(case when is_closed = false then amount end) as open_amount,

        sum(case when is_closed = true and is_won = true then amount end) as won_amount,

        -- Average win probability
        avg(probability) as avg_probability

    from opportunities
    group by stage_name
)

select * from stage_summary
