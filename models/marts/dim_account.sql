{{ config(materialized='table') }}

with accounts as (
    select * from {{ ref('stg_salescloud__account') }}
),

final as (
    select
        -- Primary key
        account_id,

        -- Account attributes
        account_name,
        account_type,
        industry,

        -- Location
        billing_city,
        billing_state,
        billing_country,

        -- Relationships
        owner_id,

        -- Flags
        account_type = 'Enterprise' as is_enterprise,  -- VD-2133 validation: schema delta for Gate 5 diff-ack test
        len(account_name) as account_name_length,  -- AC3 test: second column changes diff hash

        -- Audit
        created_date,
        last_modified_date

    from accounts
)

select * from final
