{{ config(materialized='table') }}

with won_opportunities as (
    select * from {{ ref('fct_pipeline') }}
    where is_won = true
),

rep_summary as (
    select
        -- Surrogate key (grain: owner_id + fiscal_year + fiscal_quarter)
        {{ dbt_utils.generate_surrogate_key(['owner_id', 'fiscal_year', 'fiscal_quarter']) }}
            as rep_period_id,

        -- Grain: one row per sales rep per fiscal year and quarter
        owner_id,
        owner_name,
        owner_email,
        owner_is_active,
        fiscal_quarter,
        fiscal_year,

        -- Counts
        count(opportunity_id) as won_opportunities_count,

        -- Revenue metrics
        sum(amount) as total_won_amount,
        sum(weighted_amount) as total_weighted_amount,

        -- Sales velocity
        avg(sales_cycle_days) as avg_sales_cycle_days,
        min(sales_cycle_days) as min_sales_cycle_days,
        max(sales_cycle_days) as max_sales_cycle_days,

        -- Date range of wins
        min(close_date) as first_close_date,
        max(close_date) as last_close_date

    from won_opportunities
    group by
        owner_id,
        owner_name,
        owner_email,
        owner_is_active,
        fiscal_quarter,
        fiscal_year
)

select * from rep_summary
