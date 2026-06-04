# E2E Incremental-Staging Test

## Changes

1. `stg_salescloud__opportunity`: existing view. Comment-only test marker prepended to the SQL. No grain, materialization, schema, or column changes.

## Models

### stg_salescloud__opportunity

Materialization: view  
Change: comment-only test marker prepended (E2E CI validation). No logic, schema, grain, or column changes.

### fct_pipeline

Materialization: table  
Change: none — downstream of stg_salescloud__opportunity, included in state:modified+ closure but logic is unchanged.

### fct_opportunity_closed_won

Materialization: table  
Change: none — downstream, included in closure, logic is unchanged.

### fct_pipeline_monthly_product

Materialization: table  
Change: none — downstream, included in closure, logic is unchanged.

### fct_sales_pipeline_by_stage

Materialization: table  
Change: none — downstream, included in closure, logic is unchanged.
