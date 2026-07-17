# VD-3477 cleanup drop-order backport

## Changes

No dbt model source changes. This intent updates `.github/scripts/cleanup_runner.py`
only, swapping the MotherDuck cleanup drop order to DROP SHARE before DROP
DATABASE (MotherDuck refuses DROP DATABASE while a share still references it).

`state:modified+` currently resolves to the full project graph because no
prod-manifest baseline exists (a prior greenfield E2E run intentionally
deleted all successful `publish-prod-manifest-duckdb` runs and a baseline
restore was still in progress at the time this PR was opened). Every model
below is included in closure solely for that reason — none of them changed.

## Models

### dim_account
Materialization: table
Change: none — included in closure only due to missing prod baseline.

### dim_user
Materialization: table
Change: none — included in closure only due to missing prod baseline.

### fct_opportunity_closed_won
Materialization: table
Change: none — included in closure only due to missing prod baseline.

### fct_pipeline
Materialization: table
Change: none — included in closure only due to missing prod baseline.

### fct_pipeline_monthly_product
Materialization: table
Change: none — included in closure only due to missing prod baseline.

### fct_sales_pipeline_by_stage
Materialization: table
Change: none — included in closure only due to missing prod baseline.

### stg_salescloud__account
Materialization: view
Change: none — included in closure only due to missing prod baseline.

### stg_salescloud__opportunity
Materialization: view
Change: none — included in closure only due to missing prod baseline.

### stg_salescloud__opportunitylineitem
Materialization: view
Change: none — included in closure only due to missing prod baseline.

### stg_salescloud__user
Materialization: view
Change: none — included in closure only due to missing prod baseline.
