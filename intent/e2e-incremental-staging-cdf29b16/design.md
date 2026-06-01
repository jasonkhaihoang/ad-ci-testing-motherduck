# E2E Incremental-Staging Test (VD-2282)

## Changes

One change in this PR:

1. `stg_salescloud__opportunity`: existing view. Comment-only test marker prepended.
   No grain, materialization, schema, or column changes — marker line only.

## Models

### stg_salescloud__opportunity

Materialization: view
Change: comment-only test marker prepended (E2E CI validation). No structural changes.

### fct_pipeline

Materialization: table
Change: none — downstream of stg_salescloud__opportunity, no direct modifications.

### fct_pipeline_monthly_product

Materialization: table
Change: none — downstream, no direct modifications.

### fct_sales_pipeline_by_stage

Materialization: table
Change: none — downstream, no direct modifications.
