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
Change: none (downstream rebuild).  
Columns (33): opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, forecast_category, sales_cycle_days, opportunity_age_days, days_in_current_stage, is_orphaned_opportunity, is_zero_value, last_modified_date, system_modified_timestamp, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_name, owner_email, owner_is_active

### fct_pipeline_monthly_product

Materialization: table  
Change: none (downstream rebuild).  
Columns (18): close_month, product_id, product_code, product_name, total_revenue, won_revenue, lost_revenue, opportunity_count, won_opportunity_count, lost_opportunity_count, total_quantity, line_item_count, avg_deal_size, avg_unit_price, avg_discount, win_rate_pct, earliest_close_date, latest_close_date

### fct_sales_pipeline_by_stage

Materialization: table  
Change: none (downstream rebuild).  
Columns (9): stage_name, fiscal_year, fiscal_quarter, opportunity_count, won_count, lost_count, total_amount, weighted_amount, avg_probability

### fct_won_opportunities

Materialization: table  
unique_key: opportunity_id  
Change: new model added.  
Columns (8): opportunity_id, account_id, owner_id, close_date, fiscal_quarter, fiscal_year, arr, stage_name
