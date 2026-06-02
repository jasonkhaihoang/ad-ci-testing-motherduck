{{ config(materialized='table') }}

with opportunities as (
    select * from {{ ref('stg_salescloud__opportunity') }}
    where is_closed = true
      and is_won = true
),

accounts as (
    select * from {{ ref('dim_account') }}
),

users as (
    select * from {{ ref('dim_user') }}
),

final as (
    select
        -- Primary key
        opp.opportunity_id,

        -- Foreign keys
        opp.account_id,
        opp.owner_id,

        -- Opportunity attributes
        opp.opportunity_name,
        opp.stage_name,
        opp.opportunity_type,
        opp.lead_source,

        -- Revenue metrics
        opp.amount,
        opp.probability,
        opp.expected_revenue,
        opp.amount * (opp.probability / 100.0) as weighted_amount,

        -- Dates
        opp.created_date,
        opp.close_date,
        opp.fiscal_quarter,
        opp.fiscal_year,

        -- Sales velocity
        datediff('day', cast(opp.created_date as date), opp.close_date) as sales_cycle_days,

        -- Denormalized account attributes
        acct.account_name,
        acct.account_type,
        acct.industry,
        acct.billing_country,

        -- Denormalized user attributes
        usr.user_name as owner_name,
        usr.email as owner_email

    from opportunities as opp

    left join accounts as acct
        on opp.account_id = acct.account_id

    left join users as usr
        on opp.owner_id = usr.user_id
)

select * from final
