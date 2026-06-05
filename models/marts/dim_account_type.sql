{{ config(materialized='table') }}

-- VD-2380: account counts by type and industry.

with accounts as (
    select * from {{ ref('stg_salescloud__account') }}
),

final as (
    select
        coalesce(account_type, 'Unknown') as account_type,
        coalesce(industry, 'Unknown') as industry,
        count(*) as account_count

    from accounts
    group by 1, 2
)

select * from final
