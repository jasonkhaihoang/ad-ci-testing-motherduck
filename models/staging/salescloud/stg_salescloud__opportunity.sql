{{ config(materialized='view') }}

with source as (
    select * from {{ source('salescloud', 'opportunity') }}
),

renamed as (
    select
        -- Primary key
        id as opportunity_id,

        -- Foreign keys
        accountid as account_id,
        ownerid as owner_id,

        -- Opportunity attributes
        name as opportunity_name,
        stagename as stage_name,
        type as opportunity_type,
        leadsource as lead_source,

        -- Amounts and metrics
        amount,
        probability,
        expectedrevenue as expected_revenue,

        -- Dates
        createddate as created_date,
        closedate as close_date,
        laststagechangedate as last_stage_change_date,

        -- Flags
        isclosed as is_closed,
        iswon as is_won,
        isdeleted as is_deleted,

        -- Audit fields
        lastmodifieddate as last_modified_date,
        systemmodstamp as system_modified_timestamp,

        -- VD-2136: schema delta marker to trigger Gate 5 non-empty diff
        true as is_vd2136_validation,

        -- fiscal quarter from close date (Q1=Jan-Mar, Q2=Apr-Jun, etc.)
        case
            when month(closedate) in (1, 2, 3) then 'Q1'
            when month(closedate) in (4, 5, 6) then 'Q2'
            when month(closedate) in (7, 8, 9) then 'Q3'
            when month(closedate) in (10, 11, 12) then 'Q4'
        end as fiscal_quarter,

        -- Derived: fiscal year of close date
        year(closedate) as fiscal_year

    from source
    where isdeleted = false  -- Exclude soft-deleted records
)

select * from renamed
-- modified: 2026-05-16

-- validation: VD-2030/VD-2035/VU-1194 2026-05-18

-- validation: VD-1747 2026-05-19

-- validation: VD-2138-2142 2026-05-22

-- re-trigger: VD-2138-2142 post-main-baseline 2026-05-22
