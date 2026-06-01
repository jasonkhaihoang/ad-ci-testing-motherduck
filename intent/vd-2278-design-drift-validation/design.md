# VD-2278 Design-Drift Validation

## Changes

One change in this PR:

1. `fct_won_opportunities`: new table. Reads from `stg_salescloud__opportunity` filtering `stagename = 'Closed Won'`. Grain: one row per opportunity_id. `unique_key: opportunity_id` configured.

## Models

One model in `state:modified+` — the new mart model added in this PR.

### fct_won_opportunities

Materialization: table  
unique_key: opportunity_id  
Change: new model added.  
Columns (8): account_id, arr, close_date, fiscal_quarter, fiscal_year, opportunity_id, owner_id, stage_name
