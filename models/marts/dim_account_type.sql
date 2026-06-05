{{ config(materialized='table') }}

-- VD-2380: dim_account_type — account counts grouped by type and industry.
-- Added to exercise Dive qualified-ref fix (AC-10 of domain-pr-review-approval).

with accounts as (
    select * from {{ ref('stg_salescloud__account') }}
),

final as (
    select
        coalesce(account_type, 'Unknown')   as account_type,
        coalesce(industry, 'Unknown')       as industry,
        count(*)                             as account_count

    from accounts
    group by 1, 2
)

select * from final
