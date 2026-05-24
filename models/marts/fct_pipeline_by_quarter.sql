{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

quarter_metrics as (
    select
        fiscal_year,
        fiscal_quarter,

        count(opportunity_id) as opportunity_count,
        count(case when is_won = true then 1 end) as won_count,
        count(case when is_closed = true and is_won = false then 1 end)
            as lost_count,
        count(case when is_closed = false then 1 end) as open_count,

        coalesce(sum(amount), 0) as total_amount,
        coalesce(sum(case when is_won = true then amount end), 0) as won_amount,
        coalesce(sum(case when is_closed = false then amount end), 0)
            as open_pipeline_amount,

        avg(probability) as avg_probability

    from opportunities
    where
        fiscal_year is not null
        and fiscal_quarter is not null
    group by
        fiscal_year,
        fiscal_quarter
),

final as (
    select
        fiscal_year,
        fiscal_quarter,
        opportunity_count,

        won_count,
        lost_count,
        open_count,
        total_amount,

        won_amount,

        open_pipeline_amount,
        avg_probability,
        concat(cast(fiscal_year as string), '-', fiscal_quarter)
            as fiscal_period,
        case
            when (won_count + lost_count) > 0
                then
                    round(
                        won_count
                        / cast(won_count + lost_count as decimal(10, 4)),
                        4
                    )
        end as win_rate

    from quarter_metrics
)

select * from final
