# Gate-3/Gate-4 dbt deps Fix Validation (VD-2289/VD-2290)

## Changes

Two changes in this PR:

1. `stg_salescloud__account`: existing view. Comment bump for CI validation.
   No grain, materialization, schema, or column changes — validation marker only.

2. `dim_opportunity_stage`: new table. Aggregates opportunity pipeline volume
   by sales stage. Grain: one row per stage_name.

## Models

### stg_salescloud__account

Materialization: view
Grain: one row per account (account_id)
Change: comment-only validation marker added. No structural changes.

### dim_opportunity_stage

Materialization: table
Grain: one row per stage_name
Change: new model. Columns: stage_name, opportunity_count, total_amount, avg_probability, won_count, lost_count, open_count.

### dim_account

Materialization: table
Grain: one row per account
Change: none — downstream of stg_salescloud__account, no direct modifications.

### dim_user

Materialization: table
Grain: one row per user
Change: none — downstream, no direct modifications.

### fct_pipeline

Materialization: table
Grain: one row per opportunity
Change: none — downstream of stg_salescloud__account via dim_account, no direct modifications.

### fct_pipeline_monthly_product

Materialization: table
Grain: one row per month per product
Change: none — downstream, no direct modifications.

### fct_sales_pipeline_by_stage

Materialization: table
Grain: one row per stage
Change: none — downstream, no direct modifications.
