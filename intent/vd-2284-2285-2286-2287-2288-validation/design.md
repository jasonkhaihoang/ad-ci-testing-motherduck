# MotherDuck CI Fix Validation (VD-2284/2285/2286/2287/2288)

## Changes

Two changes in this PR:

1. `stg_salescloud__opportunity`: existing view. Comment bump for CI validation.
   No grain, materialization, schema, or column changes — validation marker only.

2. `dim_opportunity_summary`: new table. Aggregates opportunity counts and amounts
   by sales stage. Grain: one row per stage_name. References stg_salescloud__opportunity.

## Models

### stg_salescloud__opportunity

Materialization: view
Change: comment-only validation marker updated. No structural changes.

### dim_opportunity_summary

Materialization: table
Change: new model added. Aggregates opportunities by stage_name.
Columns: stage_name (PK), opportunity_count, total_amount, avg_amount, won_count, lost_count.

### fct_pipeline

Materialization: table
Change: none — downstream of stg_salescloud__opportunity, no direct modifications.

### fct_pipeline_monthly_product

Materialization: table
Change: none — downstream, no direct modifications.

### fct_sales_pipeline_by_stage

Materialization: table
Change: none — downstream, no direct modifications.
