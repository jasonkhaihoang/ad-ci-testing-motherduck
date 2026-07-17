# E2E Incremental-Staging Test

## Changes

1. `stg_salescloud__opportunity`: existing view. Comment-only test marker prepended. No grain, materialization, schema, or column changes.
2. Downstream fan-out (`fct_pipeline`, `fct_opportunity_closed_won`, `fct_pipeline_monthly_product`, `fct_sales_pipeline_by_stage`): no changes; included in closure solely via their dependency on `stg_salescloud__opportunity`.

## Models

### stg_salescloud__opportunity

Materialization: view  
Change: comment-only test marker (E2E CI validation, VD-3478).

### fct_pipeline

Materialization: table  
Change: none — downstream dependent, rebuilt as part of closure.

### fct_opportunity_closed_won

Materialization: table  
Change: none — downstream dependent, rebuilt as part of closure.

### fct_pipeline_monthly_product

Materialization: table  
Change: none — downstream dependent, rebuilt as part of closure.

### fct_sales_pipeline_by_stage

Materialization: table  
Change: none — downstream dependent, rebuilt as part of closure.
