{{ config(materialized='table') }}

with source as (
    select
        stage_name,
        count(opportunity_id) as opportunity_count,
        sum(amount) as total_amount,
        avg(probability) as avg_probability
    from {{ ref('stg_salescloud__opportunity') }}
    group by stage_name
)

select * from source
