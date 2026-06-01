-- fct_won_opportunities: closed-won opportunities for revenue reporting.
-- Added for VD-2278 design-drift validation.
with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
),

won as (
    select
        opportunityid as opportunity_id,
        accountid as account_id,
        ownerid as owner_id,
        closedate as close_date,
        fiscal_quarter,
        fiscal_year,
        amount as arr,
        stagename as stage_name
    from opportunities
    where
        stagename = 'Closed Won'
        and iswon = true
)

select * from won
