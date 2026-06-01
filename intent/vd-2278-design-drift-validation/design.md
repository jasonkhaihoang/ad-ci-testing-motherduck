# VD-2278 Design-Drift Validation

## Changes

Two changes in this PR:

1. `stg_salescloud__opportunity`: bump comment for state:modified+ coverage. No logic changes.
2. `fct_won_opportunities`: new table. Reads from `stg_salescloud__opportunity` filtering `stagename = 'Closed Won'`. Grain: one row per opportunity_id. `unique_key: opportunity_id` configured.

## Models

All five models in `state:modified+`. Three downstream models rebuild because `stg_salescloud__opportunity` changed.

### stg_salescloud__opportunity

Materialization: view  
Change: bump comment only. All columns unchanged.  
Columns (20): opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year

### fct_pipeline

Materialization: table  
Change: none (downstream rebuild). No columns defined in schema.yml.

### fct_pipeline_monthly_product

Materialization: table  
Change: none (downstream rebuild). No columns defined in schema.yml.

### fct_sales_pipeline_by_stage

Materialization: table  
Change: none (downstream rebuild). No columns defined in schema.yml.

### fct_won_opportunities

Materialization: table  
unique_key: opportunity_id  
Change: new model added.  
Columns (8): opportunity_id, account_id, owner_id, close_date, fiscal_quarter, fiscal_year, arr, stage_name
