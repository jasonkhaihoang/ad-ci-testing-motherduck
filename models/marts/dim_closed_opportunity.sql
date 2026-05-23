{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

closed as (
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
        is_won,
        created_date
    from opportunities
    where is_closed = true
)

select * from closed
