{{ config(materialized='table') }}

with accounts as (
    select * from {{ ref('stg_salescloud__account') }}
),

final as (
    select distinct
        -- Primary key (surrogate: industry name)
        industry,

        -- Aggregated stats
        count(*) over (partition by industry) as account_count

    from accounts
    where industry is not null
)

select * from final
-- VD-2299 AC-10 validation
