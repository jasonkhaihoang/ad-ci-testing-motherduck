{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

final as (
    select
        opportunity_id,
        account_id,
        owner_id,
        opportunity_name,
        stage_name,
        opportunity_type,
        lead_source,
        amount,
        close_date,
        fiscal_quarter,
        fiscal_year,
        created_date,
        last_modified_date
    from opportunities
    where
        is_won = true
        and is_closed = true
)

select * from final
